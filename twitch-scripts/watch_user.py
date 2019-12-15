import api
import sys
import time
from download_video import download_video
from user import User


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
        print("Watching user", name)
    except Exception as e:
        print("Failed requesting user", name)
        print(str(e))
        return

    old = _get_video_ids(user.id)

    while True:
        print("Waiting 1 hour")
        time.sleep(3600)

        new = _get_video_ids(user.id)

        for video_id in new.difference(old):
            download_video(video_id)

        old = new


if __name__ == "__main__":
    if len(sys.argv) == 2:
        watch_user(sys.argv[1])
    else:
        print("Please provide a user name")
