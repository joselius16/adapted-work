# scheduler_service.py
import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from adapted_work.scheduler.interact_historic import execute_scheduler

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function of scheduler."""
    scheduler = BackgroundScheduler()

    # Job
    scheduler.add_job(
        execute_scheduler,
        CronTrigger(hour=10, minute=0),
        id='daily_historic_job',
        name='Execute Historic Scheduler Daily'
    )

    try:
        scheduler.start()
        logger.info("Scheduler executed.")

        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Closing scheduler...")
        scheduler.shutdown()

if __name__ == "__main__":
    main()
