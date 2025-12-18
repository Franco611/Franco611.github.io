#!/usr/bin/env python3
"""
GTF File Processor
This script processes GTF files by extracting gene_id from column 9 and appending
gene_name with the same value to the end of column 9.

Usage:
    python process_gtf.py input.gtf output.gtf
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


def process_gtf_line(line):
    """
    Process a single GTF line by appending gene_name to column 9.
    
    Args:
        line: A single line from the GTF file
        
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
        # Append gene_name with the gene_id value to the end of attributes
        # Make sure attributes ends with proper formatting
        if not attributes.endswith(';'):
            attributes += ';'
        attributes += f' gene_name "{gene_id}";'
        fields[8] = attributes
    
    # Reconstruct the line
    return '\t'.join(fields) + '\n'


def process_gtf_file(input_file, output_file):
    """
    Process entire GTF file.
    
    Args:
        input_file: Path to input GTF file
        output_file: Path to output GTF file
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                processed_line = process_gtf_line(line)
                outfile.write(processed_line)
        print(f"Successfully processed {input_file} -> {output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) != 3:
        print("Usage: python process_gtf.py input.gtf output.gtf")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    process_gtf_file(input_file, output_file)


if __name__ == "__main__":
    main()
