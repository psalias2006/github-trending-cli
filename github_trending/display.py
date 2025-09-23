"""
Display Manager for GitHub Trending CLI Tool
Handles all output formatting and display logic.
"""

import shutil
from typing import List, Dict, Callable, Optional
import re
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text


class DisplayManager:
    """Manages display and formatting of repository information."""
    
    # Constants
    DEFAULT_TERMINAL_WIDTH = 80
    MAX_CONSOLE_WIDTH = 120
    REPOS_PER_PAGE = 5
    LINES_PER_PAGE = 30
    
    # Language emoji mapping
    LANGUAGE_EMOJIS = {
        'Python': '🐍', 'JavaScript': '🟨', 'TypeScript': '🔷', 'Java': '☕',
        'C++': '⚡', 'C': '🔧', 'C#': '💜', 'Go': '🐹', 'Rust': '🦀',
        'PHP': '🐘', 'Ruby': '💎', 'Swift': '🍎', 'Kotlin': '🟣',
        'Dart': '🎯', 'Shell': '🐚', 'HTML': '🌐', 'CSS': '🎨',
        'Vue': '💚', 'React': '⚛️', 'Angular': '🅰️', 'Jupyter Notebook': '📓',
        'Lua': '🌙', 'R': '📊', 'Scala': '🔺', 'Perl': '🐪',
        'Haskell': '🎓', 'Clojure': '🔮', 'Elixir': '💧', 'Erlang': '📡',
        'Unknown': '❓'
    }
    
    # Range display mapping
    RANGE_EMOJIS = {"daily": "📅", "weekly": "📊", "monthly": "📈"}
    
    # Trending indicators based on stars today
    TRENDING_THRESHOLDS = [
        (100, "🔥", "red"),
        (50, "🚀", "yellow"), 
        (10, "📈", "green"),
        (0, "", "dim")
    ]
    
    def __init__(self):
        self.terminal_width = self._get_terminal_width()
        self.console = Console(width=min(self.terminal_width - 4, self.MAX_CONSOLE_WIDTH))
    
    def _get_terminal_width(self) -> int:
        """Get the current terminal width."""
        try:
            return shutil.get_terminal_size().columns
        except:
            return self.DEFAULT_TERMINAL_WIDTH
    
    def _format_number(self, number_str: str) -> str:
        """Format number string with commas for better readability."""
        try:
            num = int(number_str.replace(',', ''))
            return f"{num:,}"
        except (ValueError, AttributeError):
            return number_str or "0"
    
    def _get_trending_indicator(self, stars_period: str) -> tuple[str, str]:
        """Get trending indicator and style based on stars in current period."""
        try:
            stars_num = int(stars_period.replace(',', '') or '0')
            for threshold, indicator, style in self.TRENDING_THRESHOLDS:
                if stars_num >= threshold:
                    return indicator, style
        except (ValueError, AttributeError):
            pass
        return "", "dim"
    
    def _clean_repo_name(self, name: str) -> str:
        """Clean up repository name by removing extra whitespace."""
        return re.sub(r'\s+', ' ', name.strip())
    
    def _get_language_emoji(self, language: str) -> str:
        """Get emoji for programming language."""
        return self.LANGUAGE_EMOJIS.get(language, self.LANGUAGE_EMOJIS['Unknown'])
    
    def _create_repo_line(self, index: int, repo: Dict[str, str]) -> Text:
        """Create a formatted text line for a repository."""
        name = self._clean_repo_name(repo.get('name', 'Unknown'))
        language = repo.get('language', 'Unknown').strip()
        stars = self._format_number(repo.get('stars', '0'))
        stars_period = self._format_number(repo.get('stars_period', '0'))
        
        lang_emoji = self._get_language_emoji(language)
        trending_indicator, stars_style = self._get_trending_indicator(repo.get('stars_period', '0'))
        
        line = Text()
        line.append(f"{index:2}. ", style="dim")
        line.append(f"{name}", style="bold")
        line.append(f"  {lang_emoji}", style="dim")
        line.append(f"  ⭐{stars}", style="dim")
        line.append(f"  {trending_indicator}", style=stars_style)
        line.append(f"+{stars_period}", style=stars_style)
        
        return line
    
    def _print_header(self, date_range: str):
        """Print the application header."""
        range_emoji = self.RANGE_EMOJIS.get(date_range, "📋")
        range_text = date_range.title() if date_range != "current" else "Current List"
        
        header_text = Text()
        header_text.append("🚀 GitHub Trending Repositories", style="bold")
        header_text.append(f" - {range_text} {range_emoji}", style="dim")
        
        self.console.print()
        self.console.print(header_text)
        self.console.print()
    
    def _clear_screen_and_show_header(self, date_range: str = "daily"):
        """Clear screen and redisplay header."""
        print("\033[H\033[2J", end="")
        self._print_header(date_range)
    
    def show_repositories(self, repos: List[Dict[str, str]], date_range: str, callback: Optional[Callable] = None):
        """Display a list of trending repositories with Rich formatting."""
        if not repos:
            self.console.print("[red]No repositories found.[/red]")
            return
        
        self._print_header(date_range)
        self._paginate_repositories(repos, date_range, callback)
        self._print_footer(len(repos))
    
    def _print_footer(self, repo_count: int):
        """Print the application footer."""
        footer_text = Text()
        footer_text.append("Found ", style="dim")
        footer_text.append(str(repo_count), style="bold")
        footer_text.append(" trending repositories", style="dim")
        
        self.console.print()
        self.console.print(footer_text)
    
    def _display_repo_list(self, repos: List[Dict[str, str]]):
        """Display a list of repositories."""
        for i, repo in enumerate(repos):
            line = self._create_repo_line(i + 1, repo)
            description = repo.get('description', 'No description').strip()
            
            self.console.print(line)
            self._print_description_with_indent(description)
            self.console.print()
    
    def _print_description_with_indent(self, description: str):
        """Print description with proper indentation for wrapped lines."""
        import textwrap
        
        # Calculate available width (console width minus indentation)
        available_width = self.console.size.width - 4  # 4 spaces for indentation
        
        # Wrap the text to fit within available width
        wrapped_lines = textwrap.wrap(description, width=available_width)
        
        # Print each line with proper indentation
        for line in wrapped_lines:
            self.console.print(f"    [dim]{line}[/dim]")
    
    
    def show_repository_header(self, repo: Dict[str, str]):
        """Show detailed header information for a repository."""
        name = repo.get('name', 'Unknown')
        url = repo.get('url', '')
        language = repo.get('language', 'Unknown')
        stars = repo.get('stars', '0')
        stars_period = repo.get('stars_period', '0')
        description = repo.get('description', 'No description')
        
        print(f"📦 Name: {name}")
        print(f"🔗 URL: {url}")
        print(f"🏷️  Language: {language}")
        print(f"⭐ Stars: {stars} (+{stars_period} this period)")
        print(f"📝 Description: {description}")
    
    def show_readme(self, readme_content: str):
        """Display README content with beautiful Rich markdown rendering."""
        print("\n" + "-"*80)
        print("📖 README")
        print("-"*80)
        
        if not readme_content or readme_content.strip() == "":
            print("No README content available.")
            return
        
        self._render_readme_content(readme_content)
    
    def _render_readme_content(self, content: str):
        """Render markdown content using Rich with pagination."""
        try:
            markdown = Markdown(content)
            with self.console.capture() as capture:
                self.console.print(markdown)
            
            rendered_content = capture.get()
            self._paginate_content(rendered_content.split('\n'))
            
        except Exception as e:
            print(f"⚠️  Error rendering with Rich: {e}")
            self._paginate_content(content.split('\n'))
    
    def _paginate_content(self, lines: List[str]):
        """Display content with pagination for long texts."""
        current_line = 0
        
        while current_line < len(lines):
            end_line = min(current_line + self.LINES_PER_PAGE, len(lines))
            
            # Display current page
            for i in range(current_line, end_line):
                print(lines[i])
            
            current_line = end_line
            
            # Check if there are more lines
            if current_line < len(lines):
                remaining_lines = len(lines) - current_line
                print(f"\n--- More content available ({remaining_lines} lines remaining) ---")
                
                try:
                    user_input = input("📖 Press Enter to continue, 'q' to stop reading: ").strip().lower()
                    if user_input == 'q':
                        print("📖 README reading stopped.")
                        break
                except KeyboardInterrupt:
                    print("\n📖 README reading interrupted.")
                    break
    
    def _paginate_repositories(self, repos: List[Dict[str, str]], date_range: str, callback: Optional[Callable] = None):
        """Display repositories with scrolling pagination and interactive selection."""
        current_repo = 0
        displayed_repos = []
        
        while True:
            # Clear screen and show header if not first iteration
            if current_repo > 0:
                self._clear_screen_and_show_header(date_range)
            
            # Add new repositories to display
            end_repo = min(current_repo + self.REPOS_PER_PAGE, len(repos))
            for i in range(current_repo, end_repo):
                if i >= len(displayed_repos):
                    displayed_repos.append(repos[i])
            
            # Display all repositories shown so far
            self._display_repo_list(displayed_repos)
            
            # Update current position
            if current_repo < len(repos):
                current_repo = end_repo
            
            # Handle user input
            if not self._handle_pagination_input(repos, displayed_repos, current_repo, date_range, callback):
                break
    
    def _handle_pagination_input(self, repos: List[Dict[str, str]], displayed_repos: List[Dict[str, str]], 
                                current_repo: int, date_range: str, callback: Optional[Callable]) -> bool:
        """Handle user input for pagination. Returns False to exit, True to continue."""
        # Show prompt
        if current_repo < len(repos):
            remaining = len(repos) - current_repo
            self.console.print(f"[dim]({remaining} more repositories)[/dim]")
            prompt = f"Enter repo number (1-{len(displayed_repos)}), Enter for more, 'q' to quit: "
        else:
            prompt = f"Enter repo number (1-{len(displayed_repos)}) or 'q' to quit: "
        
        try:
            user_input = input(prompt).strip().lower()
            
            if user_input == 'q':
                return False
            elif user_input == '':
                if current_repo >= len(repos):
                    # No more repos, redisplay current state
                    self._clear_screen_and_show_header(date_range)
                    self._display_repo_list(displayed_repos)
                return True
            else:
                # Try to parse as repository number
                try:
                    repo_num = int(user_input)
                    if 1 <= repo_num <= len(displayed_repos):
                        if callback:
                            callback(repo_num - 1, displayed_repos)
                            self._clear_screen_and_show_header(date_range)
                        else:
                            selected_repo = displayed_repos[repo_num - 1]
                            self.console.print(f"\n[green]Selected: {selected_repo.get('name', 'Unknown')}[/green]")
                            input("Press Enter to continue browsing...")
                        return True
                    else:
                        self.console.print(f"[red]Please enter a number between 1 and {len(displayed_repos)}[/red]")
                        return True
                except ValueError:
                    self.console.print("[red]Please enter a valid number, Enter, or 'q'[/red]")
                    return True
        except KeyboardInterrupt:
            print("\nInterrupted.")
            return False
    
    def show_error(self, message: str):
        """Display an error message."""
        print(f"❌ Error: {message}")
    
    def show_success(self, message: str):
        """Display a success message."""
        print(f"✅ {message}")
