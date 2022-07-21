import argparse
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

    origin_chat = int(input("Digite o id_chat de origem: "))
    destination_chat = int(input("Digite o id_chat de destino: "))
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
        posted += [message.id]
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


def get_list_posted():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, mode="r") as file:
            posted = json.loads(file.read())
    else:
        posted = []
    return posted


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

    message_id = 0
    last_message_id = get_last_message_id(origin_chat)

    list_posted = get_list_posted()

    while message_id < last_message_id:
        message_id = message_id + 1
        wait_a_moment(message_id)
        if message_id in list_posted:
            continue

        message = get_message(origin_chat, message_id)

        if message.empty or message.service:
            list_posted += [message.id]
            continue

        func_sender = get_sender(message)
        func_sender(message, destination_chat)

        list_posted += [message.id]

        update_cache(CACHE_FILE, list_posted)
        print(f"{message_id}/{last_message_id}")

    print("Finish chat cloning")


main()
