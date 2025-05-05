# Smart Commit Messenger

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A tool that automatically analyzes changes in a GitHub repository, generates simple and understandable descriptions using AI, and sends them to a Telegram channel.

## Features

- **Automated Commit Analysis**: Monitors GitHub repositories for new commits
- **AI-Powered Descriptions**: Uses OpenAI to generate human-readable summaries of code changes
- **Telegram Integration**: Sends commit summaries directly to your Telegram channel
- **Flexible Scheduling**: Run once or continuously at specified intervals
- **Customizable Configuration**: Easily adjust settings through YAML configuration

## Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/yourusername/smart-commit-messenger.git
   cd smart-commit-messenger
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables by copying the template:
   ```
   cp .env.template .env
   ```
   Then edit the `.env` file with your API keys and tokens.

4. Customize the `config/config.yaml` file to match your specific needs.

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
GITHUB_TOKEN=your_github_personal_access_token
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

See the [User Guide](docs/user_guide.md) for detailed instructions on obtaining these tokens.

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

## Project Structure

```
smart-commit-messenger/
├── config/                # Configuration files
│   └── config.yaml       # Main configuration
├── docs/                 # Documentation
│   └── user_guide.md     # Detailed user guide
├── src/                  # Source code
│   ├── commit_analyzer.py # AI-powered commit analysis
│   ├── github_client.py  # GitHub API interactions
│   ├── main.py           # Main application entry point
│   ├── scheduler.py      # Scheduling functionality
│   └── telegram_sender.py # Telegram messaging
├── tests/                # Test suite
├── .env.template         # Template for environment variables
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [OpenAI](https://openai.com/) for providing the AI models
- [PyGithub](https://github.com/PyGithub/PyGithub) for GitHub API integration
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for Telegram integration