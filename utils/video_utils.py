# utils/video_utils.py
import cv2

def read_video(video_path):
    cap =cv2.VideoCapture(video_path)
    frames=[]
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames


def save_video(output_video_frames, output_video_path):
    # Use 'mp4v' codec for MP4 format, 'XVID' is for AVI
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # For MP4 format
    frame_height, frame_width, _ = output_video_frames[0].shape  # Get the resolution of the first frame
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (frame_width, frame_height))  # Use dynamic resolution
    
    for frame in output_video_frames:
        # Resize frame to ensure it's consistent with the output resolution
        frame = cv2.resize(frame, (frame_width, frame_height))
        out.write(frame)
    
    out.release()