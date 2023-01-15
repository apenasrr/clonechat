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

    if key == "video":
        cloneplan_dict["duration"] = msg["video"]["duration"]
        cloneplan_dict["file_size"] = msg["video"]["file_size"]
        cloneplan_dict["file_name"] = msg["video"]["file_name"]
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


def create_cloneplan(history_path: Path):

    list_dict = json.load(open(history_path, encoding="utf-8"))
    list_type = msgs_types()
    list_ignore_types = ignore_types()
    ignore = False
    found = False
    cloneplan_list_dict = []
    for msg in list_dict:
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


def save_cloneplan(history_path, cloneplan_path):

    cloneplan_list_dict = create_cloneplan(history_path)
    save_csv(cloneplan_list_dict, cloneplan_path)
    return cloneplan_path
