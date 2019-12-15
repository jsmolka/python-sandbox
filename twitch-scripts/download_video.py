import api
import os
import sys
import time
from video import Video


def _finalize(video, parts):
    name = "{} {}".format(video.user, video.created_at.split("T")[0].replace("-", ""))

    output = os.path.join(video.id, name + ".mp4")

    if os.system("ffmpeg -i \"concat:{}\" -c copy -bsf:a aac_adtstoasc \"{}\"".format("|".join(parts), output)) == 0:
        for part in parts:
            os.remove(part)
    else:
        print("Cannot concatenate parts")


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
