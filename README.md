# Chia Plot Mover for Windows: Efficient and Parallel Transfers

## Introduction:

In the world of **Chia** farming on **Windows**, a significant bottleneck often faced is the slow pace of plotting to HDDs, particularly with USB-connected drives. GPU plotting with compression drastically accelerates plot creation, leading to transfers becoming the primary decelerating factor.

This script offers a seamless solution. Plot to a zippy NVMe, then use this script to swiftly and **parallelly** ferry the plots to a set of slower HDDs.

## Key Features:

- **Parallel Movement**: Facilitates simultaneous transfer of multiple plots to individual HDDs, achieving maximum throughput.
- **Dynamic Destination Selection**: Chooses an apt HDD based on space availability and ensures no ongoing move processes to sidestep overlaps.
- **Intelligent Queueing & Polling**: If all HDDs are busy, the script queues the plots, consistently polling at set intervals (determined by the `polling_interval` variable) for incoming plots, thus enhancing stability.
- **Folder-based Disk Mounts**: Harnesses folder-based mounting (e.g., `c:\disks\001`, `c:\disks\002`) over traditional drive letters, addressing the constraint of drive letter scarcity in Windows.

## Requirements:

1. **Windows OS**: Tailored explicitly for Windows, the mechanism for fetching disk space is unique to this platform.
2. **Python**: Ensure the latest version of Python for Windows is installed. Acquire it [here](https://www.python.org/downloads/windows/).

## Installation:

1. **Clone the Repository**:
   ```
   gh repo clone marcweigand/chia-plot-mover
   cd chia-plot-mover
   ```

2. **Install Required Libraries**:
   ```
   pip install -r requirements.txt
   ```

## How to Adjust the Script:

You can tailor specific parameters to your setup:

- `source_dir`: Specifies the NVMe location storing new plots. Examples:
  - `"D:\Plots\"`
  - `"E:\"`
  - `f"C:\\NewPlots\\{str(i).zfill(3)}\\"` (for iterating folders)

- `dest_dirs`: Denotes the HDD directories. These are folder-mounted for streamlined sorting.
- `polling_interval`: Defines the duration (in seconds) the script waits before checking for new plots. Adjust as needed.
- `required_free_space`: The minimum free space an HDD must have to qualify as a transfer target.

## License:

This project is licensed under the GPL 3.0 license. You can read more about its permissions, conditions, and limitations [here](https://www.gnu.org/licenses/gpl-3.0.html).

## Points to Remember:

- Ensure directory permissions are in order.
- For maximum efficiency, the NVMe and HDDs shouldn't be on the same bus.
- It's designed to be robust, but TEST before you start moving plots around. I don't want you to lose existing plots.
- Prevent any potential conflicts; ensure no other processes or scripts interfere with the plots simultaneously.

## In Conclusion:

Effective plot management is the essence of unlocking your hardware's full capability. This script minimizes plot idle times, capitalizing on your NVMe's rapid performance. For issues or suggestions, feel free to raise an issue or send in a PR. Happy farming!

[Link to Repository](https://github.com/marcweigand/chia-plot-mover.git)
