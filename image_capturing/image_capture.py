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

    # Process the frame with MediaPipe Hands
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Display the video feed
    cv2.imshow("Hand Capture", frame)

    # Check if class name is provided
    if not class_name:
        # Wait for user input while showing the screen
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting program.")
            break
        print("Waiting for user to input a class name...")
        class_name = input("Enter the class name for the images: ")
        output_dir = os.path.join("/Users/bineethreddyn/Desktop/nnmodel/nnmodel_asl/images/captured_images", class_name)
        os.makedirs(output_dir, exist_ok=True)
        print(f"Capturing images for class: {class_name}")

    elif result.multi_hand_landmarks and captured_count < capture_limit:
        for hand_landmarks in result.multi_hand_landmarks:
            # Get the bounding box of the hand
            x_min, y_min = int(min(lm.x for lm in hand_landmarks.landmark) * w), int(min(lm.y for lm in hand_landmarks.landmark) * h)
            x_max, y_max = int(max(lm.x for lm in hand_landmarks.landmark) * w), int(max(lm.y for lm in hand_landmarks.landmark) * h)

            # Check if hand is within the bounding box
            if start_x < x_min < end_x and start_y < y_min < end_y and start_x < x_max < end_x and start_y < y_max < end_y:
                # Crop the image inside the bounding box (excluding edges)
                # Adjust cropping coordinates to exclude the bounding box lines
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