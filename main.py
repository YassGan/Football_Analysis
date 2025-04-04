#main.py
import os
from utils import read_video, save_video
from trackers.tracker import Tracker  

def main():
    # Get the current working directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use relative paths based on the current working directory
    video_path = os.path.join(base_dir, 'input_videos', 'input_vid.mp4')
    frames = read_video(video_path)
    print(f"Number of frames read: {len(frames)}")


    # Instantiate the Tracker
    tracker = Tracker("models/best.pt")

    # Call the method
    tracks = tracker.get_object_tracks(frames,
                                       read_from_stub=True,
                                       stub_path='stubs/track_stubs.pkl')
    

    #draw  output
    #draw object tracks
    output_video_frames=tracker.draw_annotations(frames, tracks)


        # Output video path
    output_video_path = os.path.join(base_dir, 'output_videos', 'output_vid.avi')
    save_video(output_video_frames, output_video_path)
    print(f"Video saved at: {output_video_path}")
    print("Tracks:", tracks)


if __name__ == "__main__":
    main()
