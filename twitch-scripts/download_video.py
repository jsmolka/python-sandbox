import api
import argparse
import os
import sys
import time
from logger import *
from video import *


def _process(video, parts):
    name = "{} {}".format(video.user, video.created_at.split("T")[0].replace("-", ""))

    pattern = os.path.join(video.id, "*.ts")
    output_ts = os.path.join(video.id, name + ".ts")
    output_mp = os.path.join(video.id, name + ".mp4")

    def combine():
        if sys.platform == "win32":
            return os.system("copy /b \"{}\" \"{}\" >nul".format(pattern, output_ts))
        else:
            return os.system("cat {} > \"{}\"".format(pattern, output_ts))

    if combine() != 0:
        log("Failed concatenating parts")
        return

    for part in parts:
        os.remove(part)

    if os.system("ffmpeg -hide_banner -loglevel panic -i \"{}\" -acodec copy -bsf:a aac_adtstoasc -vcodec copy \"{}\"".format(output_ts, output_mp)) != 0:
        log("Failed converting to video")
        return

    os.remove(output_ts)


def download_video(id):
    video = None
    try:
        video = Video(id)
        log("Downloading video", id)
    except Exception as e:
        log("Failed video request")
        log(str(e))
        return

    os.makedirs(id, exist_ok=True)

    parts = []
    finished = set()

    while True:
        for segment in video.segments:
            try:
                if segment.id in finished:
                    continue

                log("Downloading segment", segment.id + 1, "/", len(video.segments))

                response = api.get(segment.uri, stream=True)
                filename = "{}/{}".format(video.id, segment.file_name)
                with open(filename, "wb") as data:
                    for chunk in response.iter_content(chunk_size=128):
                        data.write(chunk)

                parts.append(filename)
                finished.add(segment.id)
            except Exception as e:
                log("Failed downloading segment", segment.id)
                log(str(e))

        if not video.is_live:
            break

        log("Stream is live - waiting 60 seconds")
        time.sleep(60)

        try:
            video.update()
        except Exception as e:
            log("Failed updating video")
            log(str(e))
            break

    log("Processing segments")
    _process(video, parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", help="video id", required=True)
    parser.add_argument("-l", help="log file")

    args = parser.parse_args()

    init_logger(args.l)

    download_video(args.v)
