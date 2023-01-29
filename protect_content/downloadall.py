from __future__ import annotations

import asyncio
from pathlib import Path

from setup import version

from . import clonechat_protect, cloneplan
from .pipe import download


async def main():

    print(
        f"\n....:: Clonechat - v{version} ::....\n"
        + "github.com/apenasrr/clonechat/\n"
        + "---------DownloadAll----------"
    )

    session_folder = Path(".").absolute()
    client = await clonechat_protect.get_client(
        "user", session_folder=session_folder
    )

    message = "Enter the ORIGIN chat_id, chat_link or chat_username: "
    chat_origin_info = await clonechat_protect.get_chat_info_until(
        client, message
    )
    chat_origin_title = chat_origin_info["chat_title"]
    chat_origin_id = chat_origin_info["chat_id"]
    print(f"ORIGIN: {abs(chat_origin_id)}-{chat_origin_title}\n")

    # cloneplan_path
    folder_path_cloneplan = Path("protect_content") / "log_cloneplan"
    folder_path_cloneplan.mkdir(exist_ok=True)
    cloneplan_path = clonechat_protect.get_cloneplan_path(
        folder_path_cloneplan, chat_origin_id, chat_origin_title
    )

    new_clone = True
    if cloneplan_path.exists():
        new_clone = clonechat_protect.ask_for_new_clone()

    if new_clone:
        history_path = clonechat_protect.get_history_path(
            chat_origin_title, chat_origin_id
        )
        await clonechat_protect.save_history(
            client, chat_origin_id, history_path
        )

        cloneplan.save_cloneplan(history_path, cloneplan_path)
    else:
        history_path = clonechat_protect.get_recent_history(
            chat_origin_title, chat_origin_id
        )

    clonechat_protect.show_history_overview(history_path)

    # download_folder
    cache_folder = Path("protect_content") / "Cache"
    cache_folder.mkdir(exist_ok=True)
    download_folder = (
        cache_folder / f"{str(abs(chat_origin_id))}-{chat_origin_title}"
    )
    download_folder.mkdir(exist_ok=True)

    await download.pipe_download(
        client,
        chat_origin_id,
        cloneplan_path,
        download_folder,
        max_size_mb=9_999_999,
    )


if __name__ == "__main__":
    asyncio.run(main())
