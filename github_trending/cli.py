"""
Command Line Interface for GitHub Trending CLI Tool
"""

import argparse
import sys
from typing import List, Dict
from .scraper import GitHubTrendingScraper
from .display import DisplayManager


class GitHubTrendingCLI:
    """Main CLI application class."""
    
    def __init__(self):
        self.scraper = GitHubTrendingScraper()
        self.display = DisplayManager()
        self.current_repos = []
    
    def run(self):
        """Main entry point for the CLI application."""
        parser = self._create_parser()
        args = parser.parse_args()
        
        # Fetch trending repositories
        print("🔍 Fetching trending repositories...")
        self.current_repos = self.scraper.get_trending_repos(args.range)
        
        if not self.current_repos:
            print("❌ No repositories found or error occurred.")
            sys.exit(1)
        
        # Display repositories
        self.display.show_repositories(self.current_repos, args.range)
        
        # Start interactive navigation
        self._interactive_navigation(args.range)
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            description="Browse GitHub trending repositories from the command line",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  github-trending                    # Show today's trending repos
  github-trending --range weekly     # Show this week's trending repos
  github-trending --range monthly    # Show this month's trending repos
            """
        )
        
        parser.add_argument(
            '--range', '-r',
            choices=['daily', 'weekly', 'monthly'],
            default='daily',
            help='Time range for trending repositories (default: daily)'
        )
        
        return parser
    
    def _interactive_navigation(self, date_range: str):
        """Handle interactive navigation through repositories."""
        while True:
            try:
                print("\n" + "╔" + "═"*58 + "╗")
                print("║" + "🧭 Navigation Menu".center(58) + "║")
                print("╠" + "═"*58 + "╣")
                print("║  📖 Enter a number (1-{}) to view README".format(len(self.current_repos)).ljust(58) + "║")
                print("║  📋 Enter 'list' or 'l' to show repositories again".ljust(58) + "║")
                print("║  🚪 Enter 'quit' or 'q' to exit".ljust(58) + "║")
                print("╚" + "═"*58 + "╝")
                
                user_input = input("\n👉 Your choice: ").strip().lower()
                
                if user_input in ['quit', 'q', 'exit']:
                    print("\n👋 Thanks for using GitHub Trending CLI!")
                    break
                elif user_input in ['list', 'l']:
                    self.display.show_repositories(self.current_repos, date_range)
                elif user_input.isdigit():
                    repo_index = int(user_input) - 1
                    if 0 <= repo_index < len(self.current_repos):
                        self._show_repository_details(repo_index)
                    else:
                        print(f"❌ Invalid number. Please enter 1-{len(self.current_repos)}")
                else:
                    print("❌ Invalid input. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for using GitHub Trending CLI!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
    
    def _show_repository_details(self, repo_index: int):
        """Show detailed information and README for a repository."""
        repo = self.current_repos[repo_index]
        
        print("\n" + "="*80)
        print(f"📦 Repository Details")
        print("="*80)
        
        self.display.show_repository_header(repo)
        
        print("\n📖 Fetching README...")
        readme_content = self.scraper.get_readme(repo['url'])
        
        self.display.show_readme(readme_content)
        
        # Wait for user to continue
        input("\n📖 Press Enter to continue...")


def main():
    """Entry point for the CLI application."""
    try:
        cli = GitHubTrendingCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using GitHub Trending CLI!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
