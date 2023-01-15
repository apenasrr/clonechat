from __future__ import annotations

import argparse
import json
import os
import time
from configparser import ConfigParser
from pathlib import Path

import pyrogram
from pyrogram.errors import ChannelInvalid, FloodWait, PeerIdInvalid

from setup import version

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
        print(f"..FloodWait {e.value} seconds..")
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
        print(f"..FloodWait {e.value} seconds..")
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
        print(f"..FloodWait {e.value} seconds..")
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
        print(f"..FloodWait {e.value} seconds..")
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
        print(f"..FloodWait {e.value} seconds..")
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
        print(f"..FloodWait {e.value} seconds..")
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
        print(f"..FloodWait {e.value} seconds..")
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_voice(message, destination_chat)


def foward_video_note(message, destination_chat):

    video_note_id = message.video_note.file_id
    try:
        tg.send_video_note(
            chat_id=destination_chat,
            video_note=video_note_id,
            disable_notification=True,
        )
        return
    except FloodWait as e:
        print(f"..FloodWait {e.value} seconds..")
        time.sleep(e.value)
    except Exception as e:
        print(f"trying again... Due to: {e}")
        time.sleep(10)

    foward_video_note(message, destination_chat)


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
        print(f"..FloodWait {e.value} seconds..")
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
        print(f"..FloodWait {e.value} seconds..")
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
    if message.video_note:
        return foward_video_note
    if message.poll:
        return foward_poll

    print("\nNot recognized message type:\n")
    print(message)
    raise Exception


def get_input_type_to_copy():

    answer = ""
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
    return answer


def get_files_type_excluded_by_input(input_string):

    files_type_excluded = []
    if input_string == "" or "0" in input_string:
        return files_type_excluded
    else:
        if "1" not in input_string:
            files_type_excluded += [foward_photo]
        if "2" not in input_string:
            files_type_excluded += [foward_text]
        if "3" not in input_string:
            files_type_excluded += [foward_document]
        if "4" not in input_string:
            files_type_excluded += [foward_sticker]
        if "5" not in input_string:
            files_type_excluded += [foward_animation]
        if "6" not in input_string:
            files_type_excluded += [foward_audio]
        if "7" not in input_string:
            files_type_excluded += [foward_voice]
        if "8" not in input_string:
            files_type_excluded += [foward_video]
        if "9" not in input_string:
            files_type_excluded += [foward_poll]
        if len(files_type_excluded) == 9:
            print("Invalid option! Try again")
            return get_files_type_excluded_by_input(input_string)
    return files_type_excluded


def get_message(origin_chat, message_id):

    try:
        message = tg.get_messages(origin_chat, message_id)
        return message
    except FloodWait as e:
        print(f"..FloodWait {e.value} seconds..")
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


def get_list_posted(int_task_type):

    # 1 = new
    if int_task_type == 1:
        if os.path.exists(CACHE_FILE):
            os.remove(CACHE_FILE)
        return []
    else:  # 2 = resume
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
        FILES_TYPE_EXCLUDED = get_files_type_excluded_by_input(
            get_input_type_to_copy()
        )
        return FILES_TYPE_EXCLUDED


def is_empty_message(message, message_id, last_message_id) -> bool:

    if message.empty or message.service or message.dice or message.location:
        print(f"{message_id}/{last_message_id} (blank id)")
        wait_a_moment(message_id, skip=True)
        return True
    else:
        return False


def must_be_ignored(func_sender, message_id, last_message_id) -> bool:

    if func_sender in FILES_TYPE_EXCLUDED:
        print(f"{message_id}/{last_message_id} (skip by type)")
        wait_a_moment(message_id, skip=True)
        return True
    else:
        return False


def get_first_message_id(list_posted) -> int:

    if len(list_posted) > 0:
        message_id = list_posted[-1]
    else:
        message_id = 1
    return message_id


def ensure_folder_existence(folder_path):
    """If the folder does not exist, it creates

    Args:
        folder_path (str): folder path
    """

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def get_task_file(ORIGIN_CHAT_TITLE, destination_chat):

    ensure_folder_existence("user")
    ensure_folder_existence(os.path.join("user", "tasks"))
    task_file_name = f"{ORIGIN_CHAT_TITLE}-{destination_chat}.json"
    task_file_path = os.path.join("user", "tasks", task_file_name)
    return task_file_path


def check_chat_id(chat_id):

    try:
        chat_obj = tg.get_chat(chat_id)
        chat_title = chat_obj.title
        return chat_title
    except ChannelInvalid:  # When you are not part of the channel
        print("\nNon-accessible chat")
        if MODE == "bot":
            print(
                "\nCheck that the bot is part of the chat as an administrator."
                + "It is necessary for bot mode."
            )
        else:
            print("\nCheck that the user account is part of the chat.")
        return False
    except PeerIdInvalid:  # When the chat_id is invalid
        print(f"\nInvalid chat_id: {chat_id}")
        return False


def ensure_connection(client_name):

    if client_name == "user":
        if Path(f"{client_name}.session").exists():
            try:
                useraccount = pyrogram.Client(client_name)
                useraccount.start()
                return useraccount
            except:
                print("Delete Session file and try again.")

        while True:
            try:
                api_id = int(input("Enter your api_id: "))
                api_hash = input("Enter your api_hash: ")

                useraccount = pyrogram.Client("user", api_id, api_hash)
                useraccount.start()
                return useraccount
            except:
                print("\nError. Try again.\n")
                pass
    else:
        pass

    if client_name == "bot":
        if Path(f"{client_name}.session").exists():
            try:
                bot = pyrogram.Client(client_name)
                bot.start()
                return bot
            except:
                print("Delete Session file and try again.")

        while True:
            try:
                api_id = int(input("Enter your api_id: "))
                api_hash = input("Enter your api_hash: ")
                bot_token = input("Enter your bot_token: ")

                bot = pyrogram.Client(
                    client_name, api_id, api_hash, bot_token=bot_token
                )
                bot.start()
                return bot
            except:
                print("\nError. Try again.\n")
                pass


def main():

    print(
        f"\n....:: Clonechat - v{version} ::....\n"
        + "github.com/apenasrr/clonechat/\n"
    )

    global FILES_TYPE_EXCLUDED
    FILES_TYPE_EXCLUDED = get_files_type_excluded()
    last_message_id = get_last_message_id(origin_chat)

    global NEW
    if NEW is None:
        int_task_type = task_type()
    else:
        int_task_type = NEW
    list_posted = get_list_posted(int_task_type)

    message_id = get_first_message_id(list_posted)
    while message_id < last_message_id:
        message_id = message_id + 1
        if message_id in list_posted:
            continue

        message = get_message(origin_chat, message_id)

        if is_empty_message(message, message_id, last_message_id):
            list_posted += [message.id]
            continue

        func_sender = get_sender(message)

        if must_be_ignored(func_sender, message_id, last_message_id):
            list_posted += [message.id]
            update_cache(CACHE_FILE, list_posted)
            continue

        func_sender(message, destination_chat)
        print(f"{message_id}/{last_message_id}")

        list_posted += [message.id]
        update_cache(CACHE_FILE, list_posted)

        wait_a_moment(message_id)

    print(
        "\nChat cloning finished! :)\n"
        + "If you are not going to continue this task for these chats, "
        + "delete the posted.json file"
    )


config_data = get_config_data(
    path_file_config=os.path.join("user", "config.ini")
)

USER_DELAY_SECONDS = float(config_data.get("user_delay_seconds"))
BOT_DELAY_SECONDS = float(config_data.get("bot_delay_seconds"))
SKIP_DELAY_SECONDS = float(config_data.get("skip_delay_seconds"))

parser = argparse.ArgumentParser()
parser.add_argument("--orig", help="chat_id of origin channel/group")
parser.add_argument("--dest", help="chat_id of destination channel/group")
parser.add_argument(
    "--mode",
    choices=["user", "bot"],
    help='"user" is slow. "bot" requires token_bot in credentials',
)
parser.add_argument(
    "--new", type=int, choices=[1, 2], help="1 = new, 2 = resume"
)
help_type = """list separated by comma of message type to be clonned:
Ex. for documents and videos: 3,8 || Options:
0 = All files
1 = Photos
2 = Text
3 = Documents (pdf, zip, rar...)
4 = Stickers
5 = Animation
6 = Audio files (music
7 = Voice message
8 = Videos
9 = Polls"""
parser.add_argument("--type", help=help_type)
options = parser.parse_args()

if options.mode is None:
    MODE = config_data.get("mode")
else:
    MODE = options.mode


useraccount = ensure_connection("user")
print(f"{MODE=}")
if MODE == "bot":
    bot = ensure_connection("bot")
    tg = bot
    DELAY_AMOUNT = BOT_DELAY_SECONDS

if MODE == "user":
    tg = useraccount
    DELAY_AMOUNT = USER_DELAY_SECONDS

DELAY_SKIP = SKIP_DELAY_SECONDS

NEW = options.new

if options.orig is None:  # Menu interface
    while True:
        origin_chat = int(input("Enter the origin id_chat:"))
        ORIGIN_CHAT_TITLE = check_chat_id(origin_chat)
        if ORIGIN_CHAT_TITLE:
            break
else:  # CLI interface
    origin_chat = int(options.orig)
    ORIGIN_CHAT_TITLE = check_chat_id(origin_chat)
    if ORIGIN_CHAT_TITLE is False:
        raise AttributeError("Fix the origin chat_id")
    FILES_TYPE_EXCLUDED = []
    if NEW is None:
        NEW = 1
    else:
        NEW = int(NEW)

if options.dest is None:  # Menu interface
    while True:
        destination_chat = int(input("Enter the destination id_chat:"))
        DESTINATION_CHAT_TITLE = check_chat_id(origin_chat)
        if DESTINATION_CHAT_TITLE:
            break
else:  # CLI interface
    destination_chat = int(options.dest)
    DESTINATION_CHAT_TITLE = check_chat_id(origin_chat)
    if DESTINATION_CHAT_TITLE is False:
        raise AttributeError("Fix the destination chat_id")

if options.type is None:
    pass
else:
    TYPE = options.type
    FILES_TYPE_EXCLUDED = get_files_type_excluded_by_input(TYPE)

CACHE_FILE = get_task_file(ORIGIN_CHAT_TITLE, destination_chat)

main()
