#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
# RUP Protocol Validator v3.0.0 - Bash Script
#
# Validates RUP protocol YAML files and agent outputs against the JSON Schema.
#
# Usage:
#   ./validate_rup.sh protocol <protocol.yaml>
#   ./validate_rup.sh output <output.json> <discovery|plan|execution|verification>
#   ./validate_rup.sh all <directory>
#   ./validate_rup.sh [options] <command> <args...>
#
# Options:
#   -s, --schema <path>   Path to rup-schema.json
#   -v, --verbose         Show all validation errors
#
# Requirements:
#   - Node.js with npm
#   - npm install (in this directory)
#
# Author: Faye Håkansdotter
# License: CC0-1.0
#═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Print colored output
print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Main entry point
main() {
    VALIDATOR_SCRIPT="$SCRIPT_DIR/../../validators/validate_rup.js"
    # Check if validate_rup.js exists
    if [ ! -f "$VALIDATOR_SCRIPT" ]; then
        print_error "validate_rup.js not found at $VALIDATOR_SCRIPT"
        exit 1
    fi

    # Verify Node.js is available
    if ! command -v node &> /dev/null; then
        print_error "Node.js is required but not found"
        exit 1
    fi

    # Delegate to validate_rup.js
    node "$VALIDATOR_SCRIPT" "$@"
}

main "$@"
