import time
import logging
import schedule
import sys
from main import SmartCommitMessenger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('scheduler.log')
    ]
)

class CommitMessengerScheduler:
    """Scheduler for running the Smart Commit Messenger at regular intervals."""
    
    def __init__(self, config_path='../config/config.yaml'):
        """
        Initialize the scheduler.
        
        Args:
            config_path (str, optional): Path to the configuration file. Defaults to '../config/config.yaml'.
        """
        self.messenger = SmartCommitMessenger(config_path=config_path)
        self.config = self.messenger.config
        self.interval = self.config.get('schedule', {}).get('interval_minutes', 15)
        self.continuous = self.config.get('schedule', {}).get('continuous', True)
    
    def job(self):
        """The job to run at scheduled intervals."""
        logging.info("Running scheduled commit analysis job")
        try:
            self.messenger.process_latest_commits()
            logging.info("Scheduled job completed successfully")
        except Exception as e:
            logging.error(f"Error in scheduled job: {str(e)}")
    
    def run(self):
        """Run the scheduler."""
        logging.info(f"Starting scheduler with {self.interval} minute intervals")
        
        # Schedule the job
        schedule.every(self.interval).minutes.do(self.job)
        
        # Run the job immediately once
        self.job()
        
        # Keep the scheduler running
        if self.continuous:
            logging.info("Running in continuous mode. Press Ctrl+C to exit.")
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Scheduler stopped by user")
        else:
            # Run pending jobs and exit
            schedule.run_pending()
            logging.info("Scheduler completed one-time execution")

def main():
    """Main function to run the scheduler."""
    try:
        scheduler = CommitMessengerScheduler()
        scheduler.run()
    except Exception as e:
        logging.error(f"Error running scheduler: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())