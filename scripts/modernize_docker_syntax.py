#!/usr/bin/env python3
"""
Docker Syntax Modernizer
Updates Docker commands and syntax to 2025+ standards
"""

import re
import os
import sys
from pathlib import Path


class DockerSyntaxModernizer:
    """Modernizes Docker syntax in markdown files"""
    
    def __init__(self):
        self.content = ""
        self.changes_made = []
    
    def modernize_file(self, file_path):
        """Modernize Docker syntax in a single file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        self.changes_made = []
        original_content = self.content
        
        # Apply modernizations
        self.modernize_compose_command()
        self.modernize_volume_syntax()
        self.modernize_compose_file_names()
        self.remove_deprecated_commands()
        self.add_modern_flags()
        
        # Check if changes were made
        if self.content != original_content:
            return True, self.changes_made
        return False, []
    
    def modernize_compose_command(self):
        """Replace docker-compose with docker compose"""
        pattern = r'\bdocker-compose\b'
        if re.search(pattern, self.content):
            self.content = re.sub(pattern, 'docker compose', self.content)
            self.changes_made.append("docker-compose → docker compose")
    
    def modernize_volume_syntax(self):
        """Update -v flag to --mount where appropriate"""
        # This is complex and context-dependent, so we'll add comments for now
        # Pattern: docker run -v /host:/container
        pattern = r'docker run ([^\n]*)-v\s+([^\s:]+):([^\s]+)'
        
        def replace_volume(match):
            before_flags = match.group(1)
            host_path = match.group(2)
            container_path = match.group(3)
            
            # Add a comment suggesting modern syntax
            self.changes_made.append(f"-v flag found (consider --mount)")
            return match.group(0)  # Keep original for now, will update in content creation
        
        if re.search(pattern, self.content):
            self.content = re.sub(pattern, replace_volume, self.content)
    
    def modernize_compose_file_names(self):
        """Update docker-compose.yml references to compose.yaml"""
        patterns = [
            (r'\bdocker-compose\.yml\b', 'compose.yaml'),
            (r'\bdocker-compose\.yaml\b', 'compose.yaml'),
        ]
        
        for pattern, replacement in patterns:
            if re.search(pattern, self.content):
                self.content = re.sub(pattern, replacement, self.content)
                self.changes_made.append(f"{pattern} → {replacement}")
    
    def remove_deprecated_commands(self):
        """Flag deprecated Docker commands"""
        deprecated = [
            r'\bdocker-machine\b',
            r'\bdocker-swarm\b',
        ]
        
        for pattern in deprecated:
            if re.search(pattern, self.content):
                self.changes_made.append(f"Deprecated command found: {pattern}")
    
    def add_modern_flags(self):
        """Suggest modern flag alternatives"""
        # This is informational - actual updates happen during content creation
        old_new_flags = [
            (r'--link\b', '--network (consider using networks instead of --link)'),
        ]
        
        for old_pattern, suggestion in old_new_flags:
            if re.search(old_pattern, self.content):
                self.changes_made.append(f"Old flag found: {suggestion}")
    
    def save_to_file(self, output_path):
        """Save modernized content to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.content)


def modernize_directory(source_dir, output_dir=None):
    """Modernize all markdown files in a directory"""
    modernizer = DockerSyntaxModernizer()
    source_path = Path(source_dir)
    
    if output_dir is None:
        output_dir = source_dir
    output_path = Path(output_dir)
    
    modernized_files = []
    
    for md_file in source_path.rglob('*.md'):
        # Calculate relative path
        rel_path = md_file.relative_to(source_path)
        output_file = output_path / rel_path
        
        print(f"Modernizing: {md_file}")
        
        try:
            changed, changes = modernizer.modernize_file(md_file)
            
            if changed:
                modernizer.save_to_file(output_file)
                print(f"  ✓ Modernized: {', '.join(changes)}")
                modernized_files.append((str(md_file), changes))
            else:
                # Copy unchanged file if output is different directory
                if output_dir != source_dir:
                    modernizer.save_to_file(output_file)
                print(f"  - No changes needed")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    return modernized_files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python modernize_docker_syntax.py <source_dir> [output_dir]")
        print("Example: python modernize_docker_syntax.py temp_converted modernized")
        sys.exit(1)
    
    source = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else source
    
    if not os.path.exists(source):
        print(f"Error: Source directory '{source}' does not exist")
        sys.exit(1)
    
    print(f"Modernizing Docker syntax in '{source}'...")
    if output != source:
        print(f"Output will be written to '{output}'")
    
    modernized = modernize_directory(source, output)
    
    print(f"\nModernization complete! Updated {len(modernized)} files.")
    
    if modernized:
        print("\nSummary of changes:")
        for file_path, changes in modernized:
            print(f"  {file_path}:")
            for change in changes:
                print(f"    - {change}")
