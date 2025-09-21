"""
Command Line Interface for GitHub Trending CLI Tool
"""

import argparse
import sys
from typing import List, Dict, Callable
from .scraper import GitHubTrendingScraper
from .display import DisplayManager


class GitHubTrendingCLI:
    """Main CLI application class."""
    
    # Constants
    VALID_RANGES = ['daily', 'weekly', 'monthly']
    DEFAULT_RANGE = 'daily'
    
    def __init__(self):
        self.scraper = GitHubTrendingScraper()
        self.display = DisplayManager()
        self.current_repos: List[Dict[str, str]] = []
    
    def run(self):
        """Main entry point for the CLI application."""
        args = self._parse_arguments()
        
        if not self._fetch_repositories(args.range):
            sys.exit(1)
        
        self._display_repositories(args.range)
    
    def _parse_arguments(self) -> argparse.Namespace:
        """Parse command line arguments."""
        parser = self._create_parser()
        return parser.parse_args()
    
    def _fetch_repositories(self, date_range: str) -> bool:
        """Fetch trending repositories. Returns True if successful."""
        print("🔍 Fetching trending repositories...")
        self.current_repos = self.scraper.get_trending_repos(date_range)
        
        if not self.current_repos:
            print("❌ No repositories found or error occurred.")
            return False
        return True
    
    def _display_repositories(self, date_range: str):
        """Display repositories with interactive interface."""
        self.display.show_repositories(
            self.current_repos, 
            date_range, 
            callback=self._handle_repository_selection
        )
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="Browse GitHub trending repositories from the command line",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_usage_examples()
        )
        
        parser.add_argument(
            '--range', '-r',
            choices=self.VALID_RANGES,
            default=self.DEFAULT_RANGE,
            help=f'Time range for trending repositories (default: {self.DEFAULT_RANGE})'
        )
        
        return parser
    
    def _get_usage_examples(self) -> str:
        """Get usage examples for the help text."""
        return """
Examples:
  github-trending                    # Show today's trending repos
  github-trending --range weekly     # Show this week's trending repos
  github-trending --range monthly    # Show this month's trending repos
            """
    
    def _handle_repository_selection(self, repo_index: int, displayed_repos: List[Dict[str, str]]):
        """Handle repository selection from the scrolling interface."""
        repo = displayed_repos[repo_index]
        
        self._show_repository_details(repo)
        self._show_repository_readme(repo)
        self._wait_for_user()
    
    def _show_repository_details(self, repo: Dict[str, str]):
        """Display repository details header."""
        print("\n" + "="*80)
        print("📦 Repository Details")
        print("="*80)
        self.display.show_repository_header(repo)
    
    def _show_repository_readme(self, repo: Dict[str, str]):
        """Fetch and display repository README."""
        print("\n📖 Fetching README...")
        readme_content = self.scraper.get_readme(repo['url'])
        self.display.show_readme(readme_content)
    
    def _wait_for_user(self):
        """Wait for user input to continue."""
        input("\n📖 Press Enter to continue...")


def main():
    """Entry point for the CLI application."""
    try:
        cli = GitHubTrendingCLI()
        cli.run()
    except KeyboardInterrupt:
        _handle_keyboard_interrupt()
    except Exception as e:
        _handle_unexpected_error(e)


def _handle_keyboard_interrupt():
    """Handle keyboard interrupt gracefully."""
    print("\n\n👋 Thanks for using GitHub Trending CLI!")
    sys.exit(0)


def _handle_unexpected_error(error: Exception):
    """Handle unexpected errors."""
    print(f"❌ An unexpected error occurred: {error}")
    sys.exit(1)


if __name__ == "__main__":
    main()
