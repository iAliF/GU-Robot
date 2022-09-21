from datetime import datetime

from telegram.ext import Updater, PicklePersistence, CallbackContext, JobQueue

import config


def do_job(context: CallbackContext):
    pass


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
