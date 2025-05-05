import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from commit_analyzer import CommitAnalyzer

class TestCommitAnalyzer(unittest.TestCase):
    """Test cases for the CommitAnalyzer class."""
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"})
    def test_init_with_env_key(self):
        """Test initialization with API key from environment variable."""
        analyzer = CommitAnalyzer()
        self.assertEqual(analyzer.api_key, "fake_key")
    
    @patch.dict(os.environ, {})
    def test_init_without_key(self):
        """Test initialization without an API key raises ValueError."""
        with self.assertRaises(ValueError):
            CommitAnalyzer()
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"})
    def test_init_with_custom_params(self):
        """Test initialization with custom model and token parameters."""
        analyzer = CommitAnalyzer(model_name="gpt-4", max_tokens=1000)
        self.assertEqual(analyzer.model_name, "gpt-4")
        self.assertEqual(analyzer.max_tokens, 1000)
    
    def test_format_files_changed(self):
        """Test formatting of files changed information."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
            analyzer = CommitAnalyzer()
            
            files_changed = [
                {
                    'filename': 'test.py',
                    'status': 'modified',
                    'additions': 10,
                    'deletions': 5
                },
                {
                    'filename': 'new.py',
                    'status': 'added',
                    'additions': 20,
                    'deletions': 0
                }
            ]
            
            formatted = analyzer.format_files_changed(files_changed)
            self.assertIn("Modified: test.py (+10, -5)", formatted)
            self.assertIn("Added: new.py (+20, -0)", formatted)
    
    @patch('langchain.chains.LLMChain.run')
    def test_analyze_commit(self, mock_run):
        """Test analyzing a commit and generating a description."""
        mock_run.return_value = "This is a test description of the commit."
        
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
            analyzer = CommitAnalyzer()
            
            commit_details = {
                'message': 'Test commit',
                'files_changed': [
                    {
                        'filename': 'test.py',
                        'status': 'modified',
                        'additions': 10,
                        'deletions': 5
                    }
                ],
                'stats': {
                    'additions': 10,
                    'deletions': 5,
                    'total': 15
                }
            }
            
            description = analyzer.analyze_commit(commit_details, "Test project description")
            self.assertEqual(description, "This is a test description of the commit.")
            mock_run.assert_called_once()
    
    def test_analyze_commit_empty_details(self):
        """Test analyzing a commit with empty details."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake_key"}):
            analyzer = CommitAnalyzer()
            description = analyzer.analyze_commit({})
            self.assertEqual(description, "")

if __name__ == '__main__':
    unittest.main()