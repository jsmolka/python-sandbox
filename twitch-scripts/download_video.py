import api
import os
import sys
import time
from video import Video


def _finalize(video, parts):
    name = "{} {}".format(video.user, video.created_at.split("T")[0].replace("-", ""))

    f_list = os.path.join(video.id, "list.txt")
    f_concat_ts = os.path.join(video.id, name + ".ts")
    f_concat_mp = os.path.join(video.id, name + ".mp4")

    lines = ["file '{}'".format(part) for part in parts]
    with open(f_list, "w") as f:
        f.write("\n".join(lines))

    if os.system("ffmpeg -loglevel quiet -f concat -i \"{}\" -c copy \"{}\"".format(f_list, f_concat_ts)) == 0:
        os.remove(f_list)
        for part in parts:
            os.remove(part)

        if os.system("ffmpeg -loglevel quiet -i \"{}\" -bsf:a aac_adtstoasc -acodec copy -vcodec copy \"{}\"".format(f_concat_ts, f_concat_mp)) == 0:
            os.remove(f_concat_ts)
        else:
            print("Cannot convert concatenated files")    
    else:
        print("Cannot concatenate files")


def download_video(id):
    video = None
    try:
        video = Video(id)
        print("Downloading video", id)
    except Exception as e:
        print("Failed requesting video", id)
        print(str(e))
        return

    os.makedirs(id, exist_ok=True)

    parts = []
    finished = set()

    while True:
        for segment in video.segments:
            try:
                if segment.id in finished:
                    continue

                is_last = segment.id == len(video.segments) - 1

                print("Downloading segment {} / {}".format(segment.id + 1, len(video.segments)), end='\n' if is_last else '\r')

                response = api.get(segment.uri, stream=True)
                filename = "{}/{}".format(video.id, segment.file_name)
                with open(filename, "wb") as data:
                    for chunk in response.iter_content(chunk_size=128):
                        data.write(chunk)

                parts.append(filename)
                finished.add(segment.id)
            except Exception as e:
                print("Skipped segment", segment.id)
                print(str(e))

        if not video.is_live:
            break

        print("Stream is live, waiting 60 seconds")
        time.sleep(60)

        try:
            video.update()
        except Exception as e:
            print("Failed updating video")
            print(str(e))
            break

    print("Finalizing video")
    _finalize(video, parts)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        download_video(sys.argv[1])
    else:
        print("Please provide a video id")
