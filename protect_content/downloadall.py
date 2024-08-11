from __future__ import annotations

from pathlib import Path

from setup import version

from . import clonechat_protect_down, cloneplan
from .pipe import download
from .utils import parser


def main():

    print(
        f"\n....:: Clonechat - v{version} ::....\n"
        + "github.com/apenasrr/clonechat/\n"
        + "---------DownloadAll----------"
    )

    session_folder = Path(".").absolute()
    client = clonechat_protect_down.get_client(
        "user", session_folder=session_folder
    )

    message = "Enter the ORIGIN chat_id, chat_link or chat_username: "
    chat_origin_info = clonechat_protect_down.get_chat_info_until(
        client, message
    )
    chat_origin_title = parser.sanitize_string(chat_origin_info["chat_title"])
    chat_origin_title = (
        chat_origin_title[:100].strip()
        if len(chat_origin_title) > 100
        else chat_origin_title
    )
    chat_origin_id = chat_origin_info["chat_id"]
    chat_origin_topic_id: int | None = chat_origin_info.get("topic_id", None)
    chat_origin_topic_name = chat_origin_info.get("topic_name", None)
    if chat_origin_topic_name:
        print(
            f"ORIGIN: {abs(chat_origin_id)}-{chat_origin_title}-"
            + f"{chat_origin_topic_name}\n"
        )
    else:
        print(f"ORIGIN: {abs(chat_origin_id)}-{chat_origin_title}\n")

    # cloneplan_path
    folder_path_cloneplan = Path("protect_content") / "log_cloneplan"
    folder_path_cloneplan.mkdir(exist_ok=True)
    cloneplan_path = clonechat_protect_down.get_cloneplan_path(
        folder_path_cloneplan,
        chat_origin_id,
        chat_origin_title,
        chat_origin_topic_id,
        chat_origin_topic_name,
    )
    history_path = clonechat_protect_down.get_history_path(
        chat_origin_title, chat_origin_id
    )
    new_clone = True

    if not history_path.exists():
        clonechat_protect_down.save_history(
            client, chat_origin_id, history_path
        )

    if cloneplan_path.exists():
        new_clone = clonechat_protect_down.ask_for_new_clone()

    if new_clone:
        cloneplan.save_cloneplan(
            history_path, cloneplan_path, chat_origin_topic_id
        )
    else:
        history_path = clonechat_protect_down.get_recent_history(
            chat_origin_title, chat_origin_id
        )
    clonechat_protect_down.show_history_overview(
        history_path, chat_origin_topic_id
    )

    # download_folder
    cache_folder = Path("protect_content") / "Cache"
    cache_folder.mkdir(exist_ok=True)
    if chat_origin_topic_name:
        download_folder = cache_folder / (
            f"{str(abs(chat_origin_id))}-{chat_origin_title}-"
            + f"{chat_origin_topic_name}"
        )
    else:
        download_folder = (
            cache_folder / f"{str(abs(chat_origin_id))}-{chat_origin_title}"
        )
    download_folder.mkdir(exist_ok=True)

    download.pipe_download(
        client,
        chat_origin_id,
        cloneplan_path,
        download_folder,
        max_size_mb=9_999_999,
    )


if __name__ == "__main__":
    main()
