import api
import os
import sys
import time
from video import Video


def _finalize(video, parts):
    name = "{} {}".format(video.user, video.created_at.split("T")[0].replace("-", ""))

    pattern = os.path.join(video.id, "*.ts")
    output_ts = os.path.join(video.id, name + ".ts")
    output_mp = os.path.join(video.id, name + ".mp4")

    code = 0
    if sys.platform == "win32":
        code = os.system("copy /b \"{}\" \"{}\" >nul".format(pattern, output_ts))
    else:
        code = os.system("cat {} > \"{}\"".format(pattern, output_ts))

    if code != 0:
        print("Cannot concatenate parts")
        return

    for part in parts:
        os.remove(part)

    if os.system("ffmpeg -hide_banner -loglevel panic -i \"{}\" -acodec copy -bsf:a aac_adtstoasc -vcodec copy \"{}\"".format(output_ts, output_mp)) != 0:
        print("Cannot convert concatenated parts")
        return

    os.remove(output_ts)


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
