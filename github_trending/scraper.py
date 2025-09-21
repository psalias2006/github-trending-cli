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
    
    # Constants
    BASE_URL = "https://github.com/trending"
    RAW_GITHUB_URL = "https://raw.githubusercontent.com"
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    
    # Default branch names to try for README
    DEFAULT_BRANCHES = ['main', 'master']
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})
    
    def get_trending_repos(self, date_range: str = "daily") -> List[Dict[str, str]]:
        """
        Fetch trending repositories from GitHub.
        
        Args:
            date_range: "daily", "weekly", or "monthly"
            
        Returns:
            List of repository dictionaries with name, description, language, stars, etc.
        """
        params = self._build_params(date_range)
        
        try:
            response = self.session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            return self._parse_trending_page(response.text)
        except requests.RequestException as e:
            print(f"Error fetching trending repositories: {e}")
            return []
    
    def _build_params(self, date_range: str) -> Dict[str, str]:
        """Build URL parameters for the given date range."""
        if date_range in ["weekly", "monthly"]:
            return {"since": date_range}
        return {}  # daily is default
    
    def _parse_trending_page(self, html: str) -> List[Dict[str, str]]:
        """Parse the HTML content of the trending page."""
        soup = BeautifulSoup(html, 'html.parser')
        repos = []
        
        repo_articles = soup.find_all('article', class_='Box-row')
        
        for article in repo_articles:
            try:
                repo_info = self._extract_repo_info(article)
                if repo_info:
                    repos.append(repo_info)
            except Exception:
                # Skip malformed entries silently
                continue
        
        return repos
    
    def _extract_repo_info(self, article) -> Optional[Dict[str, str]]:
        """Extract repository information from an article element."""
        # Get basic repo info
        name, url = self._extract_name_and_url(article)
        if not name or not url:
            return None
        
        return {
            'name': name,
            'url': url,
            'description': self._extract_description(article),
            'language': self._extract_language(article),
            'stars': self._extract_stars(article),
            'stars_today': self._extract_stars_today(article)
        }
    
    def _extract_name_and_url(self, article) -> tuple[Optional[str], Optional[str]]:
        """Extract repository name and URL."""
        title_element = article.find('h2', class_='h3')
        if not title_element:
            return None, None
            
        link_element = title_element.find('a')
        if not link_element:
            return None, None
            
        name = link_element.get_text().strip()
        url = "https://github.com" + link_element.get('href', '')
        return name, url
    
    def _extract_description(self, article) -> str:
        """Extract repository description."""
        description_element = article.find('p', class_='col-9')
        return description_element.get_text().strip() if description_element else "No description"
    
    def _extract_language(self, article) -> str:
        """Extract programming language."""
        language_element = article.find('span', {'itemprop': 'programmingLanguage'})
        return language_element.get_text().strip() if language_element else "Unknown"
    
    def _extract_stars(self, article) -> str:
        """Extract total stars count."""
        stars_element = article.find('a', href=re.compile(r'/stargazers$'))
        if stars_element:
            return stars_element.get_text().strip().replace(',', '')
        return "0"
    
    def _extract_stars_today(self, article) -> str:
        """Extract stars gained today."""
        stars_today_element = article.find('span', class_='d-inline-block')
        if stars_today_element and "stars today" in stars_today_element.get_text():
            stars_today_match = re.search(r'(\d+(?:,\d+)*)', stars_today_element.get_text())
            if stars_today_match:
                return stars_today_match.group(1).replace(',', '')
        return "0"
    
    def get_readme(self, repo_url: str) -> str:
        """
        Fetch the README content for a repository.
        
        Args:
            repo_url: Full GitHub repository URL
            
        Returns:
            README content as string
        """
        repo_path = self._extract_repo_path(repo_url)
        if not repo_path:
            return "Invalid repository URL."
        
        # Try different branches
        for branch in self.DEFAULT_BRANCHES:
            readme_url = f"{self.RAW_GITHUB_URL}/{repo_path}/{branch}/README.md"
            try:
                response = self.session.get(readme_url)
                if response.status_code == 200:
                    return response.text
            except requests.RequestException:
                continue
        
        return "README not found or not accessible."
    
    def _extract_repo_path(self, repo_url: str) -> Optional[str]:
        """Extract repository path from GitHub URL."""
        try:
            return repo_url.replace('https://github.com/', '')
        except (AttributeError, ValueError):
            return None
