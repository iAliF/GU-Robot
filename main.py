from telegram.ext import Updater, PicklePersistence

import config

if __name__ == '__main__':
    updater: Updater = Updater(
        config.TOKEN,
        persistence=PicklePersistence(
            config.FILENAME,
            store_user_data=False,
            store_chat_data=False,
        )
    )
