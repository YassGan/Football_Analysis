#main.py
import os
from utils import read_video, save_video
from trackers.tracker import Tracker  
import cv2
from team_assigner import TeamAssigner

def main():
    # Get the current working directory 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use relative paths based on the current working directory
    video_path = os.path.join(base_dir, 'input_videos', 'input_vid.mp4')
    frames = read_video(video_path)
    print(f"Number of frames read: {len(frames)}")


    # Instantiate the Tracker
    tracker = Tracker("models/best3.pt")

    # Call the method
    tracks = tracker.get_object_tracks(frames,
                                       read_from_stub=True,
                                       stub_path='stubs/track_stubs.pkl')
    

    ## Assing player teams
    team_assigner = TeamAssigner()
    team_assigner.assign_teams(frames[0], tracks['players'][0])

    ##loop through the frames for each player and assign the team
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team=team_assigner.get_player_team(frames[frame_num], track['bbox'], player_id)
            tracks['players'][frame_num][player_id]['team'] = team
            tracks['players'][frame_num][player_id]['color'] = team_assigner.team_colors[team]
            print(f"Frame {frame_num}, Player {player_id}: Team={team}, Assigned Color={tracks['players'][frame_num][player_id]['color']}")


    output_video_frames = tracker.draw_annotations(frames, tracks)
    save_video(output_video_frames, 'output_videos/output_vid.avi')



if __name__ == "__main__":
    main()
