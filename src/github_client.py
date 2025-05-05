import os
import logging
from github import Github
from github.GithubException import GithubException

class GitHubClient:
    """Client for interacting with GitHub API to fetch repository and commit information."""
    
    def __init__(self, token=None, repository=None):
        """
        Initialize the GitHub client.
        
        Args:
            token (str, optional): GitHub personal access token. Defaults to None.
            repository (str, optional): Repository name in format 'username/repo'. Defaults to None.
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token is required. Set it in .env file or pass it to the constructor.")
        
        self.repository_name = repository
        self.github = Github(self.token)
        self.repository = None
        
        if self.repository_name:
            self.connect_to_repository(self.repository_name)
    
    def connect_to_repository(self, repository_name):
        """
        Connect to a GitHub repository.
        
        Args:
            repository_name (str): Repository name in format 'username/repo'.
            
        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            self.repository = self.github.get_repo(repository_name)
            self.repository_name = repository_name
            logging.info(f"Successfully connected to repository: {repository_name}")
            return True
        except GithubException as e:
            logging.error(f"Failed to connect to repository {repository_name}: {str(e)}")
            return False
    
    def get_readme_content(self):
        """
        Get the content of the README.md file from the repository.
        
        Returns:
            str: Content of the README.md file or empty string if not found.
        """
        if not self.repository:
            logging.error("Repository not connected. Call connect_to_repository first.")
            return ""
        
        try:
            readme = self.repository.get_readme()
            return readme.decoded_content.decode('utf-8')
        except GithubException as e:
            logging.error(f"Failed to get README content: {str(e)}")
            return ""
    
    def get_latest_commits(self, branch="main", limit=5):
        """
        Get the latest commits from the repository.
        
        Args:
            branch (str, optional): Branch name. Defaults to "main".
            limit (int, optional): Maximum number of commits to fetch. Defaults to 5.
            
        Returns:
            list: List of commit objects.
        """
        if not self.repository:
            logging.error("Repository not connected. Call connect_to_repository first.")
            return []
        
        try:
            commits = list(self.repository.get_commits(sha=branch))[:limit]
            return commits
        except GithubException as e:
            logging.error(f"Failed to get commits: {str(e)}")
            return []
    
    def get_commit_details(self, commit):
        """
        Extract relevant details from a commit object.
        
        Args:
            commit: GitHub commit object.
            
        Returns:
            dict: Dictionary containing commit details.
        """
        if not commit:
            return {}
        
        try:
            # Get the files changed in this commit
            files_changed = [{
                'filename': file.filename,
                'additions': file.additions,
                'deletions': file.deletions,
                'changes': file.changes,
                'status': file.status
            } for file in commit.files]
            
            # Create a structured commit details dictionary
            commit_details = {
                'sha': commit.sha,
                'message': commit.commit.message,
                'author': {
                    'name': commit.commit.author.name,
                    'email': commit.commit.author.email,
                    'date': commit.commit.author.date.isoformat()
                },
                'files_changed': files_changed,
                'stats': {
                    'additions': commit.stats.additions,
                    'deletions': commit.stats.deletions,
                    'total': commit.stats.total
                },
                'html_url': commit.html_url
            }
            
            return commit_details
        except Exception as e:
            logging.error(f"Error extracting commit details: {str(e)}")
            return {}