from __future__ import annotations

import math
import sys
import time


def progress_bar(current, total, start, prefix="Progress"):

    now = time.time()
    diff = now - start
    percentage = current * 100 / total
    speed = current / diff
    elapsed_time = round(diff) * 1000
    time_to_completion = round((total - current) / speed) * 1000
    estimated_total_time = elapsed_time + time_to_completion

    elapsed_time = TimeFormatter(milliseconds=elapsed_time)
    estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

    progress = "[{0}{1}] | {2}: {3}% | ".format(
        "".join(["●" for i in range(math.floor(percentage / 10))]),
        "".join(["○" for i in range(10 - math.floor(percentage / 10))]),
        prefix,
        round(percentage, 2),
    )

    tmp = progress + "{0} of {1} | Speed: {2}/s | ETA: {3} | ".format(
        humanbytes(current),
        humanbytes(total),
        humanbytes(speed),
        estimated_total_time if estimated_total_time != "" else "0 s",
    )

    sys.stdout.write(tmp)
    sys.stdout.flush()
    sys.stdout.write("\b" * len(tmp))
    sys.stdout.flush()


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + "B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]
