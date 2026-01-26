#!/usr/bin/env python3
"""
RUP Protocol Builder

Merges split YAML definition files into a single monolithic protocol file.
Usage: python build_rup.py [source_file] [output_file]
"""

import yaml
import os
import sys
from pathlib import Path
from typing import Any

# Custom loader to handle !include tags
class IncludeLoader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(IncludeLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r', encoding='utf-8') as f:
            return yaml.load(f, Loader=IncludeLoader)

IncludeLoader.add_constructor('!include', IncludeLoader.include)

def build(source_path: Path, output_path: Path):
    print(f"Building {output_path} from {source_path}...")
    
    with open(source_path, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=IncludeLoader)
    
    # Add auto-generated header
    header = "# AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY\n"
    header += f"# Source: {source_path}\n"
    header += "# Edit the files in definitions/ instead.\n\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, width=100, allow_unicode=True)
    
    print("Done.")

if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("rup-protocol-src.yaml")
    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("rup-protocol.gen.yaml")
    
    if not src.exists():
        print(f"Error: Source file {src} not found.")
        sys.exit(1)
        
    build(src, dest)
