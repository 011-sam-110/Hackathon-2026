from inference import get_model
import supervision as sv

# Load a pre-trained UI detection model
model = get_model("ui-element-detector/1") # Example model ID

# Get detections
results = model.infer("screenshot.png")[0]
detections = sv.Detections.from_inference(results)

# Print centers of all buttons
for xyxy in detections.xyxy:
    center_x = (xyxy[0] + xyxy[2]) / 2
    center_y = (xyxy[1] + xyxy[3]) / 2
    print(f"Clickable center: {center_x}, {center_y}")