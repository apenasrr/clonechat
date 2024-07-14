from __future__ import annotations

import asyncio
import collections
import os
import time
from pathlib import Path
from typing import Union

import pyrogram

from ..utils.csv_util import open_csv, save_csv
from ..utils.progress_bar import progress_bar


def get_next_to_download(cloneplan_path: Path) -> int:
    """returns the smallest message_id not yet done download

    Args:
        cloneplan_path (Path): _description_

    Returns:
        int: message_id. 0 If there was no more messages to download
    """

    list_data = open_csv(cloneplan_path)
    dict_data = collections.OrderedDict(
        sorted({int(item["id"]): item for item in list_data}.items())
    )

    for message_id in dict_data.keys():
        if (
            dict_data[message_id].get("download", "") == "0"
            and dict_data[message_id].get("clone", "") == "0"
        ):
            return message_id
    return 0


async def download_media_core(
    client: pyrogram.client, message: pyrogram.types.Message, file_path: Path
):
    print(f"dw: {file_path.name}")
    c_time = time.time()
    prefix = "DW"
    await client.download_media(
        message,
        file_name=file_path,
        progress=progress_bar,
        progress_args=(c_time, prefix),
    )
    print("")


def get_size(start_path: Path = Path(".")) -> int:
    """find python get total size of a Folder.
    Source: https://stackoverflow.com/a/1392549 .

    Args:
        start_path (str, optional): _description_. Defaults to '.'.

    Returns:
        total_size (int): bytes
    """

    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


def check_auth_download(
    file_size_bytes: int,
    download_folder: Path,
    max_size_mb: int,
    verbose: bool = False,
) -> bool:
    """Authorizes continuation of the download.
    Check if when downloading the file, it will exceed
    the maximum storage capacity of the folder.

    Args:
        file_size_bytes (int): _description_
        download_folder (Path): _description_
        max_size_mb (int): _description_

    Returns:
        bool: _description_
    """

    actual_size_mb = get_size(download_folder) / 1024**2
    file_size_mb = file_size_bytes / (1024**2)
    if verbose:
        print(f"{file_size_mb=}")
        print(f"{actual_size_mb=}")
        print(f"{max_size_mb=}")
    if (file_size_mb + actual_size_mb) > max_size_mb:
        return False
    else:
        return True


async def download_media(
    client: pyrogram.Client,
    chat_id: int,
    message_id: int,
    cloneplan_path: Path,
    download_folder: Path,
    max_size_mb: int,
):
    """Efetua download de qualquer media. Video, document, photo, audio, voice

    Args:
        client (pyrogram.Client): _description_
        chat_id (int): _description_
        message_id (int): _description_
        cloneplan_path (Path): _description_
        download_folder (Path): _description_
        max_size_mb (int):
    """

    # message_object
    message = await client.get_messages(chat_id, message_id)
    # file_path
    #  get from cloneplan report because file_name is in different locations
    #  depending the message type (video, document, photo, audio, voice)

    list_data = open_csv(cloneplan_path)
    row_data = [data for data in list_data if int(data["id"]) == message_id][0]
    file_name = row_data["file_name"]
    file_size_bytes = int(row_data["file_size"])

    file_path = download_folder / (str(message_id) + "-" + str(file_name))

    if file_path.exists():
        file_path.unlink()

    # Awaits by download authorization
    while True:
        auth_download = check_auth_download(
            file_size_bytes, download_folder, max_size_mb
        )
        if auth_download:
            break
        else:
            await asyncio.sleep(5)

    await download_media_core(client, message, file_path)

    # register flag download and file_path
    set_downloaded(cloneplan_path, message_id, file_path)


def set_downloaded(
    cloneplan_path: Path, message_id: int, file_path: Union[Path, None] = None
):
    """Mark in the clone plan report that the file was downloaded

    Args:
        cloneplan_path (Path): clone plan report path
        message_id (int): chat message id
        file_path (Path, optional): file downloaded local path. Defaults to None.
    """

    list_data = open_csv(cloneplan_path)
    for data in list_data:
        if data["id"] == str(message_id):
            data["file_path"] = file_path
            data["download"] = 1
            break
    save_csv(list_data, cloneplan_path)


async def pipe_download(
    client: pyrogram.client,
    chat_id: int,
    cloneplan_path: Path,
    download_folder: Path,
    max_size_mb: int,
):
    """Download all message_id in ascending order.
    Mark in the cloneplan_path file the flag download and file_path
    whenever finish the download of a file.
    For Message_id not downloadable, automatically marks the Flag Download and
    File_Path in empty string.

    Args:
        client (pyrogram.client): _description_
        chat_id (int): _description_
        cloneplan_path (Path): _description_
        download_folder (Path): _description_
        max_size_mb (int):
    """

    message_id = None
    while message_id != 0:
        message_id = get_next_to_download(cloneplan_path)
        if message_id == 0:
            print("-- Everything was done download :)")
            return
        # Identifies the type of post
        list_data = open_csv(cloneplan_path)
        dict_data = collections.OrderedDict(
            sorted({int(item["id"]): item for item in list_data}.items())
        )
        list_type = ["document", "video", "photo", "audio", "voice"]
        message_type = dict_data[message_id]["type"]
        # If it is a downloadable post
        if message_type in list_type:
            # Download, mark flag 'download' and register 'file_path'
            # in the cloneplan_path file
            await download_media(
                client,
                chat_id,
                message_id,
                cloneplan_path,
                download_folder,
                max_size_mb,
            )
        else:
            # mark flag 'download' in cloneplan_path file
            file_path = ""
            set_downloaded(cloneplan_path, message_id, file_path)
