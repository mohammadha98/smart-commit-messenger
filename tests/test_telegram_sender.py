import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from telegram_sender import TelegramSender

class TestTelegramSender(unittest.TestCase):
    """Test cases for the TelegramSender class."""
    
    @patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "fake_token"})
    def test_init_with_env_token(self):
        """Test initialization with token from environment variable."""
        sender = TelegramSender()
        self.assertEqual(sender.token, "fake_token")
    
    def test_init_with_provided_token(self):
        """Test initialization with provided token."""
        sender = TelegramSender(token="provided_token")
        self.assertEqual(sender.token, "provided_token")
    
    @patch.dict(os.environ, {})
    def test_init_without_token(self):
        """Test initialization without a token raises ValueError."""
        with self.assertRaises(ValueError):
            TelegramSender()
    
    def test_set_channel(self):
        """Test setting the channel ID."""
        sender = TelegramSender(token="fake_token")
        sender.set_channel("@test_channel")
        self.assertEqual(sender.channel_id, "@test_channel")
    
    @patch('telegram.Bot.send_message')
    def test_send_message_success(self, mock_send_message):
        """Test successful message sending."""
        mock_send_message.return_value = MagicMock()
        
        sender = TelegramSender(token="fake_token", channel_id="@test_channel")
        result = sender.send_message("Test message")
        
        self.assertTrue(result)
        mock_send_message.assert_called_once_with(
            chat_id="@test_channel",
            text="Test message",
            parse_mode='Markdown'
        )
    
    @patch('telegram.Bot.send_message')
    def test_send_message_with_channel_param(self, mock_send_message):
        """Test sending a message with a channel parameter."""
        mock_send_message.return_value = MagicMock()
        
        sender = TelegramSender(token="fake_token")
        result = sender.send_message("Test message", channel_id="@other_channel")
        
        self.assertTrue(result)
        mock_send_message.assert_called_once_with(
            chat_id="@other_channel",
            text="Test message",
            parse_mode='Markdown'
        )
    
    def test_send_message_no_channel(self):
        """Test sending a message without a channel ID."""
        sender = TelegramSender(token="fake_token")
        result = sender.send_message("Test message")
        
        self.assertFalse(result)
    
    @patch('telegram.Bot.send_message')
    def test_send_message_telegram_error(self, mock_send_message):
        """Test handling of Telegram errors when sending a message."""
        from telegram.error import TelegramError
        mock_send_message.side_effect = TelegramError("Test error")
        
        sender = TelegramSender(token="fake_token", channel_id="@test_channel")
        result = sender.send_message("Test message")
        
        self.assertFalse(result)
    
    def test_format_commit_message(self):
        """Test formatting a commit message for Telegram."""
        sender = TelegramSender(token="fake_token")
        
        commit_details = {
            'message': 'Test commit',
            'author': {
                'name': 'Test User',
                'email': 'test@example.com'
            },
            'html_url': 'https://github.com/user/repo/commit/abc123',
            'files_changed': [
                {'filename': 'test.py', 'status': 'modified'},
                {'filename': 'new.py', 'status': 'added'}
            ]
        }
        
        description = "This is a test description of the commit."
        
        message = sender.format_commit_message("Test Project", commit_details, description)
        
        self.assertIn("*Project:* Test Project", message)
        self.assertIn("*Commit Information:*", message)
        self.assertIn("- Author: Test User", message)
        self.assertIn("- Message: Test commit", message)
        self.assertIn("- Files Changed: 2", message)
        self.assertIn("- [View on GitHub](https://github.com/user/repo/commit/abc123)", message)
        self.assertIn("*Description:*", message)
        self.assertIn("This is a test description of the commit.", message)

if __name__ == '__main__':
    unittest.main()