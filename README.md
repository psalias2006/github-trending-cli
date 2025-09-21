# 🚀 GitHub Trending CLI

A simple and elegant command-line tool to browse GitHub trending repositories with interactive navigation and README viewing.

## ✨ Features

- 📊 **Browse trending repositories** from GitHub's trending page
- 📅 **Multiple time ranges**: daily, weekly, and monthly trends
- 🧭 **Interactive navigation** to explore repositories
- 📖 **README viewer** to read project documentation directly in terminal
- 🎨 **Beautiful, modern interface** with Unicode box drawing, language-specific emojis, and trending indicators
- ⚡ **Fast and lightweight** with minimal dependencies

## 🛠️ Installation

### Option 1: Install from source (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/github-trending-cli.git
cd github-trending-cli

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Option 2: Direct installation

```bash
# Install dependencies
pip install requests beautifulsoup4 lxml

# Run directly
python -m github_trending.cli
```

## ⚡ Quick Start

```bash
# After installation, simply run:
github-trending

# Or try different time ranges:
github-trending --range weekly
github-trending --range monthly
```

## 🚀 Usage

### Basic Commands

```bash
# Show today's trending repositories
github-trending

# Show this week's trending repositories
github-trending --range weekly

# Show this month's trending repositories  
github-trending --range monthly

# Short form
github-trending -r weekly
```

### Interactive Navigation

Once the tool displays the trending repositories, you can:

- **Enter a number (1-25)** to view a repository's README
- **Enter 'list' or 'l'** to show the repository list again
- **Enter 'quit' or 'q'** to exit the application

### Example Session

```bash
$ github-trending --range weekly

════════════════════════════════════════════════════════════════════════════════
                    🚀 GitHub Trending Repositories - Weekly 📊                    
                   🌟 Discover the hottest projects on GitHub                    
════════════════════════════════════════════════════════════════════════════════

┌─  1. 📦 microsoft/TypeScript
├─ 🔷 TypeScript
├─ 🔥 95,234 stars (+234 today)
└─ 📝 TypeScript is a superset of JavaScript that compiles to clean JavaScript...
   💡 Type '1' to view README
────────────────────────────────────────────────────────────

┌─  2. 📦 facebook/react
├─ 🟨 JavaScript
├─ 🔥 201,456 stars (+456 today)
└─ 📝 A declarative, efficient, and flexible JavaScript library for building...
   💡 Type '2' to view README

════════════════════════════════════════════════════════════════════════════════
               📊 Found 25 trending repositories • Happy coding! 🎉                
════════════════════════════════════════════════════════════════════════════════

╔══════════════════════════════════════════════════════════╗
║                    🧭 Navigation Menu                    ║
╠══════════════════════════════════════════════════════════╣
║  📖 Enter a number (1-25) to view README                ║
║  📋 Enter 'list' or 'l' to show repositories again      ║
║  🚪 Enter 'quit' or 'q' to exit                         ║
╚══════════════════════════════════════════════════════════╝

👉 Your choice: 1

================================================================================
📦 Repository Details
================================================================================
📦 Name: microsoft/TypeScript
🔗 URL: https://github.com/microsoft/TypeScript
🏷️  Language: TypeScript
⭐ Stars: 95234 (234 today)
📝 Description: TypeScript is a superset of JavaScript that compiles to clean JavaScript...

📖 Fetching README...

--------------------------------------------------------------------------------
📖 README
--------------------------------------------------------------------------------
# TypeScript

TypeScript is a language for application-scale JavaScript...
[README content continues...]

📖 Press Enter to continue...
```

## 📁 Project Structure

```
github-trending-cli/
├── github_trending/
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Main CLI interface and argument parsing
│   ├── scraper.py           # GitHub trending page scraper
│   └── display.py           # Output formatting and display logic
├── requirements.txt         # Python dependencies
├── setup.py                # Package setup configuration
└── README.md               # This file
```

## 🏗️ Architecture

The project follows a clean, modular architecture:

### `scraper.py` - GitHubTrendingScraper
- Handles HTTP requests to GitHub trending page
- Parses HTML content using BeautifulSoup
- Extracts repository information (name, stars, language, etc.)
- Fetches README content from repositories

### `display.py` - DisplayManager
- Manages all terminal output formatting
- Handles repository list display
- Provides README pagination for long content
- Responsive terminal width detection

### `cli.py` - GitHubTrendingCLI
- Command-line argument parsing
- Interactive navigation loop
- Coordinates between scraper and display components
- Error handling and user input validation

## 🔧 Dependencies

### Dependencies
- **requests** (≥2.28.0) - HTTP requests to GitHub
- **beautifulsoup4** (≥4.11.0) - HTML parsing
- **lxml** (≥4.9.0) - Fast XML/HTML parser backend
- **rich** (≥13.0.0) - Beautiful terminal rendering with colors and formatting

## 🎯 Usage Examples

### View Today's Trending
```bash
github-trending
```

### View Weekly Trending
```bash
github-trending --range weekly
```

### View Monthly Trending
```bash
github-trending -r monthly
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'github_trending'`
**Solution**: Make sure you've installed the package with `pip install -e .`

**Issue**: `requests.exceptions.ConnectionError`
**Solution**: Check your internet connection and GitHub's availability

**Issue**: Empty repository list
**Solution**: GitHub might be rate-limiting requests. Wait a few minutes and try again.

### Getting Help

If you encounter any issues:

1. Check the [Issues](https://github.com/your-username/github-trending-cli/issues) page
2. Create a new issue with detailed information about the problem
3. Include your Python version and operating system

## 🌟 Acknowledgments

- GitHub for providing the trending repositories page
- The Python community for excellent libraries like requests and BeautifulSoup
- All the amazing open-source projects that inspire us daily

---

**Happy exploring! 🚀**
