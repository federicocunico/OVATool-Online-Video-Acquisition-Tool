import os
import sys

from argparse import ArgumentParser


def convert_to_video(folder, zfill_num, image_format, output_video_fname, output_video_fps, speed=1):
    print('trying to create the output file..')
    try:
        image_pattern = "%0{0}d.{1}".format(zfill_num, image_format)
        # ffmpeg = f"ffmpeg -i {folder}/{image_pattern} -c:v libx264 -vf fps={output_video_fps} -pix_fmt yuv420p {output_video_fname}"

        # Normal speed video with one image per frame
        ffmpeg = f"ffmpeg -r {speed} -i {folder}/{image_pattern} -c:v libx264 -framerate {output_video_fps} -pix_fmt yuv420p {output_video_fname}"
        os.system(ffmpeg)
    except:
        print('Something went wrong. try manually.')
        pass
    print("End of program")


if __name__ == "__main__":

    # if len(sys.argv) < 2:
    #     print('Please specify folder')
    #     sys.exit(0)
    # folder = sys.argv[1]
    parser = ArgumentParser()
    parser.add_argument(
        "folder", help="The folder with data", type=str)
    parser.add_argument("--fps", help="Video output fps", type=int, default=25)
    parser.add_argument("--zfill", help="Images zfill number", type=int, default=7)
    parser.add_argument("--speed", help="Relative speed of video. i.e. how many frames per second", type=str, default="1")
    args = parser.parse_args()
    
    folder = args.folder
    files = [f for f in os.listdir(
        folder) if os.path.isfile(os.path.join(folder, f))]
    zfill_num = args.zfill  # with zfill = 7, the max frame num is 9,999,999; should be enough
    output_video_fps = args.fps
    folder_id = folder.split('frames_')[1].replace(os.sep, '')
    output_video_fname = f"out_{folder_id}.mp4"
    speed = args.speed

    num_files = len(files)
    if num_files > 0:
        image_format = files[0].split('.')[-1]
        convert_to_video(folder, zfill_num, image_format,
                         output_video_fname, output_video_fps, speed)
        print('Done')
    else:
        print(f'Found {num_files} files, aborting.')
