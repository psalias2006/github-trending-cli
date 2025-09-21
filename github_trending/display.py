"""
Display Manager for GitHub Trending CLI Tool
Handles all output formatting and display logic.
"""

import os
import shutil
from typing import List, Dict
import re


class DisplayManager:
    """Manages display and formatting of repository information."""
    
    # Language colors mapping
    LANGUAGE_COLORS = {
        'Python': '🐍',
        'JavaScript': '🟨',
        'TypeScript': '🔷',
        'Java': '☕',
        'C++': '⚡',
        'C': '🔧',
        'C#': '💜',
        'Go': '🐹',
        'Rust': '🦀',
        'PHP': '🐘',
        'Ruby': '💎',
        'Swift': '🍎',
        'Kotlin': '🟣',
        'Dart': '🎯',
        'Shell': '🐚',
        'HTML': '🌐',
        'CSS': '🎨',
        'Vue': '💚',
        'React': '⚛️',
        'Angular': '🅰️',
        'Jupyter Notebook': '📓',
        'Lua': '🌙',
        'R': '📊',
        'Scala': '🔺',
        'Perl': '🐪',
        'Haskell': '🎓',
        'Clojure': '🔮',
        'Elixir': '💧',
        'Erlang': '📡',
        'Unknown': '❓'
    }
    
    def __init__(self):
        self.terminal_width = self._get_terminal_width()
    
    def _get_terminal_width(self) -> int:
        """Get the current terminal width."""
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80  # Default fallback
    
    def _format_number(self, number_str: str) -> str:
        """Format number string with commas for better readability."""
        try:
            # Remove existing commas and convert to int
            num = int(number_str.replace(',', ''))
            # Format with commas
            return f"{num:,}"
        except (ValueError, AttributeError):
            return number_str or "0"
    
    def show_repositories(self, repos: List[Dict[str, str]], date_range: str):
        """Display a list of trending repositories."""
        if not repos:
            print("No repositories found.")
            return
        
        # Header with enhanced styling
        range_emoji = {"daily": "📅", "weekly": "📊", "monthly": "📈"}.get(date_range, "📋")
        range_text = date_range.title() if date_range != "current" else "Current List"
        
        # Create a beautiful header
        header_line = "═" * self.terminal_width
        print(f"\n{header_line}")
        print(f"🚀 GitHub Trending Repositories - {range_text} {range_emoji}".center(self.terminal_width))
        print(f"🌟 Discover the hottest projects on GitHub".center(self.terminal_width))
        print(f"{header_line}")
        
        # Repository list with enhanced formatting
        for i, repo in enumerate(repos, 1):
            self._print_repository_summary(i, repo)
            # Add separator between repos (except for the last one)
            if i < len(repos):
                print("─" * min(60, self.terminal_width - 10))
        
        # Footer with stats
        print(f"\n{header_line}")
        print(f"📊 Found {len(repos)} trending repositories • Happy coding! 🎉".center(self.terminal_width))
        print(f"{header_line}")
    
    def _print_repository_summary(self, index: int, repo: Dict[str, str]):
        """Print a single repository summary with enhanced formatting."""
        name = repo.get('name', 'Unknown').strip()
        language = repo.get('language', 'Unknown').strip()
        stars = repo.get('stars', '0')
        stars_today = repo.get('stars_today', '0')
        description = repo.get('description', 'No description').strip()
        
        # Clean up repository name (remove extra whitespace)
        name = re.sub(r'\s+', ' ', name)
        
        # Get language emoji
        lang_emoji = self.LANGUAGE_COLORS.get(language, self.LANGUAGE_COLORS['Unknown'])
        
        # Format numbers with commas for better readability
        stars_formatted = self._format_number(stars)
        stars_today_formatted = self._format_number(stars_today)
        
        # Keep full description without truncation
        
        # Stars display with trending indicator
        stars_today_num = int(stars_today.replace(',', '') or '0')
        if stars_today_num > 100:
            trending_indicator = "🔥"
        elif stars_today_num > 50:
            trending_indicator = "📈"
        elif stars_today_num > 10:
            trending_indicator = "⭐"
        else:
            trending_indicator = "✨"
        
        # Enhanced repository display with better formatting
        print(f"\n┌─ {index:2d}. 📦 {name}")
        print(f"├─ {lang_emoji} {language}")
        print(f"├─ {trending_indicator} {stars_formatted} stars (+{stars_today_formatted} today)")
        print(f"└─ 📝 {description}")
        
        # Add selection hint with subtle styling
        print(f"   💡 Type '{index}' to view README")
    
    def show_repository_header(self, repo: Dict[str, str]):
        """Show detailed header information for a repository."""
        name = repo.get('name', 'Unknown')
        url = repo.get('url', '')
        language = repo.get('language', 'Unknown')
        stars = repo.get('stars', '0')
        stars_today = repo.get('stars_today', '0')
        description = repo.get('description', 'No description')
        
        print(f"📦 Name: {name}")
        print(f"🔗 URL: {url}")
        print(f"🏷️  Language: {language}")
        print(f"⭐ Stars: {stars} ({stars_today} today)")
        print(f"📝 Description: {description}")
    
    def show_readme(self, readme_content: str):
        """Display README content with proper formatting."""
        print("\n" + "-"*80)
        print("📖 README")
        print("-"*80)
        
        if not readme_content or readme_content.strip() == "":
            print("No README content available.")
            return
        
        # Split content into lines for better display
        lines = readme_content.split('\n')
        
        # Display with pagination for very long READMEs
        if len(lines) > 50:
            self._paginate_content(lines)
        else:
            for line in lines:
                print(line)
    
    def _paginate_content(self, lines: List[str]):
        """Display content with pagination for long texts."""
        lines_per_page = 30
        current_line = 0
        
        while current_line < len(lines):
            # Display current page
            end_line = min(current_line + lines_per_page, len(lines))
            
            for i in range(current_line, end_line):
                print(lines[i])
            
            current_line = end_line
            
            # Check if there are more lines
            if current_line < len(lines):
                remaining_lines = len(lines) - current_line
                print(f"\n--- More content available ({remaining_lines} lines remaining) ---")
                
                try:
                    user_input = input("Press Enter to continue, 'q' to stop reading: ").strip().lower()
                    if user_input == 'q':
                        print("📖 README reading stopped.")
                        break
                except KeyboardInterrupt:
                    print("\n📖 README reading interrupted.")
                    break
    
    def show_error(self, message: str):
        """Display an error message."""
        print(f"❌ Error: {message}")
    
    def show_success(self, message: str):
        """Display a success message."""
        print(f"✅ {message}")
