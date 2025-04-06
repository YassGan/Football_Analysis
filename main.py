#main.py
import os
from utils import read_video, save_video
from trackers.tracker import Tracker  
import cv2

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
    



    output_video_frames = tracker.draw_annotations(frames, tracks)
    frame = output_video_frames[0]

    for track_id, track in tracks["players"][0].items():
        bbox = track["bbox"]
        x1, y1, x2, y2 = map(int, bbox)

        cropped_image = frame[y1:y2, x1:x2]
        save_path = os.path.join(base_dir, 'output_videos', f'player_{track_id}.png')
        cv2.imwrite(save_path, cropped_image)
        print(f"Saved cropped image at: {save_path}")

        output_video_path = os.path.join(base_dir, 'output_videos', 'output_vid.avi')
        save_video(output_video_frames, output_video_path)
        print(f"Video saved at: {output_video_path}")
        print("Tracks:", tracks)
        break


if __name__ == "__main__":
    main()
