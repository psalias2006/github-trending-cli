"""
GitHub Trending Scraper
Handles scraping trending repositories from GitHub.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re


class GitHubTrendingScraper:
    """Scraper for GitHub trending repositories."""
    
    BASE_URL = "https://github.com/trending"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def get_trending_repos(self, date_range: str = "daily") -> List[Dict[str, str]]:
        """
        Fetch trending repositories from GitHub.
        
        Args:
            date_range: "daily", "weekly", or "monthly"
            
        Returns:
            List of repository dictionaries with name, description, language, stars, etc.
        """
        url = self.BASE_URL
        params = {}
        
        if date_range == "weekly":
            params["since"] = "weekly"
        elif date_range == "monthly":
            params["since"] = "monthly"
        # daily is default, no param needed
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return self._parse_trending_page(response.text)
        except requests.RequestException as e:
            print(f"Error fetching trending repositories: {e}")
            return []
    
    def _parse_trending_page(self, html: str) -> List[Dict[str, str]]:
        """Parse the HTML content of the trending page."""
        soup = BeautifulSoup(html, 'html.parser')
        repos = []
        
        # Find all repository articles
        repo_articles = soup.find_all('article', class_='Box-row')
        
        for article in repo_articles:
            try:
                repo_info = self._extract_repo_info(article)
                if repo_info:
                    repos.append(repo_info)
            except Exception as e:
                # Skip malformed entries
                continue
        
        return repos
    
    def _extract_repo_info(self, article) -> Optional[Dict[str, str]]:
        """Extract repository information from an article element."""
        # Repository name and URL
        title_element = article.find('h2', class_='h3')
        if not title_element:
            return None
            
        link_element = title_element.find('a')
        if not link_element:
            return None
            
        repo_name = link_element.get_text().strip()
        repo_url = "https://github.com" + link_element.get('href', '')
        
        # Description
        description_element = article.find('p', class_='col-9')
        description = description_element.get_text().strip() if description_element else "No description"
        
        # Language
        language_element = article.find('span', {'itemprop': 'programmingLanguage'})
        language = language_element.get_text().strip() if language_element else "Unknown"
        
        # Stars
        stars_element = article.find('a', href=re.compile(r'/stargazers$'))
        stars = "0"
        if stars_element:
            stars_text = stars_element.get_text().strip()
            stars = stars_text.replace(',', '')
        
        # Stars today
        stars_today_element = article.find('span', class_='d-inline-block')
        stars_today = "0"
        if stars_today_element and "stars today" in stars_today_element.get_text():
            stars_today_text = stars_today_element.get_text()
            stars_today_match = re.search(r'(\d+(?:,\d+)*)', stars_today_text)
            if stars_today_match:
                stars_today = stars_today_match.group(1).replace(',', '')
        
        return {
            'name': repo_name,
            'url': repo_url,
            'description': description,
            'language': language,
            'stars': stars,
            'stars_today': stars_today
        }
    
    def get_readme(self, repo_url: str) -> str:
        """
        Fetch the README content for a repository.
        
        Args:
            repo_url: Full GitHub repository URL
            
        Returns:
            README content as string
        """
        try:
            # Convert GitHub URL to raw README URL
            repo_path = repo_url.replace('https://github.com/', '')
            readme_url = f"https://raw.githubusercontent.com/{repo_path}/main/README.md"
            
            response = self.session.get(readme_url)
            if response.status_code == 404:
                # Try master branch if main doesn't exist
                readme_url = f"https://raw.githubusercontent.com/{repo_path}/master/README.md"
                response = self.session.get(readme_url)
            
            if response.status_code == 200:
                return response.text
            else:
                return "README not found or not accessible."
                
        except requests.RequestException as e:
            return f"Error fetching README: {e}"
