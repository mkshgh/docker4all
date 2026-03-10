#!/usr/bin/env python3
"""
ReStructuredText to Markdown Converter
Converts .rst files to .md format with Docker syntax modernization
"""

import re
import os
import sys
from pathlib import Path


class RSTtoMDConverter:
    """Converts ReStructuredText files to Markdown format"""
    
    def __init__(self):
        self.content = ""
    
    def convert_file(self, rst_file_path):
        """Convert a single RST file to Markdown"""
        with open(rst_file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        # Apply conversions in order
        self.convert_headings()
        self.convert_inline_code()  # Do this before code blocks
        self.convert_code_blocks()
        self.convert_links()
        self.convert_lists()
        self.modernize_docker_syntax()
        
        return self.content
    
    def convert_headings(self):
        """Convert RST heading syntax to Markdown"""
        lines = self.content.split('\n')
        converted = []
        i = 0
        
        while i < len(lines):
            current_line = lines[i]
            
            # Check if next line is an underline
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                
                # Level 1 heading (===)
                if re.match(r'^=+$', next_line) and len(next_line) >= len(current_line.strip()):
                    converted.append(f"# {current_line.strip()}")
                    i += 2  # Skip the underline
                    continue
                
                # Level 2 heading (---)
                elif re.match(r'^-+$', next_line) and len(next_line) >= len(current_line.strip()):
                    converted.append(f"## {current_line.strip()}")
                    i += 2  # Skip the underline
                    continue
                
                # Level 3 heading (~~~)
                elif re.match(r'^~+$', next_line) and len(next_line) >= len(current_line.strip()):
                    converted.append(f"### {current_line.strip()}")
                    i += 2  # Skip the underline
                    continue
            
            converted.append(current_line)
            i += 1
        
        self.content = '\n'.join(converted)
    
    def convert_code_blocks(self):
        """Convert RST code blocks to Markdown fenced code blocks"""
        # Convert .. code-block:: language to ```language
        pattern = r'\.\. code-block::\s*(\w+)\s*\n+((?:(?:    |\t).*\n?)*)'
        
        def replace_code_block(match):
            language = match.group(1)
            code = match.group(2)
            # Remove 4-space or tab indentation
            code_lines = code.split('\n')
            dedented = []
            for line in code_lines:
                if line.startswith('    '):
                    dedented.append(line[4:])
                elif line.startswith('\t'):
                    dedented.append(line[1:])
                else:
                    dedented.append(line)
            code_content = '\n'.join(dedented).rstrip()
            return f"```{language}\n{code_content}\n```"
        
        self.content = re.sub(pattern, replace_code_block, self.content, flags=re.MULTILINE)
        
        # Convert simple :: code blocks
        pattern = r'::\s*\n+((?:(?:    |\t).*\n?)*)'
        
        def replace_simple_code(match):
            code = match.group(1)
            code_lines = code.split('\n')
            dedented = []
            for line in code_lines:
                if line.startswith('    '):
                    dedented.append(line[4:])
                elif line.startswith('\t'):
                    dedented.append(line[1:])
                else:
                    dedented.append(line)
            code_content = '\n'.join(dedented).rstrip()
            return f"```bash\n{code_content}\n```"
        
        self.content = re.sub(pattern, replace_simple_code, self.content, flags=re.MULTILINE)
    
    def convert_links(self):
        """Convert RST links to Markdown format"""
        # Convert `Link Text <URL>`_
        pattern = r'`([^<]+)<([^>]+)>`_'
        self.content = re.sub(pattern, r'[\1](\2)', self.content)
        
        # Convert simple links
        pattern = r'`([^`]+)`_'
        self.content = re.sub(pattern, r'[\1]', self.content)
    
    def convert_lists(self):
        """Convert RST lists to Markdown format"""
        lines = self.content.split('\n')
        converted = []
        
        for line in lines:
            # Convert numbered lists (1., 2., etc.)
            if re.match(r'^\d+\.\s+', line):
                converted.append(line)
            # Convert bullet lists (-, *, +)
            elif re.match(r'^[\-\*\+]\s+', line):
                # Ensure consistent bullet marker (-)
                converted.append(re.sub(r'^[\-\*\+]\s+', '- ', line))
            else:
                converted.append(line)
        
        self.content = '\n'.join(converted)
    
    def convert_inline_code(self):
        """Convert RST inline code to Markdown"""
        # Convert ``code`` to `code`
        self.content = re.sub(r'``([^`]+)``', r'`\1`', self.content)
    
    def modernize_docker_syntax(self):
        """Modernize Docker syntax to 2025+ standards"""
        # docker-compose -> docker compose
        self.content = re.sub(r'\bdocker-compose\b', 'docker compose', self.content)
        
        # -v flag -> --mount (in explanatory text, not in actual commands yet)
        # This is a placeholder for more sophisticated conversion
        
        # Update file references from .rst to .md
        self.content = re.sub(r'\.rst\b', '.md', self.content)
    
    def save_to_file(self, output_path):
        """Save converted content to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.content)


def convert_directory(source_dir, output_dir):
    """Convert all RST files in a directory"""
    converter = RSTtoMDConverter()
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    converted_files = []
    
    for rst_file in source_path.rglob('*.rst'):
        # Calculate relative path
        rel_path = rst_file.relative_to(source_path)
        
        # Change extension to .md
        md_filename = rel_path.stem + '.md'
        output_file = output_path / rel_path.parent / md_filename
        
        print(f"Converting: {rst_file} -> {output_file}")
        
        try:
            content = converter.convert_file(rst_file)
            converter.save_to_file(output_file)
            converted_files.append((str(rst_file), str(output_file)))
            print(f"  ✓ Converted successfully")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    return converted_files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rst_to_md_converter.py <source_dir> [output_dir]")
        print("Example: python rst_to_md_converter.py 'Basic Intro' temp_converted")
        sys.exit(1)
    
    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "temp_converted"
    
    if not os.path.exists(source):
        print(f"Error: Source directory '{source}' does not exist")
        sys.exit(1)
    
    print(f"Converting RST files from '{source}' to '{output}'...")
    converted = convert_directory(source, output)
    
    print(f"\nConversion complete! Converted {len(converted)} files.")
