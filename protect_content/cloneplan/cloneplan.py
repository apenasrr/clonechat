from __future__ import annotations

import json
from pathlib import Path

from ..utils.csv_util import save_csv


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
    list_type = [msg_type.strip() for msg_type in str_list_types.split("\n")]
    return list_type


def ignore_types():

    list_ignore_types = [
        "empty",
        "service",
        "dice",
        "location",
        "contact",
        "poll",
    ]
    return list_ignore_types


def enrich_fields(cloneplan_dict, msg, key):

    def generate_file_name(msg):
        mime_type_to_extension = {
            "video/mp4": ".mp4",
            "video/quicktime": ".mov",
        }
        extension = mime_type_to_extension.get(
            msg["video"]["mime_type"], ".mkv"
        )
        return f'{msg["id"]}-{msg["video"]["file_unique_id"]}{extension}'

    if key == "video":
        cloneplan_dict["duration"] = msg["video"]["duration"]
        cloneplan_dict["file_size"] = msg["video"]["file_size"]
        cloneplan_dict["file_name"] = msg["video"].get(
            "file_name",
            generate_file_name(msg),
        )
        return cloneplan_dict
    if key == "document":
        cloneplan_dict["file_size"] = msg["document"]["file_size"]
        cloneplan_dict["file_name"] = msg["document"]["file_name"]
        return cloneplan_dict
    if key == "photo":
        cloneplan_dict["file_size"] = msg["photo"]["file_size"]
        cloneplan_dict["file_name"] = msg["photo"]["file_unique_id"] + ".jpg"
    if key == "audio":
        cloneplan_dict["duration"] = msg["audio"]["duration"]
        cloneplan_dict["file_size"] = msg["audio"]["file_size"]
        cloneplan_dict["file_name"] = msg["audio"]["file_name"]
        return cloneplan_dict
    if key == "voice":
        cloneplan_dict["duration"] = msg["voice"]["duration"]
        cloneplan_dict["file_size"] = msg["voice"]["file_size"]
        cloneplan_dict["file_name"] = msg["voice"]["file_unique_id"] + ".ogg"
        return cloneplan_dict
    if key == "text":
        cloneplan_dict["caption_sample"] = msg["text"][:20]
        return cloneplan_dict
    return cloneplan_dict


def create_cloneplan(
    history_path: Path, topic_id: int | None = None
) -> list[dict]:

    def need_skip(msg: dict, topic_id: int | None) -> bool:
        """
        Determines if the message should be jumped based on topic rule.
        If it is a group enabled to the topic, check if the message is from the
        topic needed. If it is, you return false, otherwise you return True.
        Args:
            msg (dict): The message dictionary.
            topic_id (int | None): The topic ID.
        Returns:
            bool: True if the message needs to be skipped, False otherwise.
        """

        if topic_id is None:
            return False
        msg_topic_id = msg.get("topics", {}).get("id", 0)
        return msg_topic_id != topic_id

    list_dict = json.load(open(history_path, encoding="utf-8"))
    list_type = msgs_types()
    list_ignore_types = ignore_types()
    ignore = False
    found = False
    cloneplan_list_dict = []
    for msg in list_dict:
        if need_skip(msg, topic_id):
            continue
        cloneplan_dict = {}
        cloneplan_dict["id"] = msg["id"]
        cloneplan_dict["date"] = msg["date"]
        for key in msg.keys():
            if key in list_ignore_types:
                ignore = True
                break
            if key in list_type:
                cloneplan_dict["type"] = key
                cloneplan_dict["caption_sample"] = msg.get("caption", "")[:20]
                cloneplan_dict = enrich_fields(cloneplan_dict, msg, key)
                found = True
                break
        if not found:
            cloneplan_dict["type"] = "#not_identified"
        if ignore:
            ignore = False
            continue
        cloneplan_list_dict.append(cloneplan_dict)
        found = False
    return cloneplan_list_dict


def save_cloneplan(
    history_path, cloneplan_path, topic_id: int | None = None
) -> Path:

    cloneplan_list_dict = create_cloneplan(history_path, topic_id)
    save_csv(cloneplan_list_dict, cloneplan_path)
    return cloneplan_path
