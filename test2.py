import apscheduler.schedulers.background as BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler  # Optional for continuous local execution

def your_code_to_run():
    # Replace this with your actual code logic
    print("Your code is running every 10 seconds!")

# Create a scheduler (choose either BackgroundScheduler or BlockingScheduler)
scheduler = BackgroundScheduler()  # For non-blocking execution

# Schedule the task to run every 10 seconds
scheduler.add_job(your_code_to_run, 'interval', seconds=10)

# Start the scheduler (if using BackgroundScheduler)
if __name__ == '__main__':
    scheduler.start()

# Alternatively, for continuous execution (blocking the main thread)
# scheduler = BlockingScheduler()
# scheduler.start()