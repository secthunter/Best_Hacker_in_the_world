#!/usr/bin/env python3
"""
Puzzle File Analyzer
Analyzes the PUZZLE_SOLVED.txt file from librandom repository
"""

import requests
import re
import base64
from datetime import datetime

class PuzzleFileAnalyzer:
    def __init__(self):
        self.repo_owner = "vibehacker88"
        self.repo_name = "librandom"
        self.base_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        self.puzzle_content = ""
        
    def fetch_puzzle_file(self):
        """Fetch the PUZZLE_SOLVED.txt file content"""
        try:
            # Get file info
            response = requests.get(f"{self.base_url}/contents/PUZZLE_SOLVED.txt")
            if response.status_code == 200:
                file_data = response.json()
                
                # Decode content (GitHub API returns base64)
                content = file_data.get('content', '')
                if content:
                    self.puzzle_content = base64.b64decode(content).decode('utf-8')
                    print("Successfully fetched PUZZLE_SOLVED.txt")
                    return True
            else:
                print(f"Failed to fetch puzzle file: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Error fetching puzzle file: {e}")
            return False
            
    def analyze_puzzle_content(self):
        """Analyze the puzzle file content for clues"""
        if not self.puzzle_content:
            return {}
            
        analysis = {
            'file_length': len(self.puzzle_content),
            'line_count': len(self.puzzle_content.splitlines()),
            'word_count': len(self.puzzle_content.split()),
            'numbers_found': re.findall(r'\d+', self.puzzle_content),
            'urls_found': re.findall(r'https?://[^\s]+', self.puzzle_content),
            'email_addresses': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.puzzle_content),
            'hex_patterns': re.findall(r'[0-9A-Fa-f]{8,}', self.puzzle_content),
            'base64_patterns': re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', self.puzzle_content),
            'keywords': self._extract_keywords(),
            'suspicious_patterns': self._find_suspicious_patterns()
        }
        
        return analysis
        
    def _extract_keywords(self):
        """Extract relevant keywords from puzzle content"""
        haian_keywords = [
            'haian', 'fabian', 'schüßler', 'schuessler', 'hacker', 'puzzle',
            '2011', 'death', 'fake', 'disappear', 'random', 'seed', 'key',
            'cologne', 'germany', 'librandom', 'challenge', 'solve', 'solution'
        ]
        
        found_keywords = []
        content_lower = self.puzzle_content.lower()
        
        for keyword in haian_keywords:
            if keyword in content_lower:
                found_keywords.append(keyword)
                
        return found_keywords
        
    def _find_suspicious_patterns(self):
        """Find suspicious patterns that might be encoded messages"""
        patterns = []
        
        # Look for coordinate-like patterns
        coord_pattern = re.findall(r'\b\d{1,3}\.\d{1,6},\s*-?\d{1,3}\.\d{1,6}\b', self.puzzle_content)
        if coord_pattern:
            patterns.append({
                'type': 'coordinates',
                'matches': coord_pattern
            })
            
        # Look for date patterns
        date_pattern = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', self.puzzle_content)
        if date_pattern:
            patterns.append({
                'type': 'dates',
                'matches': date_pattern
            })
            
        # Look for phone number patterns
        phone_pattern = re.findall(r'\b\d{3}-\d{3}-\d{4}\b|\b\+\d{1,3}\s\d{1,14}\b', self.puzzle_content)
        if phone_pattern:
            patterns.append({
                'type': 'phone_numbers',
                'matches': phone_pattern
            })
            
        # Look for hash-like patterns
        hash_pattern = re.findall(r'\b[a-f0-9]{32,64}\b', self.puzzle_content.lower())
        if hash_pattern:
            patterns.append({
                'type': 'hashes',
                'matches': hash_pattern
            })
            
        return patterns
        
    def decode_potential_encodings(self):
        """Try to decode potential encoded content"""
        encodings = {}
        
        # Try base64 decoding on suspicious strings
        base64_candidates = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', self.puzzle_content)
        for i, candidate in enumerate(base64_candidates):
            try:
                decoded = base64.b64decode(candidate).decode('utf-8')
                if decoded.isprintable():
                    encodings[f'base64_{i}'] = decoded
            except:
                pass
                
        # Try hex decoding
        hex_candidates = re.findall(r'[0-9A-Fa-f]{8,}', self.puzzle_content)
        for i, candidate in enumerate(hex_candidates):
            try:
                if len(candidate) % 2 == 0:  # Even length for hex
                    decoded = bytes.fromhex(candidate).decode('utf-8', errors='ignore')
                    if decoded.isprintable() and len(decoded) > 3:
                        encodings[f'hex_{i}'] = decoded
            except:
                pass
                
        return encodings
        
    def analyze_numerical_sequences(self):
        """Analyze numerical sequences for mathematical patterns"""
        numbers = re.findall(r'\d+', self.puzzle_content)
        if not numbers:
            return {}
            
        num_list = [int(n) for n in numbers if len(n) <= 6]  # Filter reasonable length
        
        analysis = {
            'total_numbers': len(num_list),
            'unique_numbers': len(set(num_list)),
            'number_frequency': {},
            'mathematical_patterns': []
        }
        
        # Count frequency
        from collections import Counter
        freq = Counter(num_list)
        analysis['number_frequency'] = dict(freq.most_common(10))
        
        # Check for mathematical patterns
        if len(num_list) >= 3:
            # Check for arithmetic sequences
            for i in range(len(num_list) - 2):
                diff1 = num_list[i+1] - num_list[i]
                diff2 = num_list[i+2] - num_list[i+1]
                if diff1 == diff2 and diff1 != 0:
                    analysis['mathematical_patterns'].append({
                        'type': 'arithmetic_sequence',
                        'start': i,
                        'common_difference': diff1,
                        'sequence': num_list[i:i+3]
                    })
                    
            # Check for geometric sequences
            for i in range(len(num_list) - 2):
                if num_list[i] != 0 and num_list[i+1] != 0:
                    ratio1 = num_list[i+1] / num_list[i]
                    ratio2 = num_list[i+2] / num_list[i+1]
                    if abs(ratio1 - ratio2) < 0.001 and ratio1 != 1:
                        analysis['mathematical_patterns'].append({
                            'type': 'geometric_sequence',
                            'start': i,
                            'common_ratio': ratio1,
                            'sequence': num_list[i:i+3]
                        })
                        
        return analysis
        
    def generate_puzzle_analysis_report(self):
        """Generate comprehensive puzzle file analysis report"""
        if not self.fetch_puzzle_file():
            return "Failed to fetch puzzle file"
            
        # Perform all analyses
        content_analysis = self.analyze_puzzle_content()
        encodings = self.decode_potential_encodings()
        numerical_analysis = self.analyze_numerical_sequences()
        
        # Generate report
        report = []
        report.append("=" * 80)
        report.append("PUZZLE FILE ANALYSIS REPORT")
        report.append("=" * 80)
        
        # Basic content info
        report.append("\nBASIC CONTENT ANALYSIS:")
        report.append(f"File length: {content_analysis['file_length']} characters")
        report.append(f"Line count: {content_analysis['line_count']}")
        report.append(f"Word count: {content_analysis['word_count']}")
        
        # Keywords found
        if content_analysis['keywords']:
            report.append("\nHAIAN-RELATED KEYWORDS FOUND:")
            for keyword in content_analysis['keywords']:
                report.append(f"  - {keyword}")
                
        # Numbers found
        if content_analysis['numbers_found']:
            report.append(f"\nNUMBERS FOUND: {len(content_analysis['numbers_found'])}")
            report.append("First 20 numbers:")
            for num in content_analysis['numbers_found'][:20]:
                report.append(f"  {num}")
                
        # URLs found
        if content_analysis['urls_found']:
            report.append("\nURLS FOUND:")
            for url in content_analysis['urls_found']:
                report.append(f"  {url}")
                
        # Email addresses
        if content_analysis['email_addresses']:
            report.append("\nEMAIL ADDRESSES FOUND:")
            for email in content_analysis['email_addresses']:
                report.append(f"  {email}")
                
        # Suspicious patterns
        if content_analysis['suspicious_patterns']:
            report.append("\nSUSPICIOUS PATTERNS:")
            for pattern in content_analysis['suspicious_patterns']:
                report.append(f"  Type: {pattern['type']}")
                for match in pattern['matches'][:5]:  # First 5 matches
                    report.append(f"    {match}")
                    
        # Decoded content
        if encodings:
            report.append("\nDECODED CONTENT:")
            for key, value in encodings.items():
                report.append(f"  {key}: {value}")
                
        # Numerical analysis
        if numerical_analysis:
            report.append("\nNUMERICAL SEQUENCE ANALYSIS:")
            report.append(f"Total numbers: {numerical_analysis['total_numbers']}")
            report.append(f"Unique numbers: {numerical_analysis['unique_numbers']}")
            
            if numerical_analysis['number_frequency']:
                report.append("\nMost frequent numbers:")
                for num, count in list(numerical_analysis['number_frequency'].items())[:10]:
                    report.append(f"  {num}: {count} times")
                    
            if numerical_analysis['mathematical_patterns']:
                report.append("\nMathematical patterns found:")
                for pattern in numerical_analysis['mathematical_patterns']:
                    report.append(f"  {pattern['type']}: {pattern['sequence']}")
                    
        # Full content (if not too long)
        if len(self.puzzle_content) < 2000:
            report.append("\nFULL PUZZLE CONTENT:")
            report.append("-" * 40)
            report.append(self.puzzle_content)
            report.append("-" * 40)
        else:
            report.append("\nFIRST 1000 CHARACTERS OF PUZZLE CONTENT:")
            report.append("-" * 40)
            report.append(self.puzzle_content[:1000])
            report.append("...")
            report.append("-" * 40)
            
        # Assessment
        report.append("\nASSESSMENT:")
        
        suspicion_score = 0
        
        if content_analysis['keywords']:
            suspicion_score += len(content_analysis['keywords']) * 2
            report.append(f"- Contains {len(content_analysis['keywords'])} Haian-related keywords")
            
        if content_analysis['suspicious_patterns']:
            suspicion_score += len(content_analysis['suspicious_patterns']) * 3
            report.append(f"- Contains {len(content_analysis['suspicious_patterns'])} suspicious patterns")
            
        if encodings:
            suspicion_score += len(encodings) * 2
            report.append(f"- {len(encodings)} encoded strings found")
            
        if suspicion_score >= 10:
            threat_level = "HIGH"
        elif suspicion_score >= 5:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
            
        report.append(f"\nSUSPICION SCORE: {suspicion_score}")
        report.append(f"THREAT LEVEL: {threat_level}")
        
        if threat_level in ["HIGH", "MEDIUM"]:
            report.append("\nRECOMMENDATION: This file likely contains important puzzle clues")
        else:
            report.append("\nRECOMMENDATION: File appears to be legitimate")
            
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    """Main analysis function"""
    analyzer = PuzzleFileAnalyzer()
    
    # Generate analysis report
    report = analyzer.generate_puzzle_analysis_report()
    
    # Save report
    with open('puzzle_file_analysis_report.txt', 'w') as f:
        f.write(report)
        
    print("Puzzle file analysis complete. Report saved to 'puzzle_file_analysis_report.txt'")
    print(report)

if __name__ == "__main__":
    main()
