"""48 IX Particpant Route Server Config Management."""

# Standard Library
import sys
import asyncio
import logging
from datetime import datetime

# Third Party
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Project
from routingpolicy import APP_DIR
from routingpolicy.log import log
from routingpolicy.run import policy
from routingpolicy.config import params
from routingpolicy.api.main import start_api

logger = logging.getLogger("routingpolicy")

interval = IntervalTrigger(
    minutes=params.interval, start_date=datetime(2020, 9, 18, 6, 0, 0, 0)
)


class PrintJobs:
    """File-Like Object for APScheduler to Print Jobs towards."""

    @staticmethod
    def write(message: str) -> None:
        """Log job details."""
        msg = message.strip().rstrip()
        if msg and "Jobstore" not in msg:
            log.info("Job: {}", msg)


if __name__ == "__main__":
    # Ensure main app directory exists.
    if not APP_DIR.exists():
        APP_DIR.mkdir()

    loop = asyncio.new_event_loop()

    # Initialize scheduler.
    scheduler = AsyncIOScheduler(logger=logger, timezone="Etc/UTC", event_loop=loop)

    # Run RPC API
    scheduler.add_job(start_api, id="api")

    # Run Route Policy Updater
    scheduler.add_job(policy, id="policies", trigger=interval)

    scheduler.start()
    scheduler.print_jobs(out=PrintJobs)

    try:
        log.success("Starting 48 IX Routing Policy Server...")
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        log.critical("Stopping 48 IX Routing Policy Server...")
        sys.exit(1)
