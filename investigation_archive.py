#!/usr/bin/env python3
"""
Investigation Archive Tool
Creates comprehensive archive of all investigation materials
"""

import os
import json
import hashlib
import shutil
from datetime import datetime
import zipfile

class InvestigationArchiver:
    def __init__(self):
        self.investigation_dir = "."
        self.archive_name = f"haian_investigation_archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.manifest = {
            'archive_created': datetime.now().isoformat(),
            'investigation_name': 'Haian Case - Deep Forensic Research',
            'case_number': 'HAIAN-2011-2026-001',
            'classification': 'TOP SECRET',
            'files': [],
            'total_files': 0,
            'total_size': 0,
            'evidence_integrity': {}
        }
        
    def calculate_file_hash(self, filepath):
        """Calculate SHA-256 hash of file"""
        hash_sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
        
    def get_file_info(self, filepath):
        """Get comprehensive file information"""
        try:
            stat = os.stat(filepath)
            return {
                'path': os.path.relpath(filepath, self.investigation_dir),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'hash': self.calculate_file_hash(filepath),
                'type': 'file' if os.path.isfile(filepath) else 'directory'
            }
        except Exception as e:
            return {
                'path': os.path.relpath(filepath, self.investigation_dir),
                'error': str(e),
                'type': 'error'
            }
            
    def collect_evidence_files(self):
        """Collect all investigation-related files"""
        evidence_files = []
        
        # Define file patterns to include
        include_patterns = [
            '*.md', '*.txt', '*.py', '*.html', '*.jpg', '*.jpeg',
            '*.png', '*.gif', '*.ps1', '*.json', '*.log'
        ]
        
        # Define important files to always include
        important_files = [
            'README.md',
            'AGENTS.md',
            'haian_de_source.html',
            'haian_image.jpg',
            'comprehensive_investigation_summary.md'
        ]
        
        # Walk through directory
        for root, dirs, files in os.walk(self.investigation_dir):
            # Skip hidden directories and common non-evidence
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for file in files:
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, self.investigation_dir)
                
                # Skip hidden files and cache files
                if file.startswith('.') or file.endswith('.pyc'):
                    continue
                    
                # Include all important files
                if file in important_files:
                    evidence_files.append(filepath)
                    continue
                    
                # Include files matching our patterns
                for pattern in include_patterns:
                    if file.endswith(pattern[1:]):  # Remove * from pattern
                        evidence_files.append(filepath)
                        break
                        
        return evidence_files
        
    def create_manifest(self):
        """Create comprehensive evidence manifest"""
        evidence_files = self.collect_evidence_files()
        
        total_size = 0
        file_count = 0
        
        for filepath in evidence_files:
            file_info = self.get_file_info(filepath)
            self.manifest['files'].append(file_info)
            
            if file_info['type'] == 'file':
                total_size += file_info['size']
                file_count += 1
                
                # Store hash for integrity checking
                self.manifest['evidence_integrity'][file_info['path']] = file_info['hash']
                
        self.manifest['total_files'] = file_count
        self.manifest['total_size'] = total_size
        
        return evidence_files
        
    def create_evidence_summary(self):
        """Create evidence summary document"""
        summary = []
        summary.append("# EVIDENCE SUMMARY")
        summary.append(f"Case: {self.manifest['investigation_name']}")
        summary.append(f"Case Number: {self.manifest['case_number']}")
        summary.append(f"Classification: {self.manifest['classification']}")
        summary.append(f"Archive Created: {self.manifest['archive_created']}")
        summary.append("")
        
        summary.append("## EVIDENCE STATISTICS")
        summary.append(f"Total Files: {self.manifest['total_files']}")
        summary.append(f"Total Size: {self.manifest['total_size']:,} bytes")
        summary.append(f"Total Size (MB): {self.manifest['total_size'] / 1024 / 1024:.2f} MB")
        summary.append("")
        
        # Categorize files by type
        file_categories = {
            'Documentation': [],
            'Analysis Scripts': [],
            'Evidence Files': [],
            'Reports': [],
            'Other': []
        }
        
        for file_info in self.manifest['files']:
            if file_info['type'] != 'file':
                continue
                
            filepath = file_info['path']
            
            if filepath.endswith('.md'):
                file_categories['Documentation'].append(file_info)
            elif filepath.endswith('.py'):
                file_categories['Analysis Scripts'].append(file_info)
            elif filepath.endswith(('.jpg', '.jpeg', '.png', '.html')):
                file_categories['Evidence Files'].append(file_info)
            elif filepath.endswith(('.txt', '.log')):
                file_categories['Reports'].append(file_info)
            else:
                file_categories['Other'].append(file_info)
                
        for category, files in file_categories.items():
            if files:
                summary.append(f"## {category} ({len(files)} files)")
                for file_info in sorted(files, key=lambda x: x['path']):
                    summary.append(f"- {file_info['path']} ({file_info['size']:,} bytes)")
                    summary.append(f"  Hash: {file_info['hash']}")
                summary.append("")
                
        # Critical evidence files
        critical_files = [
            'comprehensive_investigation_summary.md',
            'haian_image.jpg',
            'haian_de_source.html',
            'AGENTS.md',
            'README.md'
        ]
        
        summary.append("## CRITICAL EVIDENCE FILES")
        for critical_file in critical_files:
            for file_info in self.manifest['files']:
                if file_info['path'] == critical_file:
                    summary.append(f"### {file_info['path']}")
                    summary.append(f"- Size: {file_info['size']:,} bytes")
                    summary.append(f"- Hash: {file_info['hash']}")
                    summary.append(f"- Modified: {file_info['modified']}")
                    summary.append("")
                    break
                    
        # Chain of custody
        summary.append("## CHAIN OF CUSTODY")
        summary.append(f"- Evidence collected: {datetime.now().isoformat()}")
        summary.append(f"- Collector: Automated Investigation System")
        summary.append(f"- Archive created: {self.manifest['archive_created']}")
        summary.append(f"- Archive method: SHA-256 integrity verification")
        summary.append("")
        
        summary.append("## INVESTIGATION STATUS")
        summary.append("- Primary investigation: COMPLETE")
        summary.append("- Evidence collection: COMPLETE")
        summary.append("- Initial analysis: COMPLETE")
        summary.append("- Follow-up recommended: YES (see comprehensive_investigation_summary.md)")
        summary.append("")
        
        summary.append("## SECURITY NOTES")
        summary.append("- All files have been hashed for integrity verification")
        summary.append("- Archive should be stored in secure, access-controlled environment")
        summary.append("- Any modification of files will break hash verification")
        summary.append("- Consider encrypting archive for additional security")
        summary.append("")
        
        return "\n".join(summary)
        
    def create_zip_archive(self):
        """Create ZIP archive of all evidence"""
        evidence_files = self.collect_evidence_files()
        
        with zipfile.ZipFile(f"{self.archive_name}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filepath in evidence_files:
                arcname = os.path.relpath(filepath, self.investigation_dir)
                zipf.write(filepath, arcname)
                
        return f"{self.archive_name}.zip"
        
    def verify_archive_integrity(self, archive_path):
        """Verify that archive contents match original hashes"""
        verification_results = {
            'verified_files': 0,
            'failed_files': 0,
            'errors': []
        }
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                for file_info in zipf.infolist():
                    if file_info.filename.endswith('/'):
                        continue  # Skip directories
                        
                    # Extract file to temp location and verify hash
                    try:
                        with zipf.open(file_info) as f:
                            content = f.read()
                            
                        # Calculate hash of archived content
                        file_hash = hashlib.sha256(content).hexdigest()
                        
                        # Compare with original hash
                        original_hash = self.manifest['evidence_integrity'].get(file_info.filename)
                        
                        if original_hash == file_hash:
                            verification_results['verified_files'] += 1
                        else:
                            verification_results['failed_files'] += 1
                            verification_results['errors'].append(
                                f"Hash mismatch for {file_info.filename}: "
                                f"expected {original_hash}, got {file_hash}"
                            )
                            
                    except Exception as e:
                        verification_results['errors'].append(f"Error verifying {file_info.filename}: {e}")
                        
        except Exception as e:
            verification_results['errors'].append(f"Error opening archive: {e}")
            
        return verification_results
        
    def create_complete_archive(self):
        """Create complete investigation archive"""
        print("Creating investigation archive...")
        print(f"Archive name: {self.archive_name}")
        
        # Create manifest
        print("Creating evidence manifest...")
        evidence_files = self.create_manifest()
        
        # Create evidence summary
        print("Creating evidence summary...")
        summary = self.create_evidence_summary()
        with open(f"{self.archive_name}_evidence_summary.md", 'w') as f:
            f.write(summary)
            
        # Save manifest
        print("Saving evidence manifest...")
        with open(f"{self.archive_name}_manifest.json", 'w') as f:
            json.dump(self.manifest, f, indent=2)
            
        # Create ZIP archive
        print("Creating ZIP archive...")
        zip_path = self.create_zip_archive()
        
        # Verify archive integrity
        print("Verifying archive integrity...")
        verification = self.verify_archive_integrity(zip_path)
        
        # Create verification report
        verification_report = f"""
# ARCHIVE VERIFICATION REPORT

Archive: {zip_path}
Verification Date: {datetime.now().isoformat()}

## Results
- Verified Files: {verification['verified_files']}
- Failed Files: {verification['failed_files']}
- Errors: {len(verification['errors'])}

## Status
{'SUCCESS' if verification['failed_files'] == 0 and len(verification['errors']) == 0 else 'FAILED'}

## Errors
"""
        
        for error in verification['errors']:
            verification_report += f"- {error}\n"
            
        with open(f"{self.archive_name}_verification.txt", 'w') as f:
            f.write(verification_report)
            
        print(f"\nArchive creation complete!")
        print(f"Archive file: {zip_path}")
        print(f"Evidence summary: {self.archive_name}_evidence_summary.md")
        print(f"Manifest: {self.archive_name}_manifest.json")
        print(f"Verification report: {self.archive_name}_verification.txt")
        print(f"\nVerification: {verification['verified_files']} files verified")
        
        if verification['failed_files'] > 0 or len(verification['errors']) > 0:
            print("WARNING: Archive verification failed!")
        else:
            print("SUCCESS: Archive integrity verified")
            
        return zip_path

def main():
    """Main archiving function"""
    archiver = InvestigationArchiver()
    archive_path = archiver.create_complete_archive()
    
    print(f"\nInvestigation archive created: {archive_path}")
    print("Store in secure, access-controlled environment.")

if __name__ == "__main__":
    main()
