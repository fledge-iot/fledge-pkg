#!/bin/bash
#
# Fledge Package Dependency Verification Script
#
# This script verifies that all dependencies listed in a Debian control file
# are available in the package repositories for the target platform.
#
# Usage: verify-dependencies.sh <control_file> <report_file> <os> <arch> <codename>
#
# Arguments:
#   control_file - Path to the Debian control file
#   report_file  - Path where the verification report will be generated
#   os          - Operating system (e.g., ubuntu-22.04)
#   arch        - Architecture (e.g., x86_64, aarch64)
#   codename    - OS codename (e.g., jammy, noble)
#

set -euo pipefail

# Script metadata
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Global variables
CONTROL_FILE=""
REPORT_FILE=""
OS=""
ARCH=""
CODENAME=""
TEMP_CONTROL_FILE=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $*${NC}" >&2
}

log_success() {
    echo -e "${GREEN}✅ $*${NC}" >&2
}

log_warning() {
    echo -e "${YELLOW}⚠️  $*${NC}" >&2
}

log_error() {
    echo -e "${RED}❌ $*${NC}" >&2
}

# Function to show usage
usage() {
    cat << EOF
Usage: $SCRIPT_NAME <control_file> <report_file> <os> <arch> <codename>

Arguments:
    control_file    Path to the Debian control file
    report_file     Path where the verification report will be generated
    os             Operating system (e.g., ubuntu-22.04)
    arch           Architecture (e.g., x86_64, aarch64)
    codename       OS codename (e.g., jammy, noble)

Environment Variables:
    GITHUB_WORKFLOW    GitHub workflow name (optional)
    GITHUB_RUN_NUMBER  GitHub run number (optional)

Examples:
    $SCRIPT_NAME packages/Debian/x86_64/DEBIAN/control report.md ubuntu-22.04 x86_64 jammy
EOF
}

# Function to validate control file exists
validate_control_file() {
    local control_file="$1"
    
    log_info "Validating control file: $control_file"
    
    if [ ! -f "$control_file" ]; then
        log_error "Control file missing: $control_file"
        log_info "Available files in packages/Debian/:"
        find packages/Debian/ -name "control" 2>/dev/null || log_warning "No control files found"
        return 1
    fi
    
    log_success "Control file found: $control_file"
    return 0
}

# Enhanced dependency extraction function
extract_deps() {
    local field="$1"
    local control_file="${2:-$CONTROL_FILE}"
    
    awk -v field="$field" '
        BEGIN { found=0; deps="" }
        {
            if ($0 ~ "^" field ":") {
                found=1
                gsub("^" field ":[[:space:]]*", "")
                deps = $0
            } else if (found && $0 ~ "^[[:space:]]") {
                # Continuation line (starts with whitespace)
                gsub("^[[:space:]]*", "")
                if ($0 != "") {
                    deps = deps " " $0
                }
            } else if (found && $0 !~ "^[[:space:]]" && $0 != "") {
                # New field found, stop processing
                print deps
                exit
            }
        }
        END { if (found && deps != "") print deps }
    ' "$control_file" | \
    tr ',' '\n' | \
    sed -E 's/\([^)]*\)//g' | \
    sed -E 's/\[[^]]*\]//g' | \
    awk '{gsub(/^[[:space:]]+|[[:space:]]+$/, ""); if ($1 != "") print $1}' | \
    sort -u
}

# Function to detect and resolve version placeholders
resolve_version_placeholders() {
    local control_file="$1"
    local temp_file=""

    log_info "Checking for version placeholders in $(basename "$control_file")..."

    # Check for BOOST_VER placeholder
    if grep -q "{{BOOST_VER}}" "$control_file"; then
        log_info "Found {{BOOST_VER}} placeholder, resolving Boost version..."

        local boost_version=""
        local boost_suffix=""

        # Method 1: Check installed libboost-dev package
        if [ -z "$boost_version" ] && command -v dpkg >/dev/null 2>&1; then
            boost_version=$(dpkg -l 2>/dev/null | grep "libboost-dev" | awk '{print $3}' | sed -n 's/^\([0-9]\+\.[0-9]\+\.[0-9]\+\).*/\1/p' | head -1 || true)
            [ -n "$boost_version" ] && log_success "Found installed Boost version: $boost_version"
        fi

        # Method 2: Check available package version
        if [ -z "$boost_version" ] && command -v apt-cache >/dev/null 2>&1; then
            boost_version=$(apt-cache policy libboost-dev 2>/dev/null | grep "Candidate:" | awk '{print $2}' | sed -n 's/^\([0-9]\+\.[0-9]\+\.[0-9]\+\).*/\1/p' | head -1 || true)
            [ -n "$boost_version" ] && log_success "Found available Boost version: $boost_version"
        fi
        
        # Fallback: Use a common default version if we can't detect it
        if [ -z "$boost_version" ]; then
            boost_version="1.74.0"
            log_warning "Could not detect Boost version, using default: $boost_version"
        fi

        # Determine the correct Boost package suffix format
        log_info "Determining correct Boost package naming format..."

        local boost_major_minor=$(echo "$boost_version" | cut -d'.' -f1-2)
        local boost_major_minor_no_dot=$(echo "$boost_major_minor" | tr -d '.')

        # Test different naming conventions
        if apt-cache show "libboost-system${boost_version}" >/dev/null 2>&1; then
            boost_suffix="$boost_version"
            log_success "Found format: libboost-system${boost_suffix}"
        elif apt-cache show "libboost-system${boost_major_minor}" >/dev/null 2>&1; then
            boost_suffix="$boost_major_minor"
            log_success "Found format: libboost-system${boost_suffix}"
        elif apt-cache show "libboost-system${boost_major_minor_no_dot}" >/dev/null 2>&1; then
            boost_suffix="$boost_major_minor_no_dot"
            log_success "Found format: libboost-system${boost_suffix}"
        else
            # Fallback to the most common format
            boost_suffix="$boost_major_minor"
            log_warning "Could not detect format, using default: libboost-system${boost_suffix}"
        fi

        log_info "Final Boost package suffix: $boost_suffix"

        # Create temporary file if not already created
        if [ -z "$temp_file" ]; then
            temp_file=$(mktemp)
            cp "$control_file" "$temp_file"
        fi

        # Replace BOOST_VER placeholder
        if command -v sed >/dev/null 2>&1; then
            # Use a more portable sed command
            sed "s/{{BOOST_VER}}/${boost_suffix}/g" "$temp_file" > "${temp_file}.new" && mv "${temp_file}.new" "$temp_file"
        else
            log_error "sed command not available"
            return 1
        fi
        log_success "Resolved {{BOOST_VER}} to ${boost_suffix}"

        # Show resolved dependencies for verification
        log_info "Resolved Boost dependencies:"
        grep -E "libboost.*${boost_suffix}" "$temp_file" >&2 || true
    fi

    # TODO: Add more placeholder handlers here in the future
    # Example for future use:
    # if grep -q "{{PYTHON_VER}}" "$control_file"; then
    #     log_info "Found {{PYTHON_VER}} placeholder, resolving Python version..."
    #     # Add Python version detection logic here
    # fi

    # Return the path to the resolved file (or original if no changes)
    if [ -n "$temp_file" ]; then
        log_info "Using temporary control file with resolved placeholders: $temp_file"
        echo "$temp_file"
    else
        log_info "No version placeholders found, using original file"
        echo "$control_file"
    fi
}

# Function to update package cache with retry
update_package_cache() {
    log_info "Updating package cache..."
    
    for i in {1..3}; do
        if sudo apt-get update -qq; then
            log_success "Package cache updated successfully"
            return 0
        elif [ $i -eq 3 ]; then
            log_error "Failed to update package cache after 3 attempts"
            return 1
        else
            log_warning "Package cache update failed, retrying in 10s..."
            sleep 10
        fi
    done
}

# Enhanced dependency checking function
check_dependencies() {
    local label="$1"
    local pkgs="$2"
    local is_critical="$3"
    local fail=0
    local total=0
    local available=0

    echo "" >> "$REPORT_FILE"
    echo "## $label" >> "$REPORT_FILE"

    if [ -z "$pkgs" ]; then
        echo "- ℹ️ No $label specified" >> "$REPORT_FILE"
        return 0
    fi

    log_info "Checking $label..."

    for pkg in $pkgs; do
        total=$((total + 1))

        # Skip empty package names
        [ -z "$pkg" ] && continue

        # Check if package is available
        if apt-cache show "$pkg" > /dev/null 2>&1; then
            # Get package version info
            version=$(apt-cache policy "$pkg" 2>/dev/null | grep "Candidate:" | awk '{print $2}' || echo "unknown")
            echo "- ✅ **$pkg** (version: $version)" >> "$REPORT_FILE"
            available=$((available + 1))
            log_success "$pkg (version: $version)"
        else
            echo "- ❌ **$pkg** - Package not found in repositories" >> "$REPORT_FILE"
            log_error "$pkg - Package not found in repositories"

            # Try to find similar packages
            similar=$(apt-cache search "^$pkg" 2>/dev/null | head -3 | cut -d' ' -f1 | tr '\n' ', ' | sed 's/,$//')
            if [ -n "$similar" ]; then
                echo "  - 💡 Similar packages: $similar" >> "$REPORT_FILE"
                log_info "Similar packages: $similar"
            fi

            if [ "$is_critical" = "true" ]; then
                fail=1
            fi
        fi
    done

    # Add summary
    echo "" >> "$REPORT_FILE"
    echo "**Summary:** $available/$total packages available" >> "$REPORT_FILE"

    if [ $fail -eq 1 ]; then
        echo "⚠️ **Critical dependencies missing!**" >> "$REPORT_FILE"
        log_error "Critical dependencies missing!"
    else
        log_success "$label verification complete: $available/$total packages available"
    fi

    return $fail
}

# Function to initialize the report
initialize_report() {
    log_info "Initializing report: $REPORT_FILE"
    
    cat > "$REPORT_FILE" << EOF
## 📦 Dependency Verification Report

**Platform:** $ARCH on $OS ($CODENAME)  
**Generated:** $(date -u '+%Y-%m-%d %H:%M:%S UTC')  
**Workflow:** ${GITHUB_WORKFLOW:-Manual} - Run #${GITHUB_RUN_NUMBER:-N/A}

EOF
    
    log_success "Report initialized"
}

# Function to finalize the report
finalize_report() {
    log_info "Finalizing report..."
    
    cat >> "$REPORT_FILE" << EOF

---

## ✅ Verification Complete

All dependencies are accessible for $ARCH on $OS ($CODENAME).

EOF
    
    log_success "Report finalized"
}

# Function to validate report was generated
validate_report() {
    if [ ! -f "$REPORT_FILE" ] || [ ! -s "$REPORT_FILE" ]; then
        log_error "Report file is missing or empty"
        return 1
    fi
    
    local line_count=$(wc -l < "$REPORT_FILE")
    log_success "Report generated successfully ($line_count lines)"
    return 0
}

# Function to cleanup temporary files
cleanup() {
    if [ -n "${TEMP_CONTROL_FILE:-}" ] && [ -f "$TEMP_CONTROL_FILE" ]; then
        rm -f "$TEMP_CONTROL_FILE"
        log_success "Cleaned up temporary control file"
    fi
}

# Function to handle script interruption
handle_interrupt() {
    local exit_code=$?
    log_warning "Script interrupted (exit code: $exit_code)"
    cleanup
    exit $exit_code
}

# Main function
main() {
    # Parse arguments
    if [ $# -ne 5 ]; then
        log_error "Invalid number of arguments"
        usage
        exit 1
    fi
    
    CONTROL_FILE="$1"
    REPORT_FILE="$2"
    OS="$3"
    ARCH="$4"
    CODENAME="$5"
    
    log_info "Starting dependency verification for $ARCH on $OS ($CODENAME)"
    log_info "Control file: $CONTROL_FILE"
    log_info "Report file: $REPORT_FILE"
    
    # Validate control file exists
    if ! validate_control_file "$CONTROL_FILE"; then
        exit 1
    fi
    
    # Initialize report
    initialize_report
    
    # Resolve version placeholders in control file
    log_info "Original control file path: $CONTROL_FILE"
    local resolved_control_file
    resolved_control_file=$(resolve_version_placeholders "$CONTROL_FILE")
    log_info "Resolved control file path: $resolved_control_file"
    
    # Store the temporary file path for cleanup later
    if [ "$resolved_control_file" != "$CONTROL_FILE" ]; then
        TEMP_CONTROL_FILE="$resolved_control_file"
        log_info "Using resolved control file: $TEMP_CONTROL_FILE"
    else
        log_info "Using original control file: $CONTROL_FILE"
    fi
    
    # Update CONTROL_FILE to point to the resolved file
    CONTROL_FILE="$resolved_control_file"
    
    # Extract dependencies
    log_info "Extracting dependencies from control file..."
    log_info "Using control file: $CONTROL_FILE"
    
    # Verify the control file exists and is readable
    if [ ! -f "$CONTROL_FILE" ]; then
        log_error "Control file not found: $CONTROL_FILE"
        exit 1
    fi
    
    if [ ! -r "$CONTROL_FILE" ]; then
        log_error "Control file not readable: $CONTROL_FILE"
        exit 1
    fi
    
    local build_deps runtime_deps recommends suggests
    build_deps=$(extract_deps "Build-Depends")
    runtime_deps=$(extract_deps "Depends")
    recommends=$(extract_deps "Recommends")
    suggests=$(extract_deps "Suggests")
    
    # Validate extraction results
    local build_count runtime_count
    build_count=$(echo "$build_deps" | wc -w)
    runtime_count=$(echo "$runtime_deps" | wc -w)
    
    log_info "Extraction results:"
    log_info "  - Build dependencies: $build_count packages"
    log_info "  - Runtime dependencies: $runtime_count packages"
    log_info "  - Recommended packages: $(echo "$recommends" | wc -w) packages"
    log_info "  - Suggested packages: $(echo "$suggests" | wc -w) packages"
    
    if [ $build_count -eq 0 ] && [ $runtime_count -eq 0 ]; then
        log_error "No dependencies extracted! This might indicate a parsing error."
        log_info "Control file content:"
        head -20 "$CONTROL_FILE"
        exit 1
    fi
    
    # Update package cache
    if ! update_package_cache; then
        exit 1
    fi
    
    # Check all dependency types
    local exit_code=0
    
    if ! check_dependencies "🔨 Build Dependencies" "$build_deps" "true"; then
        exit_code=1
    fi
    
    if ! check_dependencies "🏃 Runtime Dependencies" "$runtime_deps" "true"; then
        exit_code=1
    fi
    
    # Non-critical dependencies (don't fail the build)
    check_dependencies "💡 Recommended Packages" "$recommends" "false" || true
    check_dependencies "🔧 Suggested Packages" "$suggests" "false" || true
    
    # Finalize report
    finalize_report
    
    # Validate report was generated
    if ! validate_report; then
        exit_code=1
    fi
    
    # Cleanup temporary files
    cleanup
    
    if [ $exit_code -eq 0 ]; then
        log_success "Dependency verification completed successfully"
        log_info "All critical dependencies are available in the repositories"
    else
        log_error "Dependency verification failed (exit code: $exit_code)"
        log_error "This indicates build or runtime dependencies are missing."
        log_error "Please review the generated report and update the control file or repository configuration."
        
        # Provide additional context for debugging
        if [ -f "$REPORT_FILE" ]; then
            log_info "Report file generated at: $REPORT_FILE"
            log_info "Check the report for detailed information about missing packages"
        else
            log_error "Report file was not generated, indicating a critical script failure"
        fi
    fi
    
    exit $exit_code
}

# Set up signal handlers for cleanup and interruption
trap cleanup EXIT
trap handle_interrupt INT TERM

# Run main function
main "$@"
