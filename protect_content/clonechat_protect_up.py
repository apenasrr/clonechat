from __future__ import annotations

import json
import sys
from configparser import ConfigParser
from datetime import date
from pathlib import Path
from time import sleep
from typing import Union

import pyrogram
from pyrogram.errors import ChannelInvalid, PeerIdInvalid

from setup import version

from .pipe import upload
from .utils import parser


def get_config_data(path_file_config: Path):
    """get default configuration data from file config.ini

    Returns:
        dict: config data
    """

    config_file = ConfigParser()
    config_file.read(path_file_config)
    default_config = dict(config_file["default"])
    return default_config


def get_client(
    client_name: str, session_folder: Path = Path(".")
) -> pyrogram.Client:
    """Perform the connection to Telegram and returns the client
    not requesting ID or Password if not necessary.

    Args:
        client_name (str): session file name
        session_folder (Path, optional): Folder where the session file should
            be. Defaults to Path(".").

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
            useraccount.start()
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
            useraccount.start()
            return useraccount
        except Exception as e:
            print(e, "\nError. Try again.\n")
            return None


def get_chat_info(
    client: pyrogram.Client, chat_input: Union[int, str]
) -> Union[dict, bool]:
    """Returns the chat_info (chat_id, chat_title) if chat_input is valid.
        Returns false if it is invalid.
    Valid chat_input: messsage_link, chat_id, invite link, chat_link,
        chat_username

    Args:
        client (pyrogram.Client): started pyrogram client
        chat_input (Union[int, str]): chat_id or invite link

    Returns:
        Union[dict, bool]:
            {chat_id, chat_title}
            or False if chat_input invalid
    """

    base_link = "https://t.me/c/"
    if base_link in str(chat_input):
        # if chat_input is a message link, convert to chat_id
        base_chat_id = str(chat_input.split(base_link)[1].split("/")[0])
        chat_input = "-100" + base_chat_id

    try:
        chat_obj = client.get_chat(chat_input)
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


def get_chat_info_until(client: pyrogram.Client, message: str) -> dict:
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
        origin_chat_info = get_chat_info(client, chat_input)
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


def save_history(client: pyrogram.Client, chat_id: int, history_path: Path):

    # save history json
    list_dict_msgs = []
    iter_message = client.get_chat_history(chat_id)
    for message in iter_message:
        dict_message = json.loads(str(message))
        list_dict_msgs.append(dict_message)
        if len(list_dict_msgs) % 200 == 0:
            sleep(2)
        json.dump(
            list_dict_msgs, open(history_path, "w", encoding="utf-8"), indent=2
        )

    print(f"The chat history was saved. {len(list_dict_msgs)} messages.")


def get_recent_history(chat_title: str, chat_id: int) -> Path:

    log_chats_path = Path("protect_content") / "log_chats"
    log_chats_path.mkdir(exist_ok=True)
    chat_history_name = f"{str(abs(chat_id))}-{str(chat_title)}"
    chat_history_path = log_chats_path / chat_history_name
    if not chat_history_path.is_dir():
        print(
            chat_history_name, "\nChat history not found. Waiting history..."
        )
        while not chat_history_path.is_dir():
            sleep(5)
            chat_history_path.is_dir()

    recent_history = list(chat_history_path.iterdir())[-1]
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
        for _, msg in enumerate(list_msgs):
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

    first_try = True
    while True:
        try:
            with open(history_path, encoding="utf-8") as file:
                list_msgs = json.load(file)
            break
        except (FileNotFoundError, json.JSONDecodeError) as e:
            if first_try:
                print(
                    f"{e}\n\nHold on... Awaiting the history file be saved..."
                )
                first_try = False
            sleep(5)
    list_type = msgs_types()
    data_metrics = get_chat_data_metrics(list_msgs)
    print(f"\nChat History: {history_path.parent.name}")
    print(
        f"duration: {data_metrics['hours']}h {data_metrics['minutes']}m "
        + f"{data_metrics['seconds']:.1f}s"
    )
    print(f"total size: {(data_metrics['total_size'] / 1024**3):.3f} GB")
    counter_type = get_msg_type_count(list_type, list_msgs)

    print(f"msgs count by type: {json.dumps(counter_type, indent=2)}\n")


def main():

    print(
        f"\n....:: Clonechat - v{version} ::....\n"
        + "github.com/apenasrr/clonechat/\n"
        + "-----------Protect UP---------"
    )
    config_path = Path(".").absolute() / "user" / "config.ini"
    config_data = get_config_data(path_file_config=config_path)

    session_folder = Path(".").absolute()

    up_client_name = "user_up"
    # test_connection for upload client
    client_up = get_client(up_client_name, session_folder=session_folder)

    message = (
        "Enter the ORIGIN message_link, chat_id, chat_link or chat_username: "
    )
    chat_origin_info = get_chat_info_until(client_up, message)
    chat_origin_title = parser.sanitize_string(chat_origin_info["chat_title"])
    chat_origin_id = chat_origin_info["chat_id"]
    print(f"ORIGIN: {abs(chat_origin_id)}-{chat_origin_title}\n")

    message = (
        "Enter the DESTINATION "
        + "message_link, chat_id or chat_link or chat_username: "
    )
    chat_dest_info = get_chat_info_until(client_up, message)
    chat_dest_title = parser.sanitize_string(chat_dest_info["chat_title"])
    chat_dest_id = chat_dest_info["chat_id"]
    print(f"DESTINATION: {abs(chat_dest_id)}-{chat_dest_title}\n")

    # cloneplan_path
    folder_path_cloneplan = Path("protect_content") / "log_cloneplan"
    folder_path_cloneplan.mkdir(exist_ok=True)
    cloneplan_path = get_cloneplan_path(
        folder_path_cloneplan, chat_origin_id, chat_origin_title
    )

    history_path = get_recent_history(chat_origin_title, chat_origin_id)

    show_history_overview(history_path)

    # download_folder
    cache_folder = Path("protect_content") / "Cache"
    cache_folder.mkdir(exist_ok=True)
    download_folder = (
        cache_folder / f"{str(abs(chat_origin_id))}-{chat_origin_title}"
    )
    download_folder.mkdir(exist_ok=True)

    auto_restart = int(config_data.get("auto_restart_min", 20))

    upload.pipe_upload(
        up_client_name,
        session_folder,
        chat_dest_id,
        cloneplan_path,
        history_path,
        auto_restart,
    )


if __name__ == "__main__":
    main()
