from ultralytics import YOLO
import supervision as sv
import os
import pickle
import sys
import cv2
import numpy as np  # Make sure this is at the top
import pandas as pd


sys.path.append('../')
from utils import get_center_of_bbox, get_bbox_area


class Tracker:
    def __init__(self, model_path): 
        self.model = YOLO(model_path)
        self.trackers = sv.ByteTrack()


    def interpolate_ball_positions(self, ball_positions):
        # Extract the bbox from each ball detection
        extracted_positions = [x.get(1, {}).get('bbox', []) for x in ball_positions]

        # Filter out empty bboxes (which have no values or not exactly 4 elements)
        extracted_positions = [bbox for bbox in extracted_positions if len(bbox) == 4]

        if not extracted_positions:
            print("[WARNING] No valid ball positions to interpolate.")
            return [{} for _ in ball_positions]  # Maintain same length, return empty dicts

        # Create DataFrame from valid bboxes
        df_ball_positions = pd.DataFrame(extracted_positions, columns=['x1', 'y1', 'x2', 'y2'])

        # Interpolate and fill
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill().ffill()

        # Replace original empty bboxes with interpolated ones
        interpolated = []
        idx = 0
        for x in ball_positions:
            if x.get(1, {}).get('bbox', []) and len(x[1]['bbox']) == 4:
                interpolated.append({1: {"bbox": df_ball_positions.iloc[idx].tolist()}})
                idx += 1
            else:
                interpolated.append({1: {"bbox": df_ball_positions.iloc[min(idx, len(df_ball_positions)-1)].tolist()}})

        return interpolated


    def detect_frames(self, frames):
        batch_size = 20
        detections = []
        for i in range(0, len(frames), batch_size):
            detections_batch = self.model(frames[i:i+batch_size], conf=0.1)
            detections += detections_batch
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        if read_from_stub and stub_path is not None and os.path.exists(stub_path):
            # Load the stub
            with open(stub_path, 'rb') as f:
                tracks = pickle.load(f)
            return tracks

        detections = self.detect_frames(frames)

        tracks = {
            "players": [],
            "referees": [],
            "ball": [],
        }

        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v: k for k, v in cls_names.items()}  # Reverse mapping

            # Convert to supervision detection format
            detection_supervision = sv.Detections.from_ultralytics(detection)

            # Convert goalkeeper to a normal player
            for object_ind, class_id in enumerate(detection_supervision.class_id):
                class_name = cls_names.get(int(class_id), "").lower()
                if class_name == 'goalkeeper':
                    detection_supervision.class_id[object_ind] = cls_names_inv.get('player', class_id)

            # Track objects
            detection_with_tracks = self.trackers.update_with_detections(detection_supervision)

            tracks["players"].append({})
            tracks["referees"].append({})
            tracks["ball"].append({})

            for frame_detection in detection_with_tracks:
                bbox = frame_detection[0].tolist()
                cls_id = int(frame_detection[3])
                track_id = int(frame_detection[4])

                class_name = cls_names.get(cls_id, "").lower()

                if class_name == 'player':
                    tracks["players"][frame_num][track_id] = {"bbox": bbox}

                elif class_name == 'referee':
                    tracks["referees"][frame_num][track_id] = {"bbox": bbox}

                elif class_name == 'ball':
                    tracks["ball"][frame_num][track_id] = {"bbox": bbox}



        if stub_path is not None:
            # Save the stub
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks, f)

        return tracks

    def draw_ellipse(self, frame, bbox, color, track_id=None):
        y2 = int(bbox[3])
        x_center, _ = get_center_of_bbox(bbox)
        x_center = int(x_center)  # Make sure it's an int
        width = int(get_bbox_area(bbox))  # Ensure it's a Python int

        axes = (int(width), int(0.35 * width))  # Tuple of ints

        cv2.ellipse(
            frame,
            center=(x_center, y2),
            axes=axes,
            angle=0.0,
            startAngle=45,
            endAngle=235,
            color=color,
            thickness=2,
            lineType=cv2.LINE_4,
        )

        rectangle_width=40
        rectangle_height=20

        x1_rect=x_center-rectangle_width//2
        x2_rect=x_center+rectangle_width//2

        y1_rect=y2-rectangle_height//2
        y2_rect=y2+rectangle_height//2

        if track_id is not None:
            cv2.rectangle(frame, (x1_rect, y1_rect), (x2_rect, y2_rect), color, cv2.FILLED)

            x1_text = x1_rect+12
            if track_id >99:
                x1_text -=10

            cv2.putText(
                frame,
                str(track_id),
                (x1_text, y2+5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )

        return frame
    




    def draw_triangle(self, frame, bbox, color):
        y = int(bbox[1])
        x, _ = get_center_of_bbox(bbox)
        x = int(x)

        triangle_points = np.array([
            [x, y],
            [x - 10, y + 20],
            [x + 10, y + 20]
        ], dtype=np.int32)


        cv2.drawContours(frame, [triangle_points], 0, color, thickness=cv2.FILLED)
        cv2.drawContours(frame, [triangle_points], 0, color, 2)

        return frame



    def draw_annotations(self, video_frames, tracks):
        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()

            player_dict = tracks["players"][frame_num]
            referee_dict = tracks["referees"][frame_num]
            ball_dict = tracks["ball"][frame_num]

            # Removed the redundant line that was overwriting referee_dict

            # Draw players
            for track_id, player in player_dict.items():
                color=player.get("color", (0, 0, 255))
                frame = self.draw_ellipse(frame, player["bbox"], color, track_id)

            # Draw referees
            for _,  referee in referee_dict.items():
                frame = self.draw_ellipse(frame, referee["bbox"], color=(255, 0, 0))


            # Draw ball
            for track_id, ball in ball_dict.items():
                frame =self.draw_triangle(frame, ball["bbox"], color=(0, 0, 255))

            output_video_frames.append(frame)

        return output_video_frames
