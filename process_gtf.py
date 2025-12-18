#!/usr/bin/env python3
"""
GTF File Processor
This script processes GTF files by extracting gene_id from column 9 and appending
gene_name with the same value to the end of column 9.

Usage:
    python process_gtf.py input.gtf output.gtf [--skip-if-exists]

Options:
    --skip-if-exists    Skip adding gene_name if it already exists in the attributes
"""

import sys
import re


def extract_gene_id(attributes):
    """
    Extract gene_id value from GTF attributes string.
    
    Args:
        attributes: String containing GTF attributes (column 9)
        
    Returns:
        The gene_id value if found, None otherwise
    """
    match = re.search(r'gene_id\s+"([^"]+)"', attributes)
    if match:
        return match.group(1)
    return None


def has_gene_name(attributes):
    """
    Check if gene_name attribute already exists in the attributes string.
    
    Args:
        attributes: String containing GTF attributes (column 9)
        
    Returns:
        True if gene_name exists, False otherwise
    """
    return bool(re.search(r'gene_name\s+"[^"]+"', attributes))


def process_gtf_line(line, skip_if_exists=False):
    """
    Process a single GTF line by appending gene_name to column 9.
    
    Args:
        line: A single line from the GTF file
        skip_if_exists: If True, skip adding gene_name if it already exists
        
    Returns:
        Modified line with gene_name appended
    """
    # Skip empty lines and comments
    if not line.strip() or line.startswith('#'):
        return line
    
    # Split the line into fields (GTF is tab-separated)
    fields = line.rstrip('\n').split('\t')
    
    # GTF files should have 9 columns
    if len(fields) < 9:
        return line
    
    # Extract gene_id from the 9th column (index 8)
    attributes = fields[8]
    gene_id = extract_gene_id(attributes)
    
    if gene_id:
        # Check if we should skip if gene_name already exists
        if skip_if_exists and has_gene_name(attributes):
            return line
            
        # Append gene_name with the gene_id value to the end of attributes
        # Note: This will add gene_name even if it already exists in the middle,
        # as per the original requirement to "copy to the end"
        if not attributes.endswith(';'):
            attributes += ';'
        attributes += f' gene_name "{gene_id}";'
        fields[8] = attributes
    
    # Reconstruct the line
    return '\t'.join(fields) + '\n'


def process_gtf_file(input_file, output_file, skip_if_exists=False):
    """
    Process entire GTF file.
    
    Args:
        input_file: Path to input GTF file
        output_file: Path to output GTF file
        skip_if_exists: If True, skip adding gene_name if it already exists
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                processed_line = process_gtf_line(line, skip_if_exists)
                outfile.write(processed_line)
        print(f"Successfully processed {input_file} -> {output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when accessing files.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file. Please ensure it's a valid UTF-8 text file.")
        sys.exit(1)
    except OSError as e:
        print(f"Error: OS error occurred: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments."""
    skip_if_exists = False
    args = sys.argv[1:]
    
    # Check for --skip-if-exists flag
    if '--skip-if-exists' in args:
        skip_if_exists = True
        args.remove('--skip-if-exists')
    
    if len(args) != 2:
        print("Usage: python process_gtf.py input.gtf output.gtf [--skip-if-exists]")
        print("\nOptions:")
        print("  --skip-if-exists    Skip adding gene_name if it already exists")
        sys.exit(1)
    
    input_file = args[0]
    output_file = args[1]
    
    process_gtf_file(input_file, output_file, skip_if_exists)


if __name__ == "__main__":
    main()
