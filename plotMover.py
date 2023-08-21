import os
import time
import shutil
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import ctypes

source_dir = 'D:\\'
dest_dirs = [f'C:\\Disks\\{str(i).zfill(3)}\\' for i in range(1, 26)]
polling_interval = 5  # seconds
required_free_space = 82 * (1024 ** 3)  # bytes
executor = ThreadPoolExecutor(max_workers=5)

plot_queue = deque()
busy_destinations = set()

def move_plot_file(file_path, destination):
    try:
        mv_file = file_path.replace('.plot', '.plot-mv')
        os.rename(file_path, mv_file)
        print(f"Renaming {file_path} to {mv_file} for in-place transfer...")

        # Define destination path
        dest_path = os.path.join(destination, os.path.basename(mv_file))
        
        # Move the file across drives
        shutil.move(mv_file, dest_path)
        
        free_space = get_free_space(destination) / (1024 ** 3)  # Convert bytes to GB
        total_space = get_total_space(destination) / (1024 ** 3)  # Convert bytes to GB
        print(f"Transferred {mv_file} to {dest_path}. Chose destination {destination} due to no ongoing transfer and {free_space:.2f}GB of {total_space:.2f}GB available.")

        # Rename back to .plot
        try:
            final_path = dest_path.replace('.plot-mv', '.plot')
            os.rename(dest_path, final_path)
            print(f"Renamed {dest_path} to {final_path}")
        except Exception as ren_err:
            print(f"Error renaming file {dest_path}: {ren_err}")

    except Exception as e:
        print(f"Error while moving {file_path} to {destination}: {e}")

    finally:
        busy_destinations.remove(destination)

def get_free_space(folder):
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value

def get_total_space(folder):
    total_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), ctypes.pointer(total_bytes), None, None)
    return total_bytes.value

def get_available_destination():
    valid_dirs = [dir for dir in dest_dirs 
                  if dir not in busy_destinations 
                  and get_free_space(dir) >= required_free_space 
                  and not any([file for file in os.listdir(dir) if file.endswith('.plot-mv')])]

    if not valid_dirs:
        return None

    dir = valid_dirs[0]
    busy_destinations.add(dir)
    return dir

while True:
    print("Polling for .plot files...")
    plot_files = [os.path.join(source_dir, file) for file in os.listdir(source_dir) if file.endswith('.plot')]
    plot_queue.extend(plot_files)
    print(f"Detected {len(plot_files)} new plot files.")

    while plot_queue:
        dest_dir = get_available_destination()
        if dest_dir:
            file_to_move = plot_queue.popleft()
            print(f"Initiating transfer for: {file_to_move}")
            executor.submit(move_plot_file, file_to_move, dest_dir)
        else:
            print("Waiting for a destination to become available...")
            time.sleep(polling_interval)

    time.sleep(polling_interval)
