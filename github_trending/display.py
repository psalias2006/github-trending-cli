"""
Display Manager for GitHub Trending CLI Tool
Handles all output formatting and display logic.
"""

import os
import shutil
from typing import List, Dict
import re
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.align import Align


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
        self.console = Console(width=min(self.terminal_width - 4, 120))
    
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
    
    def show_repositories(self, repos: List[Dict[str, str]], date_range: str, callback=None):
        """Display a list of trending repositories with Rich formatting."""
        if not repos:
            self.console.print("[red]No repositories found.[/red]")
            return
        
        # Header with enhanced styling
        range_emoji = {"daily": "📅", "weekly": "📊", "monthly": "📈"}.get(date_range, "📋")
        range_text = date_range.title() if date_range != "current" else "Current List"
        
        # Simple header without panels
        header_text = Text()
        header_text.append("🚀 GitHub Trending Repositories", style="bold")
        header_text.append(f" - {range_text} {range_emoji}", style="dim")
        
        self.console.print()
        self.console.print(header_text)
        self.console.print()
        
        # Paginate repository list with Rich
        self._paginate_repositories_rich(repos, callback)
        
        # Simple footer without panels
        footer_text = Text()
        footer_text.append("Found ", style="dim")
        footer_text.append(str(len(repos)), style="bold")
        footer_text.append(" trending repositories", style="dim")
        
        self.console.print()
        self.console.print(footer_text)
    
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
        """Display README content with beautiful Rich markdown rendering."""
        print("\n" + "-"*80)
        print("📖 README")
        print("-"*80)
        
        if not readme_content or readme_content.strip() == "":
            print("No README content available.")
            return
        
        self._render_with_rich(readme_content)
    
    def _render_with_rich(self, content: str):
        """Render markdown content using Rich with beautiful formatting and pagination."""
        try:
            # Create Rich Markdown object
            markdown = Markdown(content)
            
            # Render to string to get the formatted content
            with self.console.capture() as capture:
                self.console.print(markdown)
            
            # Get the rendered content and split into lines
            rendered_content = capture.get()
            lines = rendered_content.split('\n')
            
            # Paginate the beautifully rendered content
            self._paginate_rich_content(lines)
            
        except Exception as e:
            print(f"⚠️  Error rendering with Rich: {e}")
            self._render_fallback(content)
    
    def _paginate_rich_content(self, lines: list):
        """Display Rich-rendered content with pagination."""
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
                    user_input = input("📖 Press Enter to continue, 'q' to stop reading: ").strip().lower()
                    if user_input == 'q':
                        print("📖 README reading stopped.")
                        break
                except KeyboardInterrupt:
                    print("\n📖 README reading interrupted.")
                    break
    
    def _render_fallback(self, content: str):
        """Fallback rendering for plain text display."""
        # Split content into lines for better display
        lines = content.split('\n')
        
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
    
    def _paginate_repositories_rich(self, repos: List[Dict[str, str]], callback=None):
        """Display repositories with scrolling pagination and interactive selection."""
        repos_per_page = 5  # Show 5 repositories per page
        current_repo = 0
        displayed_repos = []  # Keep track of all displayed repos
        
        while True:  # Infinite loop - only exit when user presses 'q'
            # Clear screen for scroll effect (but keep header visible)
            if current_repo > 0:
                # Clear previous content but keep some context
                print("\033[H\033[2J", end="")  # Clear screen
                # Re-print header
                header_text = Text()
                header_text.append("🚀 GitHub Trending Repositories", style="bold")
                header_text.append(" - Daily 📅", style="dim")
                self.console.print(header_text)
                self.console.print()
            
            # Display current page of repositories
            end_repo = min(current_repo + repos_per_page, len(repos))
            
            # Add current page repos to displayed list
            for i in range(current_repo, end_repo):
                if i >= len(displayed_repos):
                    displayed_repos.append(repos[i])
            
            # Show all repositories up to current point
            for i, repo in enumerate(displayed_repos):
                name = repo.get('name', 'Unknown').strip()
                language = repo.get('language', 'Unknown').strip()
                stars = self._format_number(repo.get('stars', '0'))
                stars_today = self._format_number(repo.get('stars_today', '0'))
                description = repo.get('description', 'No description').strip()
                
                # Clean up repository name
                name = re.sub(r'\s+', ' ', name)
                
                # Get language emoji and color
                lang_emoji = self.LANGUAGE_COLORS.get(language, self.LANGUAGE_COLORS['Unknown'])
                
                # Color coding for stars today with trending indicators
                stars_today_num = int(repo.get('stars_today', '0').replace(',', '') or '0')
                if stars_today_num > 100:
                    stars_today_style = "red"
                    trending_indicator = "🔥"
                elif stars_today_num > 50:
                    stars_today_style = "yellow"
                    trending_indicator = "🚀"
                elif stars_today_num > 10:
                    stars_today_style = "green"
                    trending_indicator = "📈"
                else:
                    stars_today_style = "dim"
                    trending_indicator = ""
                
                # Create the main line with repository info
                line = Text()
                line.append(f"{i + 1:2}. ", style="dim")
                line.append(f"{name}", style="bold")
                line.append(f"  {lang_emoji}", style="dim")
                line.append(f"  ⭐{stars}", style="dim")
                line.append(f"  {trending_indicator}", style=stars_today_style)
                line.append(f"+{stars_today}", style=stars_today_style)
                
                self.console.print(line)
                self.console.print(f"    [dim]{description}[/dim]")
                self.console.print()
            
            # Only advance current_repo if there are more repositories to show
            if current_repo < len(repos):
                current_repo = end_repo
            
            # Interactive prompt
            if current_repo < len(repos):
                remaining_repos = len(repos) - current_repo
                self.console.print(f"[dim]({remaining_repos} more repositories)[/dim]")
                prompt_text = f"Enter repo number (1-{len(displayed_repos)}), Enter for more, 'q' to quit: "
            else:
                prompt_text = f"Enter repo number (1-{len(displayed_repos)}) or 'q' to quit: "
            
            try:
                user_input = input(prompt_text).strip().lower()
                
                if user_input == 'q':
                    break
                elif user_input == '':
                    if current_repo >= len(repos):
                        # No more repos, stay in selection mode and redisplay current state
                        print("\033[H\033[2J", end="")  # Clear screen
                        # Re-print header
                        header_text = Text()
                        header_text.append("🚀 GitHub Trending Repositories", style="bold")
                        header_text.append(" - Daily 📅", style="dim")
                        self.console.print(header_text)
                        self.console.print()
                        
                        # Re-display all repos
                        for i, repo in enumerate(displayed_repos):
                            name = repo.get('name', 'Unknown').strip()
                            language = repo.get('language', 'Unknown').strip()
                            stars = self._format_number(repo.get('stars', '0'))
                            stars_today = self._format_number(repo.get('stars_today', '0'))
                            description = repo.get('description', 'No description').strip()
                            
                            # Clean up repository name
                            name = re.sub(r'\s+', ' ', name)
                            
                            # Get language emoji and color
                            lang_emoji = self.LANGUAGE_COLORS.get(language, self.LANGUAGE_COLORS['Unknown'])
                            
                            # Color coding for stars today with trending indicators
                            stars_today_num = int(repo.get('stars_today', '0').replace(',', '') or '0')
                            if stars_today_num > 100:
                                stars_today_style = "red"
                                trending_indicator = "🔥"
                            elif stars_today_num > 50:
                                stars_today_style = "yellow"
                                trending_indicator = "🚀"
                            elif stars_today_num > 10:
                                stars_today_style = "green"
                                trending_indicator = "📈"
                            else:
                                stars_today_style = "dim"
                                trending_indicator = ""
                            
                            # Create the main line with repository info
                            line = Text()
                            line.append(f"{i + 1:2}. ", style="dim")
                            line.append(f"{name}", style="bold")
                            line.append(f"  {lang_emoji}", style="dim")
                            line.append(f"  ⭐{stars}", style="dim")
                            line.append(f"  {trending_indicator}", style=stars_today_style)
                            line.append(f"+{stars_today}", style=stars_today_style)
                            
                            self.console.print(line)
                            self.console.print(f"    [dim]{description}[/dim]")
                            self.console.print()
                        
                        continue
                    # Continue to next page (only if there are more repos)
                    continue
                else:
                    # Try to parse as repository number
                    try:
                        repo_num = int(user_input)
                        if 1 <= repo_num <= len(displayed_repos):
                            # User selected a repository
                            selected_repo = displayed_repos[repo_num - 1]
                            if callback:
                                # Call the callback function (e.g., show repository details)
                                callback(repo_num - 1, displayed_repos)
                                # After viewing details, clear screen and redisplay current state
                                print("\033[H\033[2J", end="")  # Clear screen
                                # Re-print header
                                header_text = Text()
                                header_text.append("🚀 GitHub Trending Repositories", style="bold")
                                header_text.append(" - Daily 📅", style="dim")
                                self.console.print(header_text)
                                self.console.print()
                                # Re-display all repos up to current point
                                continue
                            else:
                                self.console.print(f"\n[green]Selected: {selected_repo.get('name', 'Unknown')}[/green]")
                                input("Press Enter to continue browsing...")
                                continue
                        else:
                            self.console.print(f"[red]Please enter a number between 1 and {len(displayed_repos)}[/red]")
                            continue
                    except ValueError:
                        self.console.print("[red]Please enter a valid number, Enter, or 'q'[/red]")
                        continue
                        
            except KeyboardInterrupt:
                print("\nInterrupted.")
                break
    
    def show_error(self, message: str):
        """Display an error message."""
        print(f"❌ Error: {message}")
    
    def show_success(self, message: str):
        """Display a success message."""
        print(f"✅ {message}")
