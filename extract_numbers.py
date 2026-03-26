#!/usr/bin/env python3
"""
Extract numerical patterns from steganography analysis output
"""

import re

def extract_numbers_from_steganography():
    """Extract numbers from the steganography analysis output"""
    
    # Read the steganography analysis file
    with open('steganography_analysis.ps1', 'r') as f:
        content = f.read()
    
    # Extract all numbers
    numbers = re.findall(r'\d+', content)
    
    # Filter for reasonable ranges (0-9999)
    filtered_numbers = [int(n) for n in numbers if 0 <= int(n) <= 9999]
    
    print(f"Extracted {len(filtered_numbers)} numbers from steganography analysis")
    
    # Save to clean format
    with open('extracted_numbers.txt', 'w') as f:
        for num in filtered_numbers:
            f.write(f"{num}\n")
    
    print("Numbers saved to 'extracted_numbers.txt'")
    return filtered_numbers

if __name__ == "__main__":
    extract_numbers_from_steganography()
