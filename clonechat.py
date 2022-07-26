import argparse
import json
import os
import time
from configparser import ConfigParser

import pyrogram
from pyrogram.errors import FloodWait

import credentials
from setup import version

CACHE_FILE = "posted.json"
DELAY_AMOUNT = 10


def get_config_data(path_file_config):
    """get default configuration data from file config.ini

    Returns:
        dict: config data
    """

    config_file = ConfigParser()
    config_file.read(path_file_config)
    default_config = dict(config_file["default"])
    return default_config


def check_bot_token():

    if hasattr(credentials, "bot_token"):
        pass
    else:
        raise AttributeError(
            "bot_token not found in credentials.py. "
            + "Fill a token_bot ou change the mode to 'user'."
        )


def foward_photo(message, destination_chat):

    caption = get_caption(message)
    photo_id = message.photo.file_id
    try:
        tg.send_photo(
            chat_id=destination_chat,
            photo=photo_id,
            caption=caption,
        )
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_photo(message, destination_chat)


def foward_text(message, destination_chat):

    text = message.text.markdown
    try:
        tg.send_message(
            chat_id=destination_chat,
            text=text,
            disable_notification=True,
            disable_web_page_preview=True,
        )
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_text(message, destination_chat)


def foward_sticker(message, destination_chat):

    sticker_id = message.sticker.file_id
    try:
        tg.send_sticker(chat_id=destination_chat, sticker=sticker_id)
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_sticker(message, destination_chat)


def foward_document(message, destination_chat):

    caption = get_caption(message)
    document_id = message.document.file_id
    try:
        tg.send_document(
            chat_id=destination_chat,
            document=document_id,
            disable_notification=True,
            caption=caption,
        )
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_document(message, destination_chat)


def foward_animation(message, destination_chat):

    caption = get_caption(message)
    animation_id = message.animation.file_id
    try:
        tg.send_animation(
            chat_id=destination_chat,
            animation=animation_id,
            disable_notification=True,
            caption=caption,
        )
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_animation(message, destination_chat)


def foward_audio(message, destination_chat):

    caption = get_caption(message)
    audio_id = message.audio.file_id
    try:
        tg.send_audio(
            chat_id=destination_chat,
            audio=audio_id,
            disable_notification=True,
            caption=caption,
        )
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_audio(message, destination_chat)


def foward_voice(message, destination_chat):

    caption = get_caption(message)
    voice_id = message.voice.file_id
    try:
        tg.send_voice(
            chat_id=destination_chat,
            voice=voice_id,
            disable_notification=True,
            caption=caption,
        )
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_voice(message, destination_chat)


def foward_video(message, destination_chat):

    caption = get_caption(message)
    video_id = message.video.file_id
    try:
        tg.send_video(
            chat_id=destination_chat,
            video=video_id,
            disable_notification=True,
            caption=caption,
        )
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_video(message, destination_chat)


def foward_poll(message, destination_chat):

    if message.poll.type != "regular":
        return
    try:
        tg.send_poll(
            chat_id=destination_chat,
            question=message.poll.question,
            options=[option.text for option in message.poll.options],
            is_anonymous=message.poll.is_anonymous,
            allows_multiple_answers=message.poll.allows_multiple_answers,
            disable_notification=True,
        )
        return
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_poll(message, destination_chat)


def get_caption(message):

    if message.caption:
        caption = message.caption.markdown
    else:
        caption = None
    return caption


def get_sender(message):

    if message.empty or message.service:
        return None

    if message.photo:
        return foward_photo
    if message.text:
        return foward_text
    if message.document:
        return foward_document
    if message.sticker:
        return foward_sticker
    if message.animation:
        return foward_animation
    if message.audio:
        return foward_audio
    if message.voice:
        return foward_voice
    if message.video:
        return foward_video
    if message.poll:
        return foward_poll

    print(f"\nNot recognized message type:\n")
    print(message)
    raise Exception


def type_to_copy():

    answer = ""
    files_type_excluded = []
    print("0 - All files")
    print("1 - Photos")
    print("2 - Text")
    print("3 - Documents (pdf, zip, rar, ...)")
    print("4 - Stickers")
    print("5 - Animation")
    print("6 - Audio files (music)")
    print("7 - Voice message")
    print("8 - Videos")
    print("9 - Polls\n")
    print(
        "Enter the number(s) of the file type to clone, separating by comma."
    )
    print("For example, to copy photos and documents type: 1,3")
    answer = input("Your answer: ")
    if not len(answer) or "0" in answer:
        return files_type_excluded
    else:
        if "1" not in answer:
            files_type_excluded += [foward_photo]
        if "2" not in answer:
            files_type_excluded += [foward_text]
        if "3" not in answer:
            files_type_excluded += [foward_document]
        if "4" not in answer:
            files_type_excluded += [foward_sticker]
        if "5" not in answer:
            files_type_excluded += [foward_animation]
        if "6" not in answer:
            files_type_excluded += [foward_audio]
        if "7" not in answer:
            files_type_excluded += [foward_voice]
        if "8" not in answer:
            files_type_excluded += [foward_video]
        if "9" not in answer:
            files_type_excluded += [foward_poll]
        if len(files_type_excluded) == 9:
            print("Invalid option! Try again")
            return type_to_copy()
    return files_type_excluded


def get_message(origin_chat, message_id):

    try:
        message = tg.get_messages(origin_chat, message_id)
        return message
    except FloodWait as e:
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    return get_message(origin_chat, message_id)


def task_type():

    print("New cloning or continuation?\n1 = new\n2 = resume")
    answer = input("Your answer: ")
    if answer == "1":
        return 1
    elif answer == "2":
        return 2
    else:
        print("\nInvalid answer.\n")
        return task_type()


def get_list_posted():

    answer = task_type()
    if answer == 1:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        return []
    else:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, mode="r") as file:
                posted = json.loads(file.read())
                return posted
        else:
            return []


def wait_a_moment(message_id, skip=False):

    if message_id != 1:
        if skip:
            time.sleep(DELAY_SKIP)
        else:
            time.sleep(DELAY_AMOUNT)


def update_cache(CACHE_FILE, list_posted):

    with open(CACHE_FILE, mode="w") as file:
        file.write(json.dumps(list_posted))


def get_last_message_id(origin_chat):

    iter_message = useraccount.get_chat_history(origin_chat)
    message = next(iter_message)
    return message.id


def get_files_type_excluded():

    global FILES_TYPE_EXCLUDED
    try:
        FILES_TYPE_EXCLUDED = FILES_TYPE_EXCLUDED
        return FILES_TYPE_EXCLUDED
    except:
        FILES_TYPE_EXCLUDED = type_to_copy()
        return FILES_TYPE_EXCLUDED


def main():

    print(
        f"\n....:: Clonechat - v{version} ::....\n"
        + f"github.com/apenasrr/clonechat/\n"
    )
    FILES_TYPE_EXCLUDED = get_files_type_excluded()
    message_id = 0
    last_message_id = get_last_message_id(origin_chat)
    list_posted = get_list_posted()
    while message_id < last_message_id:
        message_id = message_id + 1
        if message_id in list_posted:
            continue

        message = get_message(origin_chat, message_id)

        if message.empty or message.service:
            list_posted += [message.id]
            print(f"{message_id}/{last_message_id} (blank id)")
            wait_a_moment(message_id, skip=True)
            continue
        func_sender = get_sender(message)

        # skip message from a particular type
        if func_sender in FILES_TYPE_EXCLUDED:
            print(f"{message_id}/{last_message_id} (skip by type)")
            list_posted += [message.id]
            update_cache(CACHE_FILE, list_posted)
            continue

        func_sender(message, destination_chat)
        list_posted += [message.id]
        update_cache(CACHE_FILE, list_posted)
        print(f"{message_id}/{last_message_id}")
        wait_a_moment(message_id)

    print(
        "\nChat cloning finished! :)\n"
        + "If you are not going to continue this task for these chats, "
        + "delete the posted.json file"
    )


config_data = get_config_data(path_file_config="config.ini")
MODE = config_data.get("mode")
USER_DELAY_SECONDS = float(config_data.get("user_delay_seconds"))
BOT_DELAY_SECONDS = float(config_data.get("bot_delay_seconds"))
SKIP_DELAY_SECONDS = float(config_data.get("skip_delay_seconds"))

parser = argparse.ArgumentParser()
parser.add_argument("--orig")
parser.add_argument("--dest")
options = parser.parse_args()

if options.orig is None:

    origin_chat = int(input("Enter the origin id_chat:"))
    destination_chat = int(input("Enter the destination id_chat:"))
else:
    origin_chat = int(options.orig)
    destination_chat = int(options.dest)
    FILES_TYPE_EXCLUDED = []


useraccount = pyrogram.Client(
    name="user",
    api_id=credentials.api_id,
    api_hash=credentials.api_hash,
    no_updates=True,
)
useraccount.start()

if MODE == "bot":

    check_bot_token()
    bot = pyrogram.Client(
        "bot",
        bot_token=credentials.bot_token,
        api_id=credentials.api_id,
        api_hash=credentials.api_hash,
    )

    bot.start()
    tg = bot
    DELAY_AMOUNT = BOT_DELAY_SECONDS

if MODE == "user":
    tg = useraccount
    DELAY_AMOUNT = USER_DELAY_SECONDS

DELAY_SKIP = SKIP_DELAY_SECONDS

main()
