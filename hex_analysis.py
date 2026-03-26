#!/usr/bin/env python3
"""
Advanced Hex Analysis for Haian Image Steganography
"""

import re
import struct
from collections import Counter

class HexAnalyzer:
    def __init__(self, image_file):
        self.image_file = image_file
        self.hex_data = None
        self.extracted_data = []
        
    def load_image(self):
        """Load image and convert to hex"""
        with open(self.image_file, 'rb') as f:
            self.hex_data = f.read().hex()
        print(f"Loaded {len(self.hex_data)//2} bytes from {self.image_file}")
        
    def extract_lsb_data(self):
        """Extract data from least significant bits"""
        if not self.hex_data:
            self.load_image()
            
        # Convert hex to bytes
        byte_data = bytes.fromhex(self.hex_data)
        
        # Extract LSB from each byte
        lsb_bits = []
        for byte in byte_data:
            lsb_bits.append(str(byte & 1))
            
        # Convert bits to bytes (8 bits = 1 byte)
        extracted_bytes = []
        for i in range(0, len(lsb_bits), 8):
            if i + 8 <= len(lsb_bits):
                bits_str = ''.join(lsb_bits[i:i+8])
                extracted_bytes.append(int(bits_str, 2))
                
        # Filter for printable ASCII
        printable_chars = []
        for byte_val in extracted_bytes:
            if 32 <= byte_val <= 126:  # Printable ASCII range
                printable_chars.append(chr(byte_val))
                
        return ''.join(printable_chars)
        
    def find_hidden_strings(self):
        """Find hidden strings in hex data"""
        if not self.hex_data:
            self.load_image()
            
        # Look for common string patterns
        patterns = [
            b'http', b'ftp', b'mail', b'key', b'pass', b'flag',
            b'puzzle', b'challenge', b'hack', b'code', b'secret'
        ]
        
        found_strings = []
        byte_data = bytes.fromhex(self.hex_data)
        
        for pattern in patterns:
            if pattern in byte_data:
                found_strings.append(pattern.decode('ascii', errors='ignore'))
                
        return found_strings
        
    def analyze_byte_patterns(self):
        """Analyze byte patterns for anomalies"""
        if not self.hex_data:
            self.load_image()
            
        byte_data = bytes.fromhex(self.hex_data)
        
        # Count byte frequencies
        byte_freq = Counter(byte_data)
        
        # Look for unusual patterns
        patterns = {
            'null_bytes': byte_freq.get(0, 0),
            'ff_bytes': byte_freq.get(255, 0),
            'repeating_sequences': self._find_repeating_bytes(byte_data),
            'suspicious_clusters': self._find_suspicious_clusters(byte_data)
        }
        
        return patterns
        
    def _find_repeating_bytes(self, byte_data):
        """Find repeating byte sequences"""
        sequences = []
        
        # Look for 3+ repeated bytes
        for i in range(len(byte_data) - 2):
            if byte_data[i] == byte_data[i+1] == byte_data[i+2]:
                sequences.append((i, byte_data[i]))
                
        return sequences[:10]  # Return first 10
        
    def _find_suspicious_clusters(self, byte_data):
        """Find clusters of unusual byte values"""
        clusters = []
        
        # Look for clusters of high or low values
        for i in range(len(byte_data) - 10):
            cluster = byte_data[i:i+10]
            avg_val = sum(cluster) / len(cluster)
            
            if avg_val > 200 or avg_val < 55:  # Unusual averages
                clusters.append((i, avg_val))
                
        return clusters[:10]
        
    def extract_embedded_data(self):
        """Try to extract embedded data using various methods"""
        methods = {
            'lsb_extraction': self.extract_lsb_data(),
            'hidden_strings': self.find_hidden_strings(),
            'byte_patterns': self.analyze_byte_patterns()
        }
        
        return methods
        
    def generate_detailed_report(self):
        """Generate comprehensive analysis report"""
        methods = self.extract_embedded_data()
        
        report = []
        report.append("=" * 70)
        report.append("ADVANCED HEX ANALYSIS REPORT")
        report.append("=" * 70)
        
        # LSB extraction
        lsb_data = methods['lsb_extraction']
        if lsb_data:
            report.append("\nLSB EXTRACTION RESULTS:")
            report.append(f"Extracted {len(lsb_data)} characters")
            report.append("First 200 characters:")
            report.append(lsb_data[:200])
            
            # Look for patterns in LSB data
            numbers_in_lsb = re.findall(r'\d+', lsb_data)
            if numbers_in_lsb:
                report.append(f"\nNumbers found in LSB data: {len(numbers_in_lsb)}")
                report.append(f"Examples: {numbers_in_lsb[:20]}")
        else:
            report.append("\nLSB EXTRACTION: No meaningful data found")
            
        # Hidden strings
        hidden_strings = methods['hidden_strings']
        if hidden_strings:
            report.append("\nHIDDEN STRINGS FOUND:")
            for string in hidden_strings:
                report.append(f"  - {string}")
        else:
            report.append("\nHIDDEN STRINGS: None found")
            
        # Byte patterns
        patterns = methods['byte_patterns']
        report.append("\nBYTE PATTERN ANALYSIS:")
        report.append(f"Null bytes (0x00): {patterns['null_bytes']}")
        report.append(f"FF bytes (0xFF): {patterns['ff_bytes']}")
        
        if patterns['repeating_sequences']:
            report.append(f"\nRepeating sequences (first 10):")
            for pos, byte_val in patterns['repeating_sequences']:
                report.append(f"  Position {pos}: 0x{byte_val:02x} repeated")
                
        if patterns['suspicious_clusters']:
            report.append(f"\nSuspicious clusters (first 10):")
            for pos, avg_val in patterns['suspicious_clusters']:
                report.append(f"  Position {pos}: Average value {avg_val:.1f}")
                
        report.append("\n" + "=" * 70)
        report.append("END OF ANALYSIS")
        report.append("=" * 70)
        
        return "\n".join(report)

def main():
    """Main analysis function"""
    analyzer = HexAnalyzer('haian_image.jpg')
    
    # Generate detailed report
    report = analyzer.generate_detailed_report()
    
    # Save report
    with open('hex_analysis_report.txt', 'w') as f:
        f.write(report)
        
    print("Advanced hex analysis complete. Report saved to 'hex_analysis_report.txt'")
    print(report)

if __name__ == "__main__":
    main()
