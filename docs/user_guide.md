# Smart Commit Messenger - User Guide

## Overview

Smart Commit Messenger is a tool that automatically analyzes changes in a GitHub repository, generates simple and understandable descriptions using AI, and sends them to a Telegram channel. This guide will help you set up and use the tool effectively.

## Installation

1. Clone the repository to your local machine:
   ```
   git clone <repository-url>
   cd smart-commit-messenger
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables by creating a `.env` file in the root directory (see Configuration section).

4. Customize the `config/config.yaml` file to match your specific needs.

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
GITHUB_TOKEN=your_github_personal_access_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

#### How to obtain the required tokens:

1. **GitHub Personal Access Token**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Generate new token
   - Select the `repo` scope to allow access to your repositories
   - Copy the generated token and add it to your `.env` file

2. **Telegram Bot Token**:
   - Open Telegram and search for @BotFather
   - Send the command `/newbot` and follow the instructions
   - Once created, you'll receive a token for your bot
   - Add the bot to your channel as an administrator

3. **OpenAI API Key**:
   - Create an account on OpenAI's platform
   - Navigate to the API section and create a new API key
   - Copy the key to your `.env` file

### Configuration File

Edit the `config/config.yaml` file to set your specific configuration:

```yaml
github:
  repository: "username/repository"  # Your GitHub repository in format username/repo
  branch: "main"                    # The branch to monitor
  commit_limit: 5                    # Number of recent commits to analyze

telegram:
  channel_id: "@your_channel_name"   # Your Telegram channel ID

schedule:
  interval_minutes: 15               # How often to check for new commits
  continuous: true                   # Whether to run continuously

ai:
  model: "gpt-3.5-turbo"             # OpenAI model to use
  max_tokens: 500                    # Maximum tokens for the response
```

## Usage

### Running Once

To run the tool once and analyze the latest commits:

```
python src/main.py
```

### Scheduled Execution

To run the tool on a schedule based on your configuration:

```
python src/scheduler.py
```

This will start the scheduler, which will run at the interval specified in your configuration file.

## Understanding the Output

The tool sends messages to your Telegram channel in the following format:

```
**Project:** [Project name]
**Commit Information:**
- Author: [Author name]
- Message: [Commit message]
- Files Changed: [Number of files]
- [View on GitHub](commit-url)

**Description:**
[AI-generated description of the changes]
```

The description includes:
1. A summary of what changed in simple terms
2. The potential impact of these changes on the project
3. Important information for non-technical team members

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Ensure your GitHub token has the correct permissions
   - Verify that your Telegram bot token is valid and the bot is an admin in the channel

2. **Rate Limiting**:
   - If you encounter rate limiting from GitHub or OpenAI, consider increasing the interval between checks

3. **Missing Messages**:
   - Check that your bot has permission to post messages in the channel
   - Verify the channel ID is correct in your configuration

### Logs

Check the log files for detailed information about any errors:
- `smart_commit_messenger.log` - For the main application
- `scheduler.log` - For the scheduler

## Extending the Tool

The tool is designed to be modular, making it easy to extend its functionality:

- Modify `github_client.py` to change how repository data is fetched
- Update `commit_analyzer.py` to customize the AI analysis
- Edit `telegram_sender.py` to change the message format or add other communication channels

## License

This project is licensed under the MIT License - see the LICENSE file for details.