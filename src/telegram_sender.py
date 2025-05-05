import os
import logging
import telegram
from telegram.error import TelegramError

class TelegramSender:
    """Handles sending messages to Telegram channels."""
    
    def __init__(self, token=None, channel_id=None):
        """
        Initialize the Telegram sender.
        
        Args:
            token (str, optional): Telegram bot token. Defaults to None.
            channel_id (str, optional): Telegram channel ID. Defaults to None.
        """
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("Telegram bot token is required. Set it in .env file or pass it to the constructor.")
        
        self.channel_id = channel_id
        self.bot = telegram.Bot(token=self.token)
    
    def set_channel(self, channel_id):
        """
        Set the channel ID for sending messages.
        
        Args:
            channel_id (str): Telegram channel ID.
        """
        self.channel_id = channel_id
    
    def send_message(self, message, channel_id=None):
        """
        Send a message to the Telegram channel.
        
        Args:
            message (str): Message to send.
            channel_id (str, optional): Channel ID to send the message to. Defaults to None.
            
        Returns:
            bool: True if message was sent successfully, False otherwise.
        """
        target_channel = channel_id or self.channel_id
        if not target_channel:
            logging.error("Channel ID is required. Set it with set_channel() or pass it to send_message().")
            return False
        
        try:
            self.bot.send_message(
                chat_id=target_channel,
                text=message,
                parse_mode='Markdown'
            )
            logging.info(f"Message sent to channel {target_channel}")
            return True
        except TelegramError as e:
            logging.error(f"Failed to send message to Telegram: {str(e)}")
            return False
    
    def format_commit_message(self, project_name, commit_details, description):
        """
        Format a commit message for Telegram.
        
        Args:
            project_name (str): Name of the project.
            commit_details (dict): Dictionary containing commit details.
            description (str): AI-generated description of the commit.
            
        Returns:
            str: Formatted message for Telegram.
        """
        if not commit_details:
            return ""
        
        # Extract commit information
        commit_message = commit_details.get('message', 'No commit message')
        author_name = commit_details.get('author', {}).get('name', 'Unknown')
        commit_url = commit_details.get('html_url', '')
        
        # Count of files changed
        files_count = len(commit_details.get('files_changed', []))
        
        # Format the message
        message = f"*Project:* {project_name}\n\n"
        message += f"*Commit Information:*\n"
        message += f"- Author: {author_name}\n"
        message += f"- Message: {commit_message}\n"
        message += f"- Files Changed: {files_count}\n"
        
        if commit_url:
            message += f"- [View on GitHub]({commit_url})\n"
        
        message += f"\n*Description:*\n{description}"
        
        return message