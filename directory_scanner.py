#!/usr/bin/env python3
"""
Directory and Subdomain Scanner for haian.de
Looks for additional hidden content and directories
"""

import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import time

class HaianDirectoryScanner:
    def __init__(self):
        self.base_url = "http://haian.de"
        self.found_directories = []
        self.found_subdomains = []
        self.common_directories = [
            'admin', 'login', 'panel', 'dashboard', 'console', 'shell',
            'puzzle', 'challenge', 'flag', 'key', 'secret', 'hidden',
            'private', 'backup', 'old', 'archive', 'test', 'dev',
            'api', 'rest', 'graphql', 'webhook', 'upload', 'download',
            'files', 'data', 'db', 'database', 'config', 'settings',
            'haian', 'fabian', 'schuessler', '2011', 'matrix', 'simulation',
            'librandom', 'random', 'seed', 'crypto', 'hack', 'puzzlesolved'
        ]
        
        self.common_subdomains = [
            'admin', 'api', 'test', 'dev', 'staging', 'old', 'archive',
            'mail', 'ftp', 'vpn', 'secure', 'private', 'hidden',
            'haian', 'fabian', 'matrix', 'simulation', 'librandom'
        ]
        
        self.common_files = [
            'robots.txt', 'sitemap.xml', 'sitemap.html', '.htaccess',
            'config.php', 'config.ini', 'settings.conf', 'database.sql',
            'README', 'CHANGELOG', 'LICENSE', 'TODO', 'AUTHORS',
            'puzzle.txt', 'solution.txt', 'key.txt', 'flag.txt',
            'haian.txt', 'message.txt', 'secret.txt', 'hidden.txt'
        ]
        
    def check_directory(self, directory):
        """Check if a directory exists"""
        try:
            url = f"{self.base_url}/{directory}"
            response = requests.get(url, timeout=5, allow_redirects=False)
            
            if response.status_code in [200, 301, 302, 403]:
                self.found_directories.append({
                    'path': directory,
                    'status': response.status_code,
                    'content_length': len(response.content),
                    'server': response.headers.get('Server', 'Unknown')
                })
                print(f"Found directory: /{directory} (Status: {response.status_code})")
                return True
                
        except Exception as e:
            pass
            
        return False
        
    def check_subdomain(self, subdomain):
        """Check if a subdomain exists"""
        try:
            url = f"http://{subdomain}.haian.de"
            response = requests.get(url, timeout=5, allow_redirects=False)
            
            if response.status_code in [200, 301, 302, 403]:
                self.found_subdomains.append({
                    'subdomain': subdomain,
                    'status': response.status_code,
                    'content_length': len(response.content),
                    'server': response.headers.get('Server', 'Unknown')
                })
                print(f"Found subdomain: {subdomain}.haian.de (Status: {response.status_code})")
                return True
                
        except Exception as e:
            pass
            
        return False
        
    def check_file(self, filename):
        """Check if a file exists"""
        try:
            url = f"{self.base_url}/{filename}"
            response = requests.get(url, timeout=5, allow_redirects=False)
            
            if response.status_code == 200:
                print(f"Found file: /{filename} (Size: {len(response.content)} bytes)")
                
                # Save interesting files
                if any(keyword in filename.lower() for keyword in ['puzzle', 'solution', 'key', 'flag', 'secret', 'haian']):
                    with open(f"found_{filename}", 'wb') as f:
                        f.write(response.content)
                    print(f"Saved file as: found_{filename}")
                    
                return True
                
        except Exception as e:
            pass
            
        return False
        
    def scan_directories(self):
        """Scan for common directories"""
        print("Scanning directories...")
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.check_directory, directory) 
                      for directory in self.common_directories]
            
            for future in futures:
                future.result()
                
    def scan_subdomains(self):
        """Scan for common subdomains"""
        print("Scanning subdomains...")
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.check_subdomain, subdomain) 
                      for subdomain in self.common_subdomains]
            
            for future in futures:
                future.result()
                
    def scan_files(self):
        """Scan for common files"""
        print("Scanning files...")
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(self.check_file, filename) 
                      for filename in self.common_files]
            
            for future in futures:
                future.result()
                
    def generate_scan_report(self):
        """Generate comprehensive scan report"""
        report = []
        report.append("=" * 80)
        report.append("HAIAN.DE DIRECTORY AND SUBDOMAIN SCAN REPORT")
        report.append("=" * 80)
        
        # Directory findings
        if self.found_directories:
            report.append(f"\nFOUND DIRECTORIES: {len(self.found_directories)}")
            for directory in sorted(self.found_directories, key=lambda x: x['path']):
                report.append(f"  /{directory['path']} - Status: {directory['status']} - Size: {directory['content_length']} bytes")
                if directory['server'] != 'Unknown':
                    report.append(f"    Server: {directory['server']}")
        else:
            report.append("\nFOUND DIRECTORIES: None")
            
        # Subdomain findings
        if self.found_subdomains:
            report.append(f"\nFOUND SUBDOMAINS: {len(self.found_subdomains)}")
            for subdomain in sorted(self.found_subdomains, key=lambda x: x['subdomain']):
                report.append(f"  {subdomain['subdomain']}.haian.de - Status: {subdomain['status']} - Size: {subdomain['content_length']} bytes")
                if subdomain['server'] != 'Unknown':
                    report.append(f"    Server: {subdomain['server']}")
        else:
            report.append("\nFOUND SUBDOMAINS: None")
            
        # Assessment
        report.append("\nASSESSMENT:")
        
        total_findings = len(self.found_directories) + len(self.found_subdomains)
        
        if total_findings == 0:
            report.append("- No hidden directories or subdomains found")
            report.append("- Website appears to be a simple memorial site")
            risk_level = "LOW"
        elif total_findings <= 3:
            report.append(f"- Found {total_findings} hidden resources")
            report.append("- Some hidden content may exist")
            risk_level = "MEDIUM"
        else:
            report.append(f"- Found {total_findings} hidden resources")
            report.append("- Significant hidden infrastructure detected")
            risk_level = "HIGH"
            
        report.append(f"\nRISK LEVEL: {risk_level}")
        
        # Recommendations
        if risk_level == "HIGH":
            report.append("\nRECOMMENDATIONS:")
            report.append("- Investigate found directories for additional puzzle content")
            report.append("- Check subdomains for related services or data")
            report.append("- Monitor for changes or new content")
        elif risk_level == "MEDIUM":
            report.append("\nRECOMMENDATIONS:")
            report.append("- Quick investigation of found resources")
            report.append("- Consider periodic monitoring")
        else:
            report.append("\nRECOMMENDATIONS:")
            report.append("- Focus investigation on other leads")
            
        report.append("\n" + "=" * 80)
        report.append("END OF SCAN REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)
        
    def run_full_scan(self):
        """Run complete directory and subdomain scan"""
        print("Starting comprehensive haian.de scan...")
        print(f"Target: {self.base_url}")
        print(f"Directories to check: {len(self.common_directories)}")
        print(f"Subdomains to check: {len(self.common_subdomains)}")
        print(f"Files to check: {len(self.common_files)}")
        print("-" * 60)
        
        start_time = time.time()
        
        # Run scans
        self.scan_directories()
        self.scan_subdomains()
        self.scan_files()
        
        end_time = time.time()
        
        print("-" * 60)
        print(f"Scan completed in {end_time - start_time:.2f} seconds")
        print(f"Found directories: {len(self.found_directories)}")
        print(f"Found subdomains: {len(self.found_subdomains)}")
        
        # Generate report
        report = self.generate_scan_report()
        
        # Save report
        with open('directory_scan_report.txt', 'w') as f:
            f.write(report)
            
        print("Scan report saved to 'directory_scan_report.txt'")
        print(report)

def main():
    """Main scan function"""
    scanner = HaianDirectoryScanner()
    scanner.run_full_scan()

if __name__ == "__main__":
    main()
