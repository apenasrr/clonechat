from __future__ import annotations

import asyncio
import multiprocessing


def func_subprocess(func_, dict_params: dict, pipe):

    result = asyncio.run(func_(**dict_params))
    pipe.send(result)


def time_out(
    sec_time_out: int, func_, dict_params: dict = {}, restart: bool = True
):
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(
        target=func_subprocess, args=[func_, dict_params, child_conn]
    )
    p.start()

    p.join(sec_time_out)

    if p.is_alive():
        p.terminate()
        if restart:
            print("\nTook too long. Restarting.")
            return time_out(sec_time_out, func_, dict_params, restart)
    else:
        return parent_conn.recv()
