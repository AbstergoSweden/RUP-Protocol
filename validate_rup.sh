#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
# RUP Protocol Validator v2.1.0 - Bash Script
#
# Validates RUP protocol YAML files and agent outputs against the JSON Schema.
#
# Usage:
#   ./validate_rup.sh protocol <protocol.yaml>
#   ./validate_rup.sh output <output.json> <discovery|plan|execution|verification>
#   ./validate_rup.sh all <directory>
#
# Requirements:
#   - Node.js with npm
#   - ajv-cli: npm install -g ajv-cli ajv-formats
#   - js-yaml: npm install -g js-yaml
#
# Author: Faye Håkansdotter
# License: CC0-1.0
#═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_PATH="${SCHEMA_PATH:-$SCRIPT_DIR/rup-schema.json}"

# Print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_header() {
    echo -e "${BOLD}$1${NC}"
}

# Check dependencies
check_dependencies() {
    local missing=()
    
    if ! command -v node &> /dev/null; then
        missing+=("node")
    fi
    
    if ! command -v npx &> /dev/null; then
        missing+=("npx")
    fi
    
    if [ ${#missing[@]} -gt 0 ]; then
        print_error "Missing dependencies: ${missing[*]}"
        echo "Please install Node.js: https://nodejs.org/"
        exit 1
    fi
    
    # Check for ajv-cli
    if ! npx ajv --version &> /dev/null 2>&1; then
        print_warning "ajv-cli not found. Installing..."
        npm install -g ajv-cli ajv-formats
    fi
}

# Validate protocol YAML
validate_protocol() {
    local protocol_file="$1"
    
    if [ ! -f "$protocol_file" ]; then
        print_error "Protocol file not found: $protocol_file"
        exit 1
    fi
    
    if [ ! -f "$SCHEMA_PATH" ]; then
        print_error "Schema file not found: $SCHEMA_PATH"
        exit 1
    fi
    
    print_info "Validating protocol: $protocol_file"
    
    # Convert YAML to JSON for validation
    local temp_json=$(mktemp)
    trap "rm -f $temp_json" EXIT
    
    # Use Node.js to convert YAML to JSON
    node -e "
        const yaml = require('js-yaml');
        const fs = require('fs');
        try {
            const doc = yaml.load(fs.readFileSync('$protocol_file', 'utf8'));
            console.log(JSON.stringify(doc, null, 2));
        } catch (e) {
            console.error('Error parsing YAML:', e.message);
            process.exit(1);
        }
    " > "$temp_json" 2>&1
    
    if [ $? -ne 0 ]; then
        print_error "Failed to parse YAML"
        cat "$temp_json"
        exit 1
    fi
    
    # Validate with ajv
    if npx ajv validate -s "$SCHEMA_PATH" -d "$temp_json" --strict=false --all-errors 2>&1; then
        print_success "Protocol is valid: $protocol_file"
        return 0
    else
        print_error "Protocol validation failed: $protocol_file"
        return 1
    fi
}

# Validate agent output JSON
validate_output() {
    local output_file="$1"
    local output_type="$2"
    
    if [ ! -f "$output_file" ]; then
        print_error "Output file not found: $output_file"
        exit 1
    fi
    
    if [ ! -f "$SCHEMA_PATH" ]; then
        print_error "Schema file not found: $SCHEMA_PATH"
        exit 1
    fi
    
    # Map output types to schema definitions
    local def_name=""
    case "$output_type" in
        discovery)
            def_name="DiscoveryReport"
            ;;
        plan)
            def_name="PlanOutput"
            ;;
        execution)
            def_name="ExecutionOutput"
            ;;
        verification)
            def_name="VerificationOutput"
            ;;
        *)
            print_error "Unknown output type: $output_type"
            echo "Valid types: discovery, plan, execution, verification"
            exit 1
            ;;
    esac
    
    print_info "Validating $output_type output: $output_file"
    
    # Create a temporary schema that references the specific definition
    local temp_schema=$(mktemp)
    trap "rm -f $temp_schema" EXIT
    
    node -e "
        const fs = require('fs');
        const schema = JSON.parse(fs.readFileSync('$SCHEMA_PATH', 'utf8'));
        const subSchema = {
            '\$schema': schema['\$schema'],
            '\$id': schema['\$id'] + '#/$def_name',
            ...schema['\$defs']['$def_name'],
            '\$defs': schema['\$defs']
        };
        console.log(JSON.stringify(subSchema, null, 2));
    " > "$temp_schema"
    
    # Validate with ajv
    if npx ajv validate -s "$temp_schema" -d "$output_file" --strict=false --all-errors 2>&1; then
        print_success "Output is valid: $output_file"
        return 0
    else
        print_error "Output validation failed: $output_file"
        return 1
    fi
}

# Validate all files in a directory
validate_all() {
    local directory="$1"
    
    if [ ! -d "$directory" ]; then
        print_error "Directory not found: $directory"
        exit 1
    fi
    
    print_header "Validating all files in: $directory"
    echo "════════════════════════════════════════════════════════"
    
    local total=0
    local valid=0
    local invalid=0
    
    # Find and validate protocol files
    while IFS= read -r -d '' file; do
        if [[ "$file" == *"protocol"* ]]; then
            ((total++))
            if validate_protocol "$file"; then
                ((valid++))
            else
                ((invalid++))
            fi
        fi
    done < <(find "$directory" -name "*.yaml" -o -name "*.yml" -print0 2>/dev/null)
    
    # Find and validate output files
    local output_patterns=(
        "discovery:discovery*.json"
        "plan:plan*.json"
        "execution:execution*.json"
        "execution:changes*.json"
        "verification:verification*.json"
        "verification:report*.json"
    )
    
    for pattern in "${output_patterns[@]}"; do
        local type="${pattern%%:*}"
        local glob="${pattern##*:}"
        
        while IFS= read -r -d '' file; do
            ((total++))
            if validate_output "$file" "$type"; then
                ((valid++))
            else
                ((invalid++))
            fi
        done < <(find "$directory" -name "$glob" -print0 2>/dev/null)
    done
    
    echo "════════════════════════════════════════════════════════"
    echo "Total: $total files"
    print_success "Valid: $valid"
    if [ $invalid -gt 0 ]; then
        print_error "Invalid: $invalid"
        return 1
    fi
    return 0
}

# Print usage
print_usage() {
    cat << EOF
${BOLD}RUP Protocol Validator v2.1.0${NC}

${BOLD}Usage:${NC}
    $0 protocol <protocol.yaml>     Validate a protocol YAML file
    $0 output <file.json> <type>    Validate an agent output JSON file
    $0 all <directory>              Validate all files in a directory
    $0 help                         Show this help message

${BOLD}Output Types:${NC}
    discovery       Discovery agent output
    plan            Planning agent output
    execution       Execution agent output
    verification    Verification agent output

${BOLD}Examples:${NC}
    $0 protocol rup-protocol-v2.1.yaml
    $0 output discovery.json discovery
    $0 output plan.json plan
    $0 all ./my-project

${BOLD}Environment Variables:${NC}
    SCHEMA_PATH     Path to rup-schema.json (default: same directory as script)

EOF
}

# Main entry point
main() {
    local command="${1:-help}"
    
    case "$command" in
        protocol)
            if [ -z "$2" ]; then
                print_error "Missing protocol file argument"
                print_usage
                exit 1
            fi
            check_dependencies
            validate_protocol "$2"
            ;;
        output)
            if [ -z "$2" ] || [ -z "$3" ]; then
                print_error "Missing arguments"
                print_usage
                exit 1
            fi
            check_dependencies
            validate_output "$2" "$3"
            ;;
        all)
            if [ -z "$2" ]; then
                print_error "Missing directory argument"
                print_usage
                exit 1
            fi
            check_dependencies
            validate_all "$2"
            ;;
        help|--help|-h)
            print_usage
            ;;
        *)
            print_error "Unknown command: $command"
            print_usage
            exit 1
            ;;
    esac
}

main "$@"
