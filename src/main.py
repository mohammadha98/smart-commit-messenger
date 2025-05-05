import os
import sys
import logging
import yaml
from dotenv import load_dotenv
from github_client import GitHubClient
from commit_analyzer import CommitAnalyzer
from telegram_sender import TelegramSender

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('smart_commit_messenger.log')
    ]
)

class SmartCommitMessenger:
    """Main class that orchestrates the GitHub commit analysis and Telegram messaging."""
    
    def __init__(self, config_path='../config/config.yaml'):
        """
        Initialize the Smart Commit Messenger.
        
        Args:
            config_path (str, optional): Path to the configuration file. Defaults to '../config/config.yaml'.
        """
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        self.config = self.load_config(config_path)
        if not self.config:
            raise ValueError(f"Failed to load configuration from {config_path}")
        
        # Initialize components
        self.github_client = GitHubClient(
            repository=self.config.get('github', {}).get('repository')
        )
        
        self.commit_analyzer = CommitAnalyzer(
            model_name=self.config.get('ai', {}).get('model', 'gpt-3.5-turbo'),
            max_tokens=self.config.get('ai', {}).get('max_tokens', 500)
        )
        
        self.telegram_sender = TelegramSender(
            channel_id=self.config.get('telegram', {}).get('channel_id')
        )
    
    def load_config(self, config_path):
        """
        Load configuration from YAML file.
        
        Args:
            config_path (str): Path to the configuration file.
            
        Returns:
            dict: Configuration dictionary or None if loading failed.
        """
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logging.error(f"Error loading configuration: {str(e)}")
            return None
    
    def process_latest_commits(self):
        """
        Process the latest commits from the configured repository.
        
        Returns:
            bool: True if processing was successful, False otherwise.
        """
        # Get repository configuration
        repo_config = self.config.get('github', {})
        branch = repo_config.get('branch', 'main')
        commit_limit = repo_config.get('commit_limit', 5)
        
        # Get project name from repository
        project_name = repo_config.get('repository', '').split('/')[-1] if repo_config.get('repository') else 'Unknown Project'
        
        # Get README content for project description
        readme_content = self.github_client.get_readme_content()
        
        # Get latest commits
        commits = self.github_client.get_latest_commits(branch=branch, limit=commit_limit)
        if not commits:
            logging.warning("No commits found to process.")
            return False
        
        # Process each commit
        for commit in commits:
            # Get detailed commit information
            commit_details = self.github_client.get_commit_details(commit)
            if not commit_details:
                logging.warning(f"Failed to get details for commit {commit.sha}")
                continue
            
            # Analyze the commit
            description = self.commit_analyzer.analyze_commit(commit_details, readme_content)
            if not description:
                logging.warning(f"Failed to generate description for commit {commit.sha}")
                continue
            
            # Format and send the message
            message = self.telegram_sender.format_commit_message(project_name, commit_details, description)
            success = self.telegram_sender.send_message(message)
            
            if success:
                logging.info(f"Successfully processed and sent message for commit {commit.sha}")
            else:
                logging.error(f"Failed to send message for commit {commit.sha}")
        
        return True

def main():
    """Main function to run the Smart Commit Messenger."""
    try:
        messenger = SmartCommitMessenger()
        messenger.process_latest_commits()
    except Exception as e:
        logging.error(f"Error running Smart Commit Messenger: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())