import cv2
import os
import sys
import time

from datetime import datetime
from argparse import ArgumentParser


def init_cap(connection: str) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(connection)
    if not cap.isOpened():
        raise ConnectionRefusedError()
    return cap


def is_close_time(hours: int) -> bool:
    now = datetime.now()
    elapsed_seconds = (now - starting_timestamp).total_seconds
    # hours * 60 = minutes;  minutes * 60 = seconds
    max_seconds = hours * 60 * 60
    if elapsed_seconds >= max_seconds:
        return True
    return False


if __name__ == "__main__":
    # ARGUMENTS
    # if len(sys.argv) < 2:
    #     print('Uri not provided. please run  python3 acquire.py <uri>')
    # s = sys.argv[1]

    # ARGUMENTS
    parser = ArgumentParser()
    parser.add_argument(
        "uri", help="The http/rtsp uri for the stream", type=str)
    parser.add_argument("--hours", help="Max hours for acquistion", type=int, default=4)
    parser.add_argument("--zfill", help="zfill for image save", type=int, default=7)
    parser.add_argument("--img_format", help="Image save format", type=str, default="jpg")
    args = parser.parse_args()
    s = args.uri

    # Preparing steps...
    print('starting reading')

    folder_id = datetime.now().strftime("%Y_%m_%dT%H_%M")
    folder = f'frames_{folder_id}'
    try:
        os.unlink(folder)
    except:
        pass
    os.makedirs(folder, exist_ok=True)

    cap = init_cap(s)

    starting_timestamp = datetime.now()
    zfill_num = args.zfill
    image_format = args.image_format
    output_video_fps = 25
    output_video_fname = f"out_{folder_id}.mp4"

    count = 0
    break_times_max = 100
    break_times = 0
    run_for_hours = args.hours

    last_fps = 1
    # Start reading frames
    while True:
        t = time.time()
        ret, frame = cap.read()
        last_fps = (1/(time.time() - t))

        if not ret:
            if break_times >= break_times_max or is_close_time(run_for_hours):
                print(f'EOS -- End of stream (iters: {break_times})')
                break
            break_times += 1
            cap = init_cap(s)
            continue
        else:
            break_times = 0

        fname = os.path.join(
            folder, f"{str(count).zfill(zfill_num)}.{image_format}")
        cv2.imwrite(fname, frame)

        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        count += 1

    cap.release()
    cv2.destroyAllWindows()
    print('done')

    from create_video import convert_to_video
    # convert_to_video(folder)
    convert_to_video(folder, zfill_num, image_format,
                     output_video_fname, output_video_fps, speed=last_fps)
