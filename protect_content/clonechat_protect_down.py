from __future__ import annotations

import json
import shutil
import sys
from configparser import ConfigParser
from datetime import date
from pathlib import Path
from time import sleep
from typing import Union

import pyrogram
from pyrogram.errors import ChannelInvalid, PeerIdInvalid

from setup import version

from . import cloneplan
from .pipe import download
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


def get_topic_data_from_link(
    client: pyrogram.Client, chat_id: str, chat_input: list
) -> dict[str, any | None]:

    topic_id = None
    topic_name = None

    base_link = "https://t.me/c/"
    splits = chat_input.split(base_link)[1].split("/")
    if len(splits) == 3:
        topic_id = int(splits[1])
        message_id = int(splits[-1])
        topic_name = None
        # Context: client.get_forum_topics does not return all chat topics.
        # Therefore, it is necessary to get the message to get the topic_id and
        # topic_name
        first_try = True
        while True:
            try:
                message = client.get_messages(chat_id, message_id)
                message = json.loads(str(message))
                break
            except Exception as e:
                if first_try:
                    print(f"\n{e}\nAn error occurred. Trying again.")
                sleep(5)
                continue
        topic_id = message.get("topic", {}).get("id", None)
        topic_name = message.get("topic", {}).get("title", None)
        topic_name = parser.sanitize_string(topic_name)
        # se topic_id ou topic_name for None, emitir erro
        if topic_id is None or topic_name is None:
            print(
                f"\nThis chat is a forum: {chat_id}\n"
                + "Please, repeat posting a message link from a topic."
            )
            client.stop()
            exit(0)
    else:
        pass
    return {"topic_id": topic_id, "topic_name": topic_name}


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
    topic_id = None
    topic_name = None
    if base_link in str(chat_input):
        # if chat_input is a message link, convert to chat_id
        splits = chat_input.split(base_link)[1].split("/")
        chat_id = "-100" + str(splits[0])
        topic_data = get_topic_data_from_link(client, chat_id, chat_input)
        topic_id = topic_data.get("topic_id", None)
        topic_name = topic_data.get("topic_name", None)
        chat_input = chat_id

    try:
        chat_obj = client.get_chat(chat_input)
        chat_id = chat_obj.id
        chat_title = chat_obj.title
        chat_isforum = chat_obj.is_forum
        if chat_isforum:
            if topic_id is None:
                print(
                    f"\nThis chat is a forum: {chat_title}\n"
                    + "Please, repeat posting a message link from a topic."
                )
                # TODO: If it is a forum, look for topics list and ask which
                # one wants
                client.stop()
                exit(0)
            else:
                pass
        chat_info = {
            "chat_id": chat_id,
            "chat_title": chat_title,
            "topic_id": topic_id,
            "topic_name": topic_name,
        }
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
                "\nPress 'Enter' to try again or press something to close:\n"
            )
            if return_ == "":
                pass
            else:
                sys.exit()

    return origin_chat_info


def get_cloneplan_path(
    folder_path_cloneplan: Path,
    chat_id: int,
    chat_title: str,
    topic_id: int | None = None,
    topic_name: str | None = None,
) -> Path:

    folder_path_cloneplan.mkdir(exist_ok=True)

    if topic_id is None:
        clonechat_path = (
            folder_path_cloneplan
            / f"cloneplan_{str(abs(chat_id))}-{chat_title}.csv"
        )
    else:
        # If it is topic, add topic_id and topic_name to the file name
        clonechat_path = folder_path_cloneplan / (
            f"cloneplan_{str(abs(chat_id))}-{chat_title}-"
            + f"{str(topic_id)}-{topic_name}.csv"
        )
    return clonechat_path


def get_history_path(chat_title: str, chat_id: int) -> Path:
    """
    Determine the file path for saving the chat history.

    Constructs a directory path based on the chat title and ID, ensuring the
    directory exists.
    If the directory already contains history files, it prompts the USER to
    decide whether to use the most recent history file.
    If the USER chooses to use the latest history, the function returns the
    path to that file.
    Otherwise, it creates a new directory if it doesn't exist and generates a
    new file path based on the current date for saving the chat history.

    Args:
        chat_title (str): The title of the chat.
        chat_id (int): The ID of the chat.

    Returns:
        Path: The path to the history file.
    """

    log_chats_path = Path("protect_content") / "log_chats"
    log_chats_path.mkdir(exist_ok=True)
    folder_chat = log_chats_path / f"{str(abs(chat_id))}-{str(chat_title)}"
    # If history folder exists, ask if you want to use the latest history
    if folder_chat.exists():
        list_history_path = list(folder_chat.iterdir())
        if len(list_history_path) > 0:
            recent_history = list_history_path[-1]
            print(
                f"Use the last history: {recent_history.name} ?",
                "1 - Yes",
                "2 - No",
                sep="\n",
            )
            answer = input("Answer: ")
            if answer in ["1", ""]:
                return recent_history

    folder_chat.mkdir(exist_ok=True)
    str_today = date.today().strftime("%Y%m%d")
    history_path = folder_chat / f"msgs_chat_{abs(chat_id)}_{str_today}.json"
    return history_path


def save_history(client: pyrogram.Client, chat_id: int, history_path: Path):
    """
    Save the message history of a chat to a JSON file.

    Collects and saves the message history of a chat in a structured manner.
    The messages are collected in blocks of 200 and saved in intermediate JSON
    files within a temporary folder. After collecting all messages, the
    intermediate JSON files are concatenated into a single JSON file, which is
    saved at the specified history path.
    The temporary folder is then removed.

    Average speed of 11 seconds for 1.000 messages.

    Args:
        client (pyrogram.Client): The Pyrogram client instance.
        chat_id (int): The ID of the chat.
        history_path (Path): The path to save the message history JSON file.
    Returns:
        None
    """

    print(f"\nHold on... Mapping message history in: {str(history_path)}")

    date_today = (history_path.stem).split("_")[-1]
    # save history. In several JSON files. Each json with 200 messages in
    # temporary folder
    history_path_folder_temp = history_path.parent / date_today
    history_path_folder_temp.mkdir(exist_ok=True)
    list_dict_msgs = []
    index = 1
    iter_message = client.get_chat_history(chat_id)
    for message in iter_message:
        dict_message = json.loads(str(message))
        list_dict_msgs.append(dict_message)
        if len(list_dict_msgs) % 200 == 0:
            sleep(2)
            history_path_temp = history_path_folder_temp / (
                str(index) + "_" + history_path.name
            )
            json.dump(
                list_dict_msgs,
                open(history_path_temp, "w", encoding="utf-8"),
                indent=2,
            )
            list_dict_msgs = []
        index += 1
    # If there are remaining messages, save last JSON
    if len(list_dict_msgs) > 0:
        history_path_temp = history_path_folder_temp / (
            str(index) + "_" + history_path.name
        )
        json.dump(
            list_dict_msgs,
            open(history_path_temp, "w", encoding="utf-8"),
            indent=2,
        )
        list_dict_msgs = []

    # concat all JSON from the History_Path_Folder_temp
    list_dict_msgs = []
    for file in history_path_folder_temp.iterdir():
        list_dict_msgs += json.load(open(file, encoding="utf-8"))
    json.dump(
        list_dict_msgs,
        open(history_path, "w", encoding="utf-8"),
        indent=2,
    )
    # remove temporary folder
    shutil.rmtree(history_path_folder_temp)
    print(f"The chat history was saved. {len(list_dict_msgs)} messages.")


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


def show_history_overview(
    history_path: Path, topic_id: int | None = None
) -> list[str]:
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
            if topic_id is not None:
                if msg.get("topics", {}).get("id", None) != topic_id:
                    continue
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
            if topic_id is not None:
                if msg.get("topics", {}).get("id", None) != topic_id:
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
                print(
                    msg["id"],
                    "unidentified message type",
                    " ".join(msg.keys()),
                )
                found = False
        return counter_type

    list_msgs = json.load(open(history_path, encoding="utf-8"))
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
        + "-----------Protect Dw---------"
    )
    config_path = Path(".").absolute() / "user" / "config.ini"
    config_data = get_config_data(path_file_config=config_path)

    session_folder = Path(".").absolute()
    client = get_client("user", session_folder=session_folder)

    message = (
        "Enter the ORIGIN messsage_link, chat_id, chat_link or chat_username: "
    )
    chat_origin_info = get_chat_info_until(client, message)
    chat_origin_title = parser.sanitize_string(chat_origin_info["chat_title"])
    chat_origin_id = chat_origin_info["chat_id"]
    print(f"ORIGIN: {abs(chat_origin_id)}-{chat_origin_title}\n")

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
        save_history(client, chat_origin_id, history_path)

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

    download.pipe_download(
        client,
        chat_origin_id,
        cloneplan_path,
        download_folder,
        cache_folder_max_size_mb,
    )


if __name__ == "__main__":
    main()
