import logging
from datetime import datetime
from typing import List

from telegram.ext import Updater, PicklePersistence, CallbackContext, JobQueue

import config
from resources import *

to_check = {
    'news': News(),
    'notifications': Notifications()
}

logger = logging.getLogger('Main')
logger.setLevel(logging.DEBUG)


def set_latest_items(context: CallbackContext) -> None:
    if is_set(context):
        return

    for name, klass in to_check.items():
        klass.log(logging.DEBUG, 'Setting latest item')

        try:
            set_latest_url(context, name, klass.get_latest_item())
            klass.log(logging.DEBUG, 'Latest item has been set')
        except GUException:
            klass.log(logging.ERROR, 'cannot set data')
            jq.run_once(set_latest_items, 60)
            break


def do_job(context: CallbackContext) -> None:
    if not is_set(context):
        logger.debug('Waiting for latest items to be set')
        return

    for name, klass in to_check.items():
        try:
            latest = klass.get_latest_item()
            if latest.url == (latest_url := get_latest_url(context, name)):
                continue

            items = fetch_items(klass, latest_url)
            # Todo: Send to channel
            # Todo: set latest item

        except GUException:
            klass.log(logging.ERROR, "Couldn't fetch the data")


def fetch_items(klass: Base, latest_url: str) -> List[Item]:
    fetched_items: List[Item] = []
    klass_items = klass.get_all_items()
    page = 1

    while True:
        if len(klass_items) == 0:
            page += 1
            klass_items = klass.get_all_items(page)

        item = klass_items.pop(0)
        if item.url == latest_url:
            break

        fetched_items.append(item)

    return fetched_items


def set_latest_url(context: CallbackContext, name: str, item: Item) -> None:
    context.bot_data[name] = item.url


def get_latest_url(context: CallbackContext, name: str) -> str:
    return context.bot_data.get(name, None)


def is_set(context: CallbackContext) -> bool:
    return get_latest_url(context, list(to_check.keys())[0]) is not None


if __name__ == '__main__':
    updater: Updater = Updater(
        config.TOKEN,
        persistence=PicklePersistence(
            config.FILENAME,
            store_user_data=False,
            store_chat_data=False,
        )
    )
    jq: JobQueue = updater.job_queue

    jq.run_once(set_latest_items, 5)

    now_minute = datetime.now().minute
    if (first := (config.INTERVAL - (now_minute % config.INTERVAL))) == config.INTERVAL:
        first = 0

    jq.run_repeating(
        do_job,
        config.INTERVAL * 60,
        first * 60
    )

    jq.start()
    updater.idle()
