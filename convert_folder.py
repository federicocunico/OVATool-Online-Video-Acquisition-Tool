import os
import sys

if len(sys.argv) < 2:
    print('Please specify folder')
    sys.exit(0)

folder = sys.argv[1]

files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
zfill_num = 7  # max 9,999,999

num_files = len(files)
if num_files > 0:
    print(f"Found {num_files} files. Converting with zfill: {zfill_num}")

    for i, fname in enumerate(files):
        print(f"{i+1}/{num_files}")
        tmp = fname.split('.')
        num = tmp[0]
        ext = tmp[1]
        real_num = num.zfill(zfill_num)

        dst = f"{real_num}.{ext}"

        original = os.path.join(folder, fname)
        destination = os.path.join(folder, dst)
        os.rename(original, destination)

    print('Done')
else:
    print(f'Found {num_files} files, aborting.')
