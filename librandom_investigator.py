#!/usr/bin/env python3
"""
Librandom Repository Investigation Tool
Analyzes the vibehacker88/librandom repository for connections to Haian puzzle
"""

import requests
import json
import re
from datetime import datetime, timezone

class LibrandomInvestigator:
    def __init__(self):
        self.repo_owner = "vibehacker88"
        self.repo_name = "librandom"
        self.base_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        self.repo_data = {}
        self.contents = []
        self.commits = []
        
    def fetch_repo_metadata(self):
        """Fetch repository metadata"""
        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                self.repo_data = response.json()
                print(f"Successfully fetched metadata for {self.repo_owner}/{self.repo_name}")
                return True
            else:
                print(f"Failed to fetch metadata: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error fetching repo metadata: {e}")
            return False
            
    def fetch_contents(self):
        """Fetch repository contents"""
        try:
            response = requests.get(f"{self.base_url}/contents")
            if response.status_code == 200:
                self.contents = response.json()
                print(f"Fetched {len(self.contents)} items from repository")
                return True
            else:
                print(f"Failed to fetch contents: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error fetching contents: {e}")
            return False
            
    def fetch_commits(self, limit=10):
        """Fetch recent commits"""
        try:
            response = requests.get(f"{self.base_url}/commits?per_page={limit}")
            if response.status_code == 200:
                self.commits = response.json()
                print(f"Fetched {len(self.commits)} recent commits")
                return True
            else:
                print(f"Failed to fetch commits: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error fetching commits: {e}")
            return False
            
    def analyze_repo_creation_date(self):
        """Analyze repository creation date for suspicious patterns"""
        if not self.repo_data:
            return {}
            
        created_at = self.repo_data.get('created_at')
        updated_at = self.repo_data.get('updated_at')
        
        if created_at:
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            today = datetime.now(timezone.utc)
            days_old = (today - created_date).days
            
            analysis = {
                'created_at': created_at,
                'updated_at': updated_at,
                'days_old': days_old,
                'suspiciously_recent': days_old < 30,
                'created_today': days_old == 0
            }
            
            if days_old < 7:
                analysis['alert_level'] = 'HIGH'
                analysis['reason'] = 'Repository created within last week'
            elif days_old < 30:
                analysis['alert_level'] = 'MEDIUM'
                analysis['reason'] = 'Repository created within last month'
            else:
                analysis['alert_level'] = 'LOW'
                analysis['reason'] = 'Repository appears established'
                
            return analysis
            
        return {}
        
    def analyze_repository_structure(self):
        """Analyze repository structure for puzzle-related content"""
        if not self.contents:
            return {}
            
        structure_analysis = {
            'total_files': len(self.contents),
            'file_types': {},
            'suspicious_files': [],
            'puzzle_indicators': []
        }
        
        puzzle_keywords = ['puzzle', 'challenge', 'random', 'seed', 'key', 'crypto', 'hash', 'haian']
        
        for item in self.contents:
            name = item.get('name', '')
            file_type = name.split('.')[-1] if '.' in name else 'unknown'
            
            # Count file types
            structure_analysis['file_types'][file_type] = structure_analysis['file_types'].get(file_type, 0) + 1
            
            # Check for suspicious files
            for keyword in puzzle_keywords:
                if keyword.lower() in name.lower():
                    structure_analysis['suspicious_files'].append({
                        'file': name,
                        'type': item.get('type', 'unknown'),
                        'match_keyword': keyword
                    })
                    
        return structure_analysis
        
    def analyze_commit_messages(self):
        """Analyze commit messages for clues"""
        if not self.commits:
            return {}
            
        commit_analysis = {
            'total_commits': len(self.commits),
            'suspicious_messages': [],
            'haian_references': [],
            'puzzle_references': []
        }
        
        suspicious_keywords = ['haian', 'puzzle', 'challenge', 'hack', 'secret', 'hidden', 'steganography']
        
        for commit in self.commits:
            message = commit.get('commit', {}).get('message', '')
            author = commit.get('commit', {}).get('author', {}).get('name', 'Unknown')
            date = commit.get('commit', {}).get('author', {}).get('date', '')
            
            # Check for suspicious keywords
            for keyword in suspicious_keywords:
                if keyword.lower() in message.lower():
                    commit_analysis['suspicious_messages'].append({
                        'message': message,
                        'author': author,
                        'date': date,
                        'match_keyword': keyword
                    })
                    
                    if keyword == 'haian':
                        commit_analysis['haian_references'].append(message)
                    elif keyword in ['puzzle', 'challenge']:
                        commit_analysis['puzzle_references'].append(message)
                        
        return commit_analysis
        
    def check_owner_profile(self):
        """Check repository owner profile for connections"""
        try:
            response = requests.get(f"https://api.github.com/users/{self.repo_owner}")
            if response.status_code == 200:
                owner_data = response.json()
                
                profile_analysis = {
                    'username': owner_data.get('login'),
                    'created_at': owner_data.get('created_at'),
                    'public_repos': owner_data.get('public_repos'),
                    'followers': owner_data.get('followers'),
                    'following': owner_data.get('following'),
                    'bio': owner_data.get('bio', ''),
                    'location': owner_data.get('location', ''),
                    'blog': owner_data.get('blog', ''),
                    'suspicious_indicators': []
                }
                
                # Check for suspicious patterns
                if profile_analysis['public_repos'] == 1:
                    profile_analysis['suspicious_indicators'].append('Single repository account')
                    
                if profile_analysis['followers'] == 0 and profile_analysis['following'] == 0:
                    profile_analysis['suspicious_indicators'].append('No social connections')
                    
                if profile_analysis['created_at']:
                    created_date = datetime.fromisoformat(profile_analysis['created_at'].replace('Z', '+00:00'))
                    days_old = (datetime.now(timezone.utc) - created_date).days
                    if days_old < 30:
                        profile_analysis['suspicious_indicators'].append('Recently created account')
                        
                return profile_analysis
                
        except Exception as e:
            print(f"Error checking owner profile: {e}")
            
        return {}
        
    def generate_investigation_report(self):
        """Generate comprehensive investigation report"""
        # Fetch all data
        self.fetch_repo_metadata()
        self.fetch_contents()
        self.fetch_commits()
        
        # Analyze everything
        date_analysis = self.analyze_repo_creation_date()
        structure_analysis = self.analyze_repository_structure()
        commit_analysis = self.analyze_commit_messages()
        profile_analysis = self.check_owner_profile()
        
        # Generate report
        report = []
        report.append("=" * 80)
        report.append("LIBRANDOM REPOSITORY INVESTIGATION REPORT")
        report.append("=" * 80)
        
        # Repository metadata
        report.append("\nREPOSITORY METADATA:")
        report.append(f"Name: {self.repo_data.get('full_name', 'Unknown')}")
        report.append(f"Description: {self.repo_data.get('description', 'No description')}")
        report.append(f"Language: {self.repo_data.get('language', 'Unknown')}")
        report.append(f"Stars: {self.repo_data.get('stargazers_count', 0)}")
        report.append(f"Forks: {self.repo_data.get('forks_count', 0)}")
        report.append(f"Open Issues: {self.repo_data.get('open_issues_count', 0)}")
        
        # Date analysis
        if date_analysis:
            report.append("\nDATE ANALYSIS:")
            report.append(f"Created: {date_analysis.get('created_at', 'Unknown')}")
            report.append(f"Days Old: {date_analysis.get('days_old', 'Unknown')}")
            report.append(f"Alert Level: {date_analysis.get('alert_level', 'Unknown')}")
            report.append(f"Reason: {date_analysis.get('reason', 'Unknown')}")
            
        # Structure analysis
        if structure_analysis:
            report.append("\nSTRUCTURE ANALYSIS:")
            report.append(f"Total Files: {structure_analysis['total_files']}")
            report.append("File Types:")
            for file_type, count in structure_analysis['file_types'].items():
                report.append(f"  {file_type}: {count}")
                
            if structure_analysis['suspicious_files']:
                report.append("\nSuspicious Files:")
                for file_info in structure_analysis['suspicious_files']:
                    report.append(f"  {file_info['file']} (matches: {file_info['match_keyword']})")
                    
        # Commit analysis
        if commit_analysis:
            report.append("\nCOMMIT ANALYSIS:")
            report.append(f"Total Commits: {commit_analysis['total_commits']}")
            
            if commit_analysis['suspicious_messages']:
                report.append("\nSuspicious Commit Messages:")
                for msg_info in commit_analysis['suspicious_messages']:
                    report.append(f"  \"{msg_info['message']}\" - {msg_info['author']}")
                    report.append(f"    Date: {msg_info['date']}")
                    report.append(f"    Match: {msg_info['match_keyword']}")
                    
        # Profile analysis
        if profile_analysis:
            report.append("\nOWNER PROFILE ANALYSIS:")
            report.append(f"Username: {profile_analysis.get('username', 'Unknown')}")
            report.append(f"Public Repos: {profile_analysis.get('public_repos', 0)}")
            report.append(f"Followers: {profile_analysis.get('followers', 0)}")
            report.append(f"Following: {profile_analysis.get('following', 0)}")
            
            if profile_analysis.get('bio'):
                report.append(f"Bio: {profile_analysis['bio']}")
                
            if profile_analysis['suspicious_indicators']:
                report.append("\nSuspicious Indicators:")
                for indicator in profile_analysis['suspicious_indicators']:
                    report.append(f"  - {indicator}")
                    
        # Overall assessment
        report.append("\nOVERALL ASSESSMENT:")
        
        risk_score = 0
        
        if date_analysis.get('suspiciously_recent'):
            risk_score += 3
            report.append("- Repository created recently (suspicious)")
            
        if structure_analysis.get('suspicious_files'):
            risk_score += 2
            report.append("- Contains suspiciously named files")
            
        if commit_analysis.get('suspicious_messages'):
            risk_score += 2
            report.append("- Contains suspicious commit messages")
            
        if profile_analysis.get('suspicious_indicators'):
            risk_score += 1
            report.append("- Owner profile shows suspicious patterns")
            
        if risk_score >= 6:
            risk_level = "HIGH"
        elif risk_score >= 3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        report.append(f"\nRISK SCORE: {risk_score}/8")
        report.append(f"RISK LEVEL: {risk_level}")
        
        if risk_level in ["HIGH", "MEDIUM"]:
            report.append("\nRECOMMENDATION: Further investigation required")
            report.append("This repository may contain clues related to the Haian puzzle")
        else:
            report.append("\nRECOMMENDATION: Low priority investigation")
            report.append("Repository appears to be legitimate")
            
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    """Main investigation function"""
    investigator = LibrandomInvestigator()
    
    # Generate investigation report
    report = investigator.generate_investigation_report()
    
    # Save report
    with open('librandom_investigation_report.txt', 'w') as f:
        f.write(report)
        
    print("Librandom investigation complete. Report saved to 'librandom_investigation_report.txt'")
    print(report)

if __name__ == "__main__":
    main()
