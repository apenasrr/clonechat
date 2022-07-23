import argparse
from importlib.metadata import files
import json
import os
import time

import pyrogram
from pyrogram.errors import FloodWait

import credentials

CACHE_FILE = "posted.json"
DELAY_AMOUNT = 2

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


tg = pyrogram.Client(
    name="user",
    api_id=credentials.api_id,
    api_hash=credentials.api_hash,
    no_updates=True,
)
tg.start()


def foward_photo(message, destination_chat):

    caption = get_caption(message)
    photo_id = message.photo.file_id
    try:
        tg.send_photo(
            chat_id=destination_chat,
            photo=photo_id,
            caption=caption,
        )
    except FloodWait as e:
        time.sleep(e.value)
        tg.send_photo(
            chat_id=destination_chat,
            photo=photo_id,
            caption=caption,
        )


def foward_text(message, destination_chat):

    text = message.text.markdown
    try:
        tg.send_message(
            chat_id=destination_chat,
            text=text,
            disable_notification=True,
            disable_web_page_preview=True,
        )
    except FloodWait as e:
        time.sleep(e.value)
        tg.send_message(
            chat_id=destination_chat,
            text=text,
            disable_notification=True,
            disable_web_page_preview=True,
        )


def foward_sticker(message, destination_chat):

    sticker_id = message.sticker.file_id
    try:
        tg.send_sticker(chat_id=destination_chat, sticker=sticker_id)
    except FloodWait as e:
        time.sleep(e.value)
        tg.send_sticker(chat_id=destination_chat, sticker=sticker_id)


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
    except FloodWait as e:
        time.sleep(e.value)
        tg.send_document(
            chat_id=destination_chat,
            document=document_id,
            disable_notification=True,
            caption=caption,
        )


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
    except FloodWait as e:
        time.sleep(e.value)
        tg.send_animation(
            chat_id=destination_chat,
            animation=animation_id,
            disable_notification=True,
            caption=caption,
        )


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
    except FloodWait as e:
        time.sleep(e.value)
        tg.send_audio(
            chat_id=destination_chat,
            audio=audio_id,
            disable_notification=True,
            caption=caption,
        )


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
    except FloodWait as e:
        time.sleep(e.value)
        tg.send_voice(
            chat_id=destination_chat,
            voice=voice_id,
            disable_notification=True,
            caption=caption,
        )


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
    except FloodWait as e:
        time.sleep(e.x)
        tg.send_video(
            chat_id=destination_chat,
            video=video_id,
            disable_notification=True,
            caption=caption,
        )


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
    except FloodWait as e:
        time.sleep(e.value)
        tg.send_poll(
            chat_id=destination_chat,
            question=message.poll.question,
            options=[option.text for option in message.poll.options],
            is_anonymous=message.poll.is_anonymous,
            allows_multiple_answers=message.poll.allows_multiple_answers,
            disable_notification=True,
        )


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

    raise Exception


def get_message(origin_chat, message_id):

    try:
        message = tg.get_messages(origin_chat, message_id)
    except FloodWait as e:
        time.sleep(e.value)
        message = tg.get_messages(origin_chat, message_id)

    return message


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

def type_to_copy():
    opt = ''
    files_type_excluded = []
    print("Choose a type of file to send")
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
    print("Choose the number(s) above")
    print("For example, to copy documents and videos type: 3 8")
    opt = input("Your answer: ") 
    if not len(opt) or '0' in opt: 
        return files_type_excluded
    else:
        if '1' not in opt: 
            files_type_excluded += [foward_photo]
        if '2' not in opt:
            files_type_excluded += [foward_text]
        if '3' not in opt:
            files_type_excluded += [foward_document]
        if '4' not in opt:
            files_type_excluded += [foward_sticker]
        if '5' not in opt:
            files_type_excluded += [foward_animation]
        if '6' not in opt:
            files_type_excluded += [foward_audio]
        if '7' not in opt:
            files_type_excluded += [foward_voice]
        if '8' not in opt:
            files_type_excluded += [foward_video]
        if '9' not in opt:
            files_type_excluded += [foward_poll]

    return files_type_excluded

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


def wait_a_moment(message_id):

    if message_id != 1:
        time.sleep(DELAY_AMOUNT)


def update_cache(CACHE_FILE, list_posted):

    with open(CACHE_FILE, mode="w") as file:
        file.write(json.dumps(list_posted))


def get_last_message_id(origin_chat):

    iter_message = tg.get_chat_history(origin_chat)
    message = next(iter_message)
    return message.id


def main():
    files_type_excluded = type_to_copy()
    message_id = 0
    last_message_id = get_last_message_id(origin_chat)
    list_posted = get_list_posted()
    while message_id < last_message_id:
        message_id = message_id + 1
        if message_id in list_posted:
            continue

        wait_a_moment(message_id)
        message = get_message(origin_chat, message_id)

        if message.empty or message.service:
            list_posted += [message.id]
            continue

        func_sender = get_sender(message)
        if func_sender in files_type_excluded:
            list_posted += [message.id]
            update_cache(CACHE_FILE, list_posted)
            continue
        func_sender(message, destination_chat)

        list_posted += [message.id]

        update_cache(CACHE_FILE, list_posted)
        print(f"{message_id}/{last_message_id}")

    print("Finish chat cloning")


main()
