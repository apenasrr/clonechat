from __future__ import annotations

import asyncio
import collections
import json
import time
from pathlib import Path

import pyrogram

from ..utils.csv_util import open_csv, save_csv
from ..utils.progress_bar import progress_bar
from ..utils.timeout import time_out


async def get_next_to_upload(
    cloneplan_path: Path, loop_seconds: int = 5
) -> int:
    """returns the smallest message_id not yet cloned
    Message_id is authorized for cloning when its clone flag = "1"
    If all message_id have been cloned, returns value "0".
    If there are still message_id to be cloned but at the moment
    there are no authorized, make available available every x seconds.
    Args:
        cloneplan_path (Path): _description_

    Returns:
        int: message_id. 0 If there was no more messages to clone
    """

    while True:
        list_data = open_csv(cloneplan_path)
        dict_data = collections.OrderedDict(
            sorted({int(item["id"]): item for item in list_data}.items())
        )  # ordered from the smallest ID to the largest

        # Check if everything has been cloned. If yes, it returns zero
        clone_done = True
        for row_data in dict_data.values():
            if row_data["clone"] == "0":
                clone_done = False
                break
        if clone_done:
            return 0

        # Se nao, opera em loop buscando proximo message_id para ser clonado
        for message_id in dict_data.keys():
            if (
                dict_data[message_id].get("download", "") == "1"
                and dict_data[message_id].get("clone", "") == "0"
            ):
                return message_id
        await asyncio.sleep(loop_seconds)


def get_caption(message_id: int, file_path_hist: Path) -> str:

    list_dict_msg = json.loads(open(file_path_hist, "r").read())
    caption = ""
    for dict_msg in list_dict_msg:
        if dict_msg["id"] == message_id:
            caption = dict_msg.get("caption", "")
            break
    return caption


async def send_video(
    client_name: str,
    session_folder: Path,
    chat_id,
    file_path: Path,
    caption: str,
) -> Path:

    client = pyrogram.Client(client_name, workdir=session_folder)
    await client.start()

    c_time = time.time()
    prefix = "UP"
    await client.send_video(
        chat_id,
        file_path,
        caption=caption,
        progress=progress_bar,
        progress_args=(c_time, prefix),
        supports_streaming=True,
    )
    await client.stop()
    return file_path


async def send_document(
    client_name: str,
    session_folder: Path,
    chat_id: int,
    file_path: Path,
    caption: str,
) -> Path:

    client = pyrogram.Client(client_name, workdir=session_folder)
    await client.start()

    c_time = time.time()
    await client.send_document(
        chat_id,
        str(file_path),
        caption=caption,
        progress=progress_bar,
        progress_args=(c_time,),
    )
    await client.stop()
    return file_path


async def send_photo(
    client_name: str,
    session_folder: Path,
    chat_id: int,
    file_path: Path,
    caption: str,
) -> Path:

    client = pyrogram.Client(client_name, workdir=session_folder)
    await client.start()

    await client.send_photo(
        chat_id,
        str(file_path),
        caption=caption,
    )
    await client.stop()
    return file_path


async def send_audio(
    client_name: str,
    session_folder: Path,
    chat_id: int,
    file_path: Path,
    caption: str,
) -> Path:

    client = pyrogram.Client(client_name, workdir=session_folder)
    await client.start()

    await client.send_audio(
        chat_id,
        file_path,
        caption=caption,
    )
    await client.stop()
    return file_path


async def send_voice(
    client_name: str,
    session_folder: Path,
    chat_id: int,
    file_path: Path,
    caption: str,
) -> Path:

    client = pyrogram.Client(client_name, workdir=session_folder)
    await client.start()

    await client.send_voice(
        chat_id,
        file_path,
        caption=caption,
    )
    await client.stop()
    return file_path


def get_sticker_id(message_id: int, file_path_hist: Path) -> str:

    list_dict_msg = json.loads(open(file_path_hist, "r").read())
    caption = ""
    for dict_msg in list_dict_msg:
        if dict_msg["id"] == message_id:
            caption = dict_msg["sticker"].get("file_id", "")
            break
    return caption


async def send_sticker(
    client_name: str, session_folder: Path, chat_id: int, sticker_id: str
):

    client = pyrogram.Client(client_name, workdir=session_folder)
    await client.start()

    await client.send_sticker(
        chat_id,
        sticker=sticker_id,
    )
    await client.stop()


def get_text(message_id: int, file_path_hist: Path) -> str:

    list_dict_msg = json.loads(open(file_path_hist, "r").read())
    caption = ""
    for dict_msg in list_dict_msg:
        if dict_msg["id"] == message_id:
            caption = dict_msg.get("text", "")
            break
    return caption


async def send_message(
    client_name: str, session_folder: Path, chat_id: int, text: str
):

    client = pyrogram.Client(client_name, workdir=session_folder)
    await client.start()

    await client.send_message(
        chat_id,
        text=text,
    )
    await client.stop()


async def upload_media(
    client_name: str,
    session_folder: Path,
    chat_id: int,
    message_id: int,
    cloneplan_path: Path,
    history_path: Path,
    auto_restart: int,
):
    """Cloning any message_id

    Args:
        client_name (str):
        session_folder (Path):
        client (pyrogram.Client): _description_
        chat_id (int): _description_
        message_id (int): _description_
        cloneplan_path (Path): _description_
        download_folder (Path): _description_
        auto_restart (int): Restart upload if it takes longer than the definite amount of minutes
    """

    auto_restart_seconds = 60 * auto_restart
    # file_path
    #  get from cloneplan report because file_name is in different locations
    #  depending the message type (video, document, photo, audio, voice)
    list_data = open_csv(cloneplan_path)

    dict_data = collections.OrderedDict(
        sorted(
            {int(row_data["id"]): row_data for row_data in list_data}.items()
        )
    )

    # video, document, photo, audio, voice, text, sticker
    message_type = dict_data[message_id]["type"]

    file_path = dict_data[message_id]["file_path"]
    caption = get_caption(message_id, history_path)
    print(f"up: {Path(file_path).name}")
    if message_type == "video":
        # await send_video(
        #     client_name, session_folder, chat_id, file_path, caption
        # )
        time_out(
            auto_restart_seconds,
            send_video,
            {
                "client_name": client_name,
                "session_folder": session_folder,
                "chat_id": chat_id,
                "file_path": file_path,
                "caption": caption,
            },
            True,
        )

    if message_type == "document":
        # await send_document(
        #     client_name, session_folder, chat_id, file_path, caption
        # )
        time_out(
            auto_restart_seconds,
            send_document,
            {
                "client_name": client_name,
                "session_folder": session_folder,
                "chat_id": chat_id,
                "file_path": file_path,
                "caption": caption,
            },
            True,
        )
    if message_type == "photo":
        await send_photo(
            client_name, session_folder, chat_id, file_path, caption
        )
    if message_type == "audio":
        # await send_audio(
        #     client_name, session_folder, chat_id, file_path, caption
        # )
        time_out(
            auto_restart_seconds,
            send_audio,
            {
                "client_name": client_name,
                "session_folder": session_folder,
                "chat_id": chat_id,
                "file_path": file_path,
                "caption": caption,
            },
            True,
        )
    if message_type == "voice":
        # await send_voice(
        #     client_name, session_folder, chat_id, file_path, caption
        # )
        time_out(
            auto_restart_seconds,
            send_voice,
            {
                "client_name": client_name,
                "session_folder": session_folder,
                "chat_id": chat_id,
                "file_path": file_path,
                "caption": caption,
            },
            True,
        )
    if message_type == "sticker":
        sticker_id = get_sticker_id(message_id, history_path)
        await send_sticker(client_name, session_folder, chat_id, sticker_id)
    if message_type == "text":
        text = get_text(message_id, history_path)
        await send_message(client_name, session_folder, chat_id, text)
    print("")


def set_clone(cloneplan_path: Path, message_id: int):

    list_data = open_csv(cloneplan_path)
    for data in list_data:
        if data["id"] == str(message_id):
            data["clone"] = 1
            break
    save_csv(list_data, cloneplan_path)


def delete_local_media(cloneplan_path: Path, message_id: int):

    list_data = open_csv(cloneplan_path)
    dict_data = collections.OrderedDict(
        sorted(
            {int(row_data["id"]): row_data for row_data in list_data}.items()
        )
    )
    file_path = dict_data[message_id]["file_path"]
    if Path(file_path).exists() and file_path != "":
        Path(file_path).unlink()


async def pipe_upload(
    client_name: str,
    session_folder: Path,
    chat_id: int,
    cloneplan_path: Path,
    history_path: Path,
    auto_restart: int = 20,
):
    """Upload all message_id in ascending order.
    Mark in the cloneplan_path file the flag clone
    whenever finish the upload of a file.

    Args:
        client_name (str):
        session_folder (Path):
        chat_id (int): _description_
        cloneplan_path (Path): _description_
        history_path (Path): _description_
        auto_restart (int): Restart upload if it takes longer than the definite amount of minutes
    """

    message_id = None
    while message_id != 0:
        message_id = await get_next_to_upload(cloneplan_path)
        if message_id == 0:
            return

        await upload_media(
            client_name,
            session_folder,
            chat_id,
            message_id,
            cloneplan_path,
            history_path,
            auto_restart,
        )
        # mark flag clone in cloneplan_path file
        set_clone(cloneplan_path, message_id)

        # delete local media to release space in the cache folder
        delete_local_media(cloneplan_path, message_id)

    print("\n-- Everything was uploaded :)")
