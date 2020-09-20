"""48 IX Particpant Route Server Config Management."""
# Standard Library
import sys
import asyncio
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

if __name__ == "__main__":
    if not APP_DIR.exists():
        APP_DIR.mkdir()
    loop = asyncio.new_event_loop()
    scheduler = AsyncIOScheduler(logger=log, timezone="Etc/UTC", event_loop=loop)
    scheduler.add_job(start_api, id="api")
    scheduler.add_job(
        policy,
        id="policies",
        trigger=IntervalTrigger(
            minutes=params.interval, start_date=datetime(2020, 9, 18, 6, 0, 0, 0)
        ),
    )
    scheduler.start()
    try:
        log.success("Starting 48 IX Routing Policy Server...")
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        log.critical("Stopping 48 IX Routing Policy Server...")
        sys.exit(1)
