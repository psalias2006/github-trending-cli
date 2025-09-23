"""
Export Manager for GitHub Trending CLI Tool
Handles exporting trending repositories to CSV and JSON Lines formats.
"""

import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path
import pandas as pd


class ExportManager:
    """Manages exporting repository data to various formats using pandas."""
    
    # Constants
    EXPORT_DIR = "exported"
    
    def __init__(self):
        self._ensure_export_directory()
    
    def _ensure_export_directory(self):
        """Create the export directory if it doesn't exist."""
        Path(self.EXPORT_DIR).mkdir(exist_ok=True)
    
    def _generate_filename(self, date_range: str, export_format: str) -> str:
        """Generate filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = "jsonl" if export_format == "json" else export_format
        return f"{self.EXPORT_DIR}/github_trending_{date_range}_{timestamp}.{extension}"
    
    def _create_dataframe(self, repos: List[Dict[str, str]], date_range: str) -> pd.DataFrame:
        """Create pandas DataFrame from repository data with additional columns."""
        # Create DataFrame from the list of dictionaries
        df = pd.DataFrame(repos)
        
        # Add metadata columns
        df['range'] = date_range.title()
        df['export_datetime'] = datetime.now().isoformat()
        
        return df
    
    def export_to_csv(self, repos: List[Dict[str, str]], date_range: str) -> str:
        """
        Export repositories to CSV format using pandas.
        
        Args:
            repos: List of repository dictionaries
            date_range: Time range (daily, weekly, monthly)
            
        Returns:
            Path to the exported file
        """
        filename = self._generate_filename(date_range, 'csv')
        df = self._create_dataframe(repos, date_range)
        
        # Export to CSV with pandas
        df.to_csv(filename, index=False, encoding='utf-8')
        
        return filename
    
    def export_to_jsonl(self, repos: List[Dict[str, str]], date_range: str) -> str:
        """
        Export repositories to JSON Lines format using pandas.
        
        Args:
            repos: List of repository dictionaries
            date_range: Time range (daily, weekly, monthly)
            
        Returns:
            Path to the exported file
        """
        filename = self._generate_filename(date_range, 'json')
        df = self._create_dataframe(repos, date_range)
        
        # Export to JSON Lines format (one JSON object per line)
        # Use force_ascii=False to avoid escaping and ensure proper UTF-8 encoding
        with open(filename, 'w', encoding='utf-8') as f:
            for record in df.to_dict('records'):
                json.dump(record, f, ensure_ascii=False, separators=(',', ':'))
                f.write('\n')
        
        return filename
    
    def export_repositories(self, repos: List[Dict[str, str]], date_range: str, export_format: str) -> str:
        """
        Export repositories in the specified format using pandas.
        
        Args:
            repos: List of repository dictionaries
            date_range: Time range (daily, weekly, monthly)
            export_format: Format to export (csv or json)
            
        Returns:
            Path to the exported file
            
        Raises:
            ValueError: If export_format is not supported
        """
        if not repos:
            raise ValueError("No repositories to export")
        
        if export_format.lower() == 'csv':
            return self.export_to_csv(repos, date_range)
        elif export_format.lower() == 'json':
            return self.export_to_jsonl(repos, date_range)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")
