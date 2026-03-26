#!/usr/bin/env python3
"""
Advanced Numerical Pattern Analysis for Haian Investigation
Analyzes extracted numerical sequences from steganographic content
"""

import re
import statistics
from collections import Counter, defaultdict
import math
from typing import List, Dict, Tuple, Any

class NumericalPatternAnalyzer:
    def __init__(self):
        self.extracted_numbers = []
        self.patterns = {}
        self.crypto_candidates = []
        
    def load_numbers_from_file(self, filename: str) -> None:
        """Load numerical data from steganography analysis output"""
        try:
            with open(filename, 'r') as f:
                content = f.read()
                # Extract all numbers from the file
                numbers = re.findall(r'\d+', content)
                self.extracted_numbers = [int(n) for n in numbers if len(n) <= 6]  # Filter reasonable length
                print(f"Loaded {len(self.extracted_numbers)} numbers")
        except FileNotFoundError:
            print(f"File {filename} not found")
            
    def analyze_frequency_distribution(self) -> Dict[str, Any]:
        """Analyze frequency distribution of numbers"""
        if not self.extracted_numbers:
            return {}
            
        freq = Counter(self.extracted_numbers)
        
        analysis = {
            'total_numbers': len(self.extracted_numbers),
            'unique_numbers': len(freq),
            'most_common': freq.most_common(10),
            'mean': statistics.mean(self.extracted_numbers),
            'median': statistics.median(self.extracted_numbers),
            'std_dev': statistics.stdev(self.extracted_numbers) if len(self.extracted_numbers) > 1 else 0,
            'min': min(self.extracted_numbers),
            'max': max(self.extracted_numbers)
        }
        
        return analysis
        
    def detect_mathematical_patterns(self) -> List[Dict[str, Any]]:
        """Detect mathematical patterns in number sequences"""
        patterns = []
        
        # Check for prime numbers
        primes = [n for n in set(self.extracted_numbers) if self._is_prime(n)]
        if len(primes) > len(set(self.extracted_numbers)) * 0.1:  # More than 10% primes
            patterns.append({
                'type': 'prime_concentration',
                'count': len(primes),
                'numbers': primes[:20],  # First 20 primes
                'significance': 'High'
            })
            
        # Check for Fibonacci sequence
        fib_patterns = self._find_fibonacci_patterns()
        if fib_patterns:
            patterns.extend(fib_patterns)
            
        # Check for powers of 2
        powers_of_2 = [n for n in set(self.extracted_numbers) if self._is_power_of_2(n)]
        if powers_of_2:
            patterns.append({
                'type': 'powers_of_2',
                'count': len(powers_of_2),
                'numbers': powers_of_2,
                'significance': 'Medium'
            })
            
        # Check for repeating sequences
        repeating = self._find_repeating_sequences()
        if repeating:
            patterns.extend(repeating)
            
        return patterns
        
    def analyze_cryptographic_potential(self) -> List[Dict[str, Any]]:
        """Analyze numbers for cryptographic significance"""
        crypto_candidates = []
        
        # Check for common key lengths
        common_key_lengths = [64, 128, 192, 256, 512, 1024, 2048]
        key_matches = [n for n in self.extracted_numbers if n in common_key_lengths]
        if key_matches:
            crypto_candidates.append({
                'type': 'key_length_candidates',
                'numbers': key_matches,
                'significance': 'High'
            })
            
        # Check for ASCII ranges (32-126)
        ascii_candidates = [n for n in self.extracted_numbers if 32 <= n <= 126]
        if ascii_candidates:
            crypto_candidates.append({
                'type': 'ascii_candidates',
                'count': len(ascii_candidates),
                'numbers': ascii_candidates[:50],
                'significance': 'Medium'
            })
            
        # Check for modulo patterns (common in crypto)
        modulo_patterns = self._analyze_modulo_patterns()
        if modulo_patterns:
            crypto_candidates.extend(modulo_patterns)
            
        return crypto_candidates
        
    def detect_coordinate_patterns(self) -> List[Dict[str, Any]]:
        """Detect potential geographic coordinates"""
        coordinates = []
        
        # Look for latitude/longitude pairs
        for i in range(len(self.extracted_numbers) - 1):
            lat, lon = self.extracted_numbers[i], self.extracted_numbers[i + 1]
            
            # Check if could be coordinates (simplified)
            if (-90 <= lat <= 90) and (-180 <= lon <= 180):
                coordinates.append({
                    'latitude': lat,
                    'longitude': lon,
                    'index': i
                })
                
        return coordinates
        
    def _is_prime(self, n: int) -> bool:
        """Check if number is prime"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
        
    def _is_power_of_2(self, n: int) -> bool:
        """Check if number is power of 2"""
        return n > 0 and (n & (n - 1)) == 0
        
    def _find_fibonacci_patterns(self) -> List[Dict[str, Any]]:
        """Find Fibonacci-like sequences"""
        patterns = []
        fib_set = set()
        a, b = 0, 1
        while b < 1000:  # Reasonable upper limit
            fib_set.add(b)
            a, b = b, a + b
            
        # Check for Fibonacci numbers in our data
        fib_matches = [n for n in self.extracted_numbers if n in fib_set]
        if len(fib_matches) > 5:  # Threshold for significance
            patterns.append({
                'type': 'fibonacci_pattern',
                'count': len(fib_matches),
                'numbers': fib_matches,
                'significance': 'Medium'
            })
            
        return patterns
        
    def _find_repeating_sequences(self) -> List[Dict[str, Any]]:
        """Find repeating number sequences"""
        patterns = []
        sequence_counts = defaultdict(int)
        
        # Look for sequences of 3-5 numbers
        for length in range(3, 6):
            for i in range(len(self.extracted_numbers) - length + 1):
                seq = tuple(self.extracted_numbers[i:i+length])
                sequence_counts[seq] += 1
                
        # Find sequences that repeat
        for seq, count in sequence_counts.items():
            if count >= 3:  # Repeats at least 3 times
                patterns.append({
                    'type': 'repeating_sequence',
                    'sequence': list(seq),
                    'count': count,
                    'significance': 'High' if count >= 5 else 'Medium'
                })
                
        return patterns
        
    def _analyze_modulo_patterns(self) -> List[Dict[str, Any]]:
        """Analyze numbers for modulo patterns common in crypto"""
        patterns = []
        
        # Common moduli in cryptography
        common_moduli = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        
        for mod in common_moduli:
            residues = [n % mod for n in self.extracted_numbers]
            residue_counts = Counter(residues)
            
            # Check for non-uniform distribution (might indicate pattern)
            if len(residue_counts) < mod:  # Not all residues present
                patterns.append({
                    'type': 'modulo_pattern',
                    'modulus': mod,
                    'residue_distribution': dict(residue_counts),
                    'significance': 'Low'
                })
                
        return patterns
        
    def generate_report(self) -> str:
        """Generate comprehensive analysis report"""
        report = []
        report.append("=" * 60)
        report.append("NUMERICAL PATTERN ANALYSIS REPORT")
        report.append("=" * 60)
        
        # Frequency analysis
        freq_analysis = self.analyze_frequency_distribution()
        if freq_analysis:
            report.append("\nFREQUENCY ANALYSIS:")
            report.append(f"Total numbers: {freq_analysis['total_numbers']}")
            report.append(f"Unique numbers: {freq_analysis['unique_numbers']}")
            report.append(f"Mean: {freq_analysis['mean']:.2f}")
            report.append(f"Median: {freq_analysis['median']}")
            report.append(f"Range: {freq_analysis['min']} - {freq_analysis['max']}")
            
            report.append("\nTop 10 most common numbers:")
            for num, count in freq_analysis['most_common']:
                report.append(f"  {num}: {count} occurrences")
                
        # Mathematical patterns
        math_patterns = self.detect_mathematical_patterns()
        if math_patterns:
            report.append("\nMATHEMATICAL PATTERNS:")
            for pattern in math_patterns:
                report.append(f"Type: {pattern['type']}")
                report.append(f"Significance: {pattern['significance']}")
                report.append(f"Count: {pattern['count']}")
                if 'numbers' in pattern:
                    report.append(f"Examples: {pattern['numbers'][:10]}")
                report.append("")
                
        # Cryptographic potential
        crypto_patterns = self.analyze_cryptographic_potential()
        if crypto_patterns:
            report.append("CRYPTOGRAPHIC POTENTIAL:")
            for pattern in crypto_patterns:
                report.append(f"Type: {pattern['type']}")
                report.append(f"Significance: {pattern['significance']}")
                if 'count' in pattern:
                    report.append(f"Count: {pattern['count']}")
                if 'numbers' in pattern:
                    report.append(f"Examples: {pattern['numbers'][:10]}")
                report.append("")
                
        # Coordinate patterns
        coordinates = self.detect_coordinate_patterns()
        if coordinates:
            report.append("POTENTIAL COORDINATES:")
            for coord in coordinates[:10]:  # First 10
                report.append(f"  {coord['latitude']}, {coord['longitude']} (index: {coord['index']})")
                
        report.append("\n" + "=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)
        
        return "\n".join(report)

def main():
    """Main analysis function"""
    analyzer = NumericalPatternAnalyzer()
    
    # Load numbers from steganography analysis
    analyzer.load_numbers_from_file('steganography_analysis.ps1')
    
    # Generate and save report
    report = analyzer.generate_report()
    
    with open('numerical_analysis_report.txt', 'w') as f:
        f.write(report)
        
    print("Numerical analysis complete. Report saved to 'numerical_analysis_report.txt'")
    print(report)

if __name__ == "__main__":
    main()
