import api
import argparse
import time
from download_video import download_video
from logger import *
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
        log("Watching user", name)
    except Exception as e:
        log("Failed user request", name)
        log(str(e))
        return

    old = _get_video_ids(user.id)

    while True:
        log("Waiting 1 hour")
        time.sleep(3600)

        new = _get_video_ids(user.id)

        log("Old videos: ", old)
        log("New videos: ", new)
        log("Difference: ", new.difference(old))

        for video_id in new.difference(old):
            download_video(video_id)

        old = new


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", help="user name", required=True)
    parser.add_argument("-l", help="log file")

    args = parser.parse_args()

    init_logger(args.l)

    watch_user(args.u)
