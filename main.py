#main.py
import os
from utils import read_video, save_video

def main():
    # Get the current working directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use relative paths based on the current working directory
    video_path = os.path.join(base_dir, 'input_videos', 'input_vid.mp4')
    frames = read_video(video_path)
    print(f"Number of frames read: {len(frames)}")

    # Output video path
    output_video_path = os.path.join(base_dir, 'output_videos', 'output_vid.avi')
    save_video(frames, output_video_path)
    print(f"Video saved at: {output_video_path}")

if __name__ == "__main__":
    main()
