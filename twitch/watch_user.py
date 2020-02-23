import api
import argparse
import time
from download_video import *
from printl import *
from user import *


def _get_video_ids(user_id):
    json = api.get_json("helix/videos", params={"user_id": user_id})

    video_ids = set()
    for video in json.get("data", []):
        video_ids.add(video.get("id"))

    return video_ids


def watch_user(name):
    user = None
    try:
        user = User(name)
        printl("Watching user", name)
    except Exception as e:
        printl("Failed user request", name)
        printl(str(e))
        return

    old = _get_video_ids(user.id)

    while True:
        printl("Waiting 1 hour")
        time.sleep(3600)

        new = _get_video_ids(user.id)
        dif = new.difference(old)

        printl("Difference: ", dif)

        for video_id in dif:
            download_video(video_id)

        old.update(dif)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="user name", required=True)
    parser.add_argument("-l", help="log file")

    args = parser.parse_args()

    printl_init(args.l)

    watch_user(args.u)
