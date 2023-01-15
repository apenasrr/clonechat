from __future__ import annotations

import asyncio
import json
import sys
from configparser import ConfigParser
from datetime import date
from pathlib import Path
from typing import Union

import pyrogram
from pyrogram.errors import ChannelInvalid, PeerIdInvalid

from . import cloneplan
from .pipe import download, upload


def get_config_data(path_file_config: Path):
    """get default configuration data from file config.ini

    Returns:
        dict: config data
    """

    config_file = ConfigParser()
    config_file.read(path_file_config)
    default_config = dict(config_file["default"])
    return default_config


async def get_client(
    client_name: str, session_folder: Path = Path(".")
) -> pyrogram.Client:
    """Perform the connection to Telegram and returns the client
    not requesting ID or Password if not necessary.

    Args:
        client_name (str): session file name
        session_folder (Path, optional): Folder where the session file should be. Defaults to Path(".").

    Returns:
        pyrogram.Client: pyrogram client
    """

    session_path = session_folder / f"{client_name}.session"
    print(session_path)
    if session_path.exists():
        try:
            useraccount = pyrogram.Client(
                client_name, workdir=str(session_folder)
            )
            await useraccount.start()
            return useraccount
        except Exception as e:
            Path(f"{useraccount}.session").unlink()
            print(
                e,
                (
                    "\nSession invalid. "
                    + "Please, try again to make a new connection."
                ),
            )

    while True:
        try:
            api_id = int(input("Enter your api_id: "))
            api_hash = input("Enter your api_hash: ")

            useraccount = pyrogram.Client(
                client_name, api_id, api_hash, workdir=str(session_folder)
            )
            await useraccount.start()
            return useraccount
        except Exception as e:
            print(e, "\nError. Try again.\n")
            return None


async def get_chat_info(
    client: pyrogram.Client, chat_input: Union[int, str]
) -> Union[dict, bool]:
    """Returns the chat_info (chat_id, chat_title) if chat_input is valid.
     Returns false if it is invalid.

    Args:
        client (pyrogram.Client): started pyrogram client
        chat_input (Union[int, str]): chat_id or invite link

    Returns:
        Union[dict, bool]:
            {chat_id, chat_title}
            or False if chat_input invalid
    """

    try:
        chat_obj = await client.get_chat(chat_input)
        chat_id = chat_obj.id
        chat_title = chat_obj.title
        chat_info = {"chat_id": chat_id, "chat_title": chat_title}
        return chat_info
    except ChannelInvalid:  # When you are not part of the channel
        print("\nNon-accessible chat")
        return False
    except PeerIdInvalid as e:  # When the chat_id is invalid
        print(f"\n{e}\nInvalid chat_input: {chat_input}")
        return False
    except Exception as e:
        print(e, f"\nInvalid chat_input: {chat_input}")


async def get_chat_info_until(client: pyrogram.Client, message: str) -> dict:
    """Continuously requests a chat identifier to return chat information:
    (chat_id, chat_title)

    Args:
        client (pyrogram.Client): pyrogram client
        message (str): request message for the user

    Returns:
        dict: keys: chat_id, chat_title
    """
    while True:
        return_question = input(message)
        chat_input = (
            int(return_question)
            if return_question.replace("-", "").isnumeric()
            else return_question
        )
        origin_chat_info = await get_chat_info(client, chat_input)
        if isinstance(origin_chat_info, dict):
            break
        else:
            return_ = input(
                "Press 'Enter' to try again or press something to close:\n"
            )
            if return_ == "":
                pass
            else:
                sys.exit()

    return origin_chat_info


def get_cloneplan_path(
    folder_path_cloneplan: Path, chat_dest_id: int, chat_dest_title: str
) -> Path:

    folder_path_cloneplan.mkdir(exist_ok=True)
    clonechat_path = (
        folder_path_cloneplan
        / f"cloneplan_{str(abs(chat_dest_id))}-{chat_dest_title}.csv"
    )
    return clonechat_path


def get_history_path(chat_title: str, chat_id: int) -> Path:

    log_chats_path = Path("protect_content") / "log_chats"
    log_chats_path.mkdir(exist_ok=True)
    folder_chat = log_chats_path / f"{str(abs(chat_id))}-{str(chat_title)}"
    folder_chat.mkdir(exist_ok=True)
    str_today = date.today().strftime("%Y%m%d")
    history_path = folder_chat / f"msgs_chat_{abs(chat_id)}_{str_today}.json"
    return history_path


async def save_history(
    client: pyrogram.Client, chat_id: int, history_path: Path
):

    # save history json
    list_dict_msgs = []
    iter_message = client.get_chat_history(chat_id)
    async for message in iter_message:
        dict_message = json.loads(str(message))
        list_dict_msgs.append(dict_message)
        if len(list_dict_msgs) % 200 == 0:
            await asyncio.sleep(2)
        json.dump(
            list_dict_msgs, open(history_path, "w", encoding="utf-8"), indent=2
        )

    print(f"The chat history was saved. {len(list_dict_msgs)} posts.")


async def pipe_clone(
    client: pyrogram.Client,
    up_client_name: str,
    up_session_folder: Path,
    chat_id_orig: int,
    chat_id_dest: int,
    cloneplan_path: Path,
    history_path: Path,
    download_folder: Path,
    max_size_mb: int,
    auto_restart: int,
):

    loop = asyncio.get_event_loop()
    list_tasks = list()
    list_tasks.append(
        loop.create_task(
            download.pipe_download(
                client,
                chat_id_orig,
                cloneplan_path,
                download_folder,
                max_size_mb,
            )
        )
    )
    list_tasks.append(
        loop.create_task(
            upload.pipe_upload(
                up_client_name,
                up_session_folder,
                chat_id_dest,
                cloneplan_path,
                history_path,
                auto_restart,
            )
        )
    )

    await asyncio.gather(*list_tasks)
    print("\nChat Cloned. Done!")


def get_recent_history(chat_title: str, chat_id: int) -> Path:

    log_chats_path = Path("protect_content") / "log_chats"
    log_chats_path.mkdir(exist_ok=True)
    folder_chat = log_chats_path / f"{str(abs(chat_id))}-{str(chat_title)}"
    recent_history = list(folder_chat.iterdir())[-1]
    return recent_history


def ask_for_new_clone() -> bool:
    print(
        "Continue cloning or start a new one?",
        "1 - Continue",
        "2 - Start a new",
        sep="\n",
    )
    answer = input("Answer: ")

    new_clone = False if answer == "1" else True
    return new_clone


def show_history_overview(history_path: Path) -> list[str]:
    def msgs_types():
        str_list_types = """photo
        text
        document
        sticker
        animation
        audio
        voice
        video
        video_note
        poll
        service
        dice
        location
        empty
        contact"""
        list_type = [
            msg_type.strip() for msg_type in str_list_types.split("\n")
        ]
        return list_type

    def get_chat_data_metrics(list_msgs):
        total_video_duration = 0
        total_size = 0
        for index, msg in enumerate(list_msgs):
            # if index == 100:
            #     break
            if isinstance(msg, str):
                msg = json.loads(msg)
            if isinstance(msg, str):
                continue
            if "video" in msg.keys():
                total_video_duration += msg["video"]["duration"]
                total_size += msg["video"]["file_size"]
            if "document" in msg.keys():
                total_size += msg["document"]["file_size"]
        hours = total_video_duration // 3600
        minutes = total_video_duration % 3600 // 60
        seconds = total_video_duration % 60

        return {
            "total_video_duration": total_video_duration,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "total_size": total_size,
        }

    def get_msg_type_count(list_type, list_msgs):

        counter_type = {}
        for msg in list_msgs:
            if isinstance(msg, str):
                msg = json.loads(msg)
            if isinstance(msg, str):
                continue
            for key in msg.keys():
                if key in list_type:
                    value = counter_type.get(key, 0)
                    found = True
                    if value == 0:
                        counter_type[key] = 1
                    else:
                        counter_type[key] += 1
                    break
            if not found:
                print(msg["id"], " ".join(msg.keys()))
                found = False
        return counter_type

    list_msgs = json.load(open(history_path, encoding="utf-8"))
    list_type = msgs_types()
    data_metrics = get_chat_data_metrics(list_msgs)
    print(f"\nChat History: {history_path.parent.name}")
    print(
        f"duration: {data_metrics['hours']}h {data_metrics['minutes']}m {data_metrics['seconds']}s"
    )
    print(f"total size: {(data_metrics['total_size'] / 1024**3):.3f} GB")
    counter_type = get_msg_type_count(list_type, list_msgs)

    print(f"msgs count by type: {json.dumps(counter_type, indent=2)}\n")


async def main():

    config_path = Path(".").absolute() / "user" / "config.ini"
    config_data = get_config_data(path_file_config=config_path)

    session_folder = Path(".").absolute()
    client = await get_client("user", session_folder=session_folder)

    up_client_name = "user_up"
    # test_connection for upload client
    client_up = await get_client(up_client_name, session_folder=session_folder)
    await client_up.stop()

    message = "Enter the ORIGIN chat_id, chat_link or chat_username: "
    chat_origin_info = await get_chat_info_until(client, message)
    chat_origin_title = chat_origin_info["chat_title"]
    chat_origin_id = chat_origin_info["chat_id"]
    print(f"ORIGIN: {abs(chat_origin_id)}-{chat_origin_title}\n")

    message = "Enter the DESTINATION chat_id or chat_link or chat_username: "
    chat_dest_info = await get_chat_info_until(client, message)
    chat_dest_title = chat_dest_info["chat_title"]
    chat_dest_id = chat_dest_info["chat_id"]
    print(f"DESTINATION: {abs(chat_dest_id)}-{chat_dest_title}\n")

    # cloneplan_path
    folder_path_cloneplan = Path("protect_content") / "log_cloneplan"
    folder_path_cloneplan.mkdir(exist_ok=True)
    cloneplan_path = get_cloneplan_path(
        folder_path_cloneplan, chat_origin_id, chat_origin_title
    )

    new_clone = True
    if cloneplan_path.exists():
        new_clone = ask_for_new_clone()

    if new_clone:
        history_path = get_history_path(chat_origin_title, chat_origin_id)
        await save_history(client, chat_origin_id, history_path)

        cloneplan.save_cloneplan(history_path, cloneplan_path)
    else:
        history_path = get_recent_history(chat_origin_title, chat_origin_id)

    show_history_overview(history_path)

    # download_folder
    cache_folder = Path("protect_content") / "Cache"
    cache_folder.mkdir(exist_ok=True)
    download_folder = (
        cache_folder / f"{str(abs(chat_origin_id))}-{chat_origin_title}"
    )
    download_folder.mkdir(exist_ok=True)

    cache_folder_max_size_mb = int(
        config_data.get("cache_folder_max_size_mb", 6000)
    )
    auto_restart = int(config_data.get("auto_restart_min", 20))

    await pipe_clone(
        client,
        up_client_name,
        session_folder,
        chat_origin_id,
        chat_dest_id,
        cloneplan_path,
        history_path,
        download_folder,
        cache_folder_max_size_mb,
        auto_restart,
    )


if __name__ == "__main__":
    asyncio.run(main())
