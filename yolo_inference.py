from ultralytics import YOLO

model =YOLO('yolov8x')

results=model.predict('input_videos/input_vid.mp4',save=True) ##It will output the same video with the boxes of the detected objects
print(results[0]) ##The result of the first frame


# print("---------------------------")
# for box in results[0].boxes: ##The box referes to the detected object
#     print(box)
