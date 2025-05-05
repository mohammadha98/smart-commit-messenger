import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from github_client import GitHubClient

class TestGitHubClient(unittest.TestCase):
    """Test cases for the GitHubClient class."""
    
    @patch.dict(os.environ, {"GITHUB_TOKEN": "fake_token"})
    def test_init_with_env_token(self):
        """Test initialization with token from environment variable."""
        client = GitHubClient()
        self.assertEqual(client.token, "fake_token")
    
    def test_init_with_provided_token(self):
        """Test initialization with provided token."""
        client = GitHubClient(token="provided_token")
        self.assertEqual(client.token, "provided_token")
    
    @patch.dict(os.environ, {})
    def test_init_without_token(self):
        """Test initialization without a token raises ValueError."""
        with self.assertRaises(ValueError):
            GitHubClient()
    
    @patch('github.Github.get_repo')
    def test_connect_to_repository_success(self, mock_get_repo):
        """Test successful connection to a repository."""
        mock_repo = MagicMock()
        mock_get_repo.return_value = mock_repo
        
        client = GitHubClient(token="fake_token")
        result = client.connect_to_repository("user/repo")
        
        self.assertTrue(result)
        self.assertEqual(client.repository, mock_repo)
        self.assertEqual(client.repository_name, "user/repo")
        mock_get_repo.assert_called_once_with("user/repo")
    
    @patch('github.Github.get_repo')
    def test_connect_to_repository_failure(self, mock_get_repo):
        """Test failed connection to a repository."""
        from github.GithubException import GithubException
        mock_get_repo.side_effect = GithubException(404, "Not Found")
        
        client = GitHubClient(token="fake_token")
        result = client.connect_to_repository("user/nonexistent")
        
        self.assertFalse(result)
        self.assertIsNone(client.repository)
    
    @patch('github.Repository.Repository.get_readme')
    def test_get_readme_content(self, mock_get_readme):
        """Test getting README content."""
        mock_content = MagicMock()
        mock_content.decoded_content = b"# Test README\n\nThis is a test."
        mock_get_readme.return_value = mock_content
        
        client = GitHubClient(token="fake_token")
        client.repository = MagicMock()
        
        content = client.get_readme_content()
        self.assertEqual(content, "# Test README\n\nThis is a test.")
    
    def test_get_readme_content_no_repository(self):
        """Test getting README content without a connected repository."""
        client = GitHubClient(token="fake_token")
        client.repository = None
        
        content = client.get_readme_content()
        self.assertEqual(content, "")
    
    @patch('github.Repository.Repository.get_commits')
    def test_get_latest_commits(self, mock_get_commits):
        """Test getting latest commits."""
        mock_commits = [MagicMock() for _ in range(3)]
        mock_get_commits.return_value = mock_commits
        
        client = GitHubClient(token="fake_token")
        client.repository = MagicMock()
        
        commits = client.get_latest_commits(branch="main", limit=2)
        self.assertEqual(len(commits), 2)
        mock_get_commits.assert_called_once_with(sha="main")
    
    def test_get_commit_details(self):
        """Test extracting commit details."""
        mock_commit = MagicMock()
        mock_commit.sha = "abc123"
        mock_commit.commit.message = "Test commit"
        mock_commit.commit.author.name = "Test User"
        mock_commit.commit.author.email = "test@example.com"
        mock_commit.commit.author.date.isoformat.return_value = "2023-01-01T12:00:00"
        mock_commit.html_url = "https://github.com/user/repo/commit/abc123"
        
        mock_file = MagicMock()
        mock_file.filename = "test.py"
        mock_file.additions = 10
        mock_file.deletions = 5
        mock_file.changes = 15
        mock_file.status = "modified"
        mock_commit.files = [mock_file]
        
        mock_commit.stats.additions = 10
        mock_commit.stats.deletions = 5
        mock_commit.stats.total = 15
        
        client = GitHubClient(token="fake_token")
        details = client.get_commit_details(mock_commit)
        
        self.assertEqual(details['sha'], "abc123")
        self.assertEqual(details['message'], "Test commit")
        self.assertEqual(details['author']['name'], "Test User")
        self.assertEqual(len(details['files_changed']), 1)
        self.assertEqual(details['files_changed'][0]['filename'], "test.py")
        self.assertEqual(details['stats']['additions'], 10)
        self.assertEqual(details['stats']['deletions'], 5)
        self.assertEqual(details['stats']['total'], 15)

if __name__ == '__main__':
    unittest.main()