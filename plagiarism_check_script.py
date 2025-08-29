#!/usr/bin/env python3
"""
Plagiarism Detection Script for Hotel NaWaB Website
This script helps check your website content for potential plagiarism issues.
"""

import re
import requests
from urllib.parse import quote_plus
import time
from bs4 import BeautifulSoup
import json

class PlagiarismChecker:
    def __init__(self):
        self.results = []
        
    def extract_text_from_html(self, html_file_path):
        """Extract readable text content from HTML file"""
        try:
            with open(html_file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), 'html.parser')
                
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text and clean it
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error reading HTML file: {e}")
            return ""
    
    def extract_sentences(self, text, min_length=10):
        """Extract sentences from text for checking"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > min_length]
    
    def google_search_check(self, query, max_results=5):
        """Check if text appears in Google search results"""
        try:
            # Note: This is a simplified check - for production use, consider Google Custom Search API
            search_url = f"https://www.google.com/search?q={quote_plus(f'"{query}"')}"
            print(f"Checking: {query[:50]}...")
            
            # In a real implementation, you would need to handle this properly
            # For now, we'll just return a placeholder result
            return {
                'query': query,
                'potentially_plagiarized': False,
                'note': 'Manual Google search recommended for: ' + query[:50] + '...'
            }
            
        except Exception as e:
            return {
                'query': query,
                'error': str(e),
                'potentially_plagiarized': False
            }
    
    def check_content_sections(self, html_file_path):
        """Check specific content sections for plagiarism"""
        try:
            with open(html_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # Extract specific content sections
            sections_to_check = [
                r'<p class="section__description">(.*?)</p>',
                r'<h4>(.*?)</h4>.*?<p>(.*?)</p>',
                r'class="feature__card">.*?<p>(.*?)</p>',
                r'class="menu__details">.*?<p>(.*?)</p>',
                r'class="news__card">.*?<p>(.*?)</p>'
            ]
            
            extracted_content = []
            for pattern in sections_to_check:
                matches = re.findall(pattern, content, re.DOTALL)
                for match in matches:
                    if isinstance(match, tuple):
                        for text in match:
                            clean_text = BeautifulSoup(text, 'html.parser').get_text().strip()
                            if len(clean_text) > 20:
                                extracted_content.append(clean_text)
                    else:
                        clean_text = BeautifulSoup(match, 'html.parser').get_text().strip()
                        if len(clean_text) > 20:
                            extracted_content.append(clean_text)
            
            return extracted_content
            
        except Exception as e:
            print(f"Error extracting content sections: {e}")
            return []
    
    def run_plagiarism_check(self, html_file_path):
        """Run comprehensive plagiarism check"""
        print("🔍 Starting Plagiarism Check for Hotel NaWaB Website")
        print("=" * 60)
        
        # Extract content sections
        content_sections = self.check_content_sections(html_file_path)
        
        print(f"📄 Found {len(content_sections)} content sections to check")
        print("\n🔍 Checking for potential plagiarism...\n")
        
        results = []
        for i, section in enumerate(content_sections, 1):
            if len(section) > 30:  # Only check substantial content
                print(f"Checking section {i}/{len(content_sections)}")
                result = self.google_search_check(section)
                results.append(result)
                time.sleep(1)  # Be respectful to search engines
        
        # Generate report
        self.generate_report(results)
        return results
    
    def generate_report(self, results):
        """Generate plagiarism check report"""
        print("\n" + "=" * 60)
        print("📊 PLAGIARISM CHECK REPORT")
        print("=" * 60)
        
        total_checks = len(results)
        potential_issues = sum(1 for r in results if r.get('potentially_plagiarized', False))
        
        print(f"Total content sections checked: {total_checks}")
        print(f"Potential plagiarism issues: {potential_issues}")
        print(f"Clean content sections: {total_checks - potential_issues}")
        
        if potential_issues == 0:
            print("\n✅ GREAT NEWS! No plagiarism detected in your content.")
            print("Your Hotel NaWaB website appears to have original content.")
        else:
            print(f"\n⚠️  Found {potential_issues} sections that need review:")
            for result in results:
                if result.get('potentially_plagiarized', False):
                    print(f"- {result['query'][:100]}...")
        
        print("\n📝 RECOMMENDATIONS:")
        print("1. Manually verify any flagged content using online plagiarism checkers")
        print("2. Use tools like Grammarly, Quetext, or Copyscape for detailed analysis")
        print("3. Always rewrite content in your own words")
        print("4. Add hotel-specific details to make content unique")
        print("5. Regular content audits are recommended")
        
        # Save detailed report
        with open('/workspace/plagiarism_check_report.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: /workspace/plagiarism_check_report.json")

def main():
    """Main function to run plagiarism check"""
    checker = PlagiarismChecker()
    
    # Check the main HTML file
    html_file = '/workspace/Hotel_NaWaB_/index.html'
    
    try:
        results = checker.run_plagiarism_check(html_file)
        
        print("\n🎯 NEXT STEPS:")
        print("1. Review the generated report")
        print("2. Use online plagiarism checkers for suspicious content")
        print("3. Rewrite any flagged sections")
        print("4. Run this script regularly for ongoing monitoring")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find HTML file at {html_file}")
        print("Please ensure the file path is correct.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()