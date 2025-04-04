from utils import read_video, save_video
from trackers import Tracker

def main():
    # Initialize the tracker with the model path
    video_frames=read_video('input_videos/input_vid.mp4')

    tracker=Tracker('models/best.pt')

    #save the video with the detections
    tracks=tracker.get_object_tracks(video_frames)
    save_video(tracks, 'output_videos/output_vid.mp4')

if __name__ == "__main__":
    main()