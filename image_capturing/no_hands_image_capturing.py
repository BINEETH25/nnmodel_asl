import cv2
import os
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.4, min_tracking_confidence=0.6)
mp_draw = mp.solutions.drawing_utils

# Parameters for bounding box
box_width, box_height = 700, 700
box_shift_x = -500
box_color = (0, 255, 0)  # Green box

# Start capturing
cap = cv2.VideoCapture(0)
class_name = None
output_dir = None
captured_count = 0
capture_limit = 500

print("Starting video feed...")
print("Please enter a class name when ready to start capturing images.")

# Wait for the user to input the class name
class_name = input("Enter the class name for the images: ")
output_dir = os.path.join("/Users/bineethreddyn/Desktop/nnmodel/nnmodel_asl/images/captured_images", class_name)
os.makedirs(output_dir, exist_ok=True)
print(f"Capturing images for class: {class_name}")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image. Exiting...")
        break

    # Flip frame for a mirrored view
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # Define bounding box region
    start_x = w // 2 + box_shift_x
    start_y = h // 2 - box_height // 2
    end_x = start_x + box_width
    end_y = start_y + box_height

    # Draw the bounding box (for visualization only)
    cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), box_color, 2)

    # Process the frame with MediaPipe Hands (for hand detection, but not necessary for capturing)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Display the video feed
    cv2.imshow("Hand Capture", frame)

    # Capture images inside the bounding box (without waiting for hand detection)
    if captured_count < capture_limit:
        # Crop the image inside the bounding box (excluding edges)
        border_thickness = 2  # Thickness of the bounding box line
        cropped_frame = frame[start_y + border_thickness:end_y - border_thickness, 
                             start_x + border_thickness:end_x - border_thickness]

        # Save the cropped frame without landmarks
        image_path = os.path.join(output_dir, f"{captured_count}.jpg")
        cv2.imwrite(image_path, cropped_frame)
        captured_count += 1
        print(f"Captured image {captured_count}/{capture_limit}")

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if captured_count >= capture_limit:
        print(f"Capture limit reached. Saved {captured_count} images in {output_dir}.")
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print(f"Image capture completed. {captured_count} images saved in {output_dir}.")
