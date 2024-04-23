import cv2
import numpy as np

def load_image(path, color_mode=cv2.IMREAD_GRAYSCALE):
    """Load an image from the specified path in the given color mode."""
    return cv2.imread(path, color_mode)

def initialize_orb_detector():
    """Initialize and return an ORB detector."""
    return cv2.ORB_create()

def find_keypoints_and_descriptors(image, detector):
    """Detect keypoints and compute descriptors for the given image using the specified detector."""
    return detector.detectAndCompute(image, None)

def configure_matcher():
    """Configure and return a brute force matcher with the NORM_HAMMING norm and cross-check enabled."""
    return cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

def load_video(path):
    """Load and return a video capture object from the specified path."""
    return cv2.VideoCapture(path)

def process_frames(video_capture, reference_image, reference_keypoints, reference_descriptors, detector, matcher):
    """Process video frames to find and display matches with the reference descriptors."""
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = find_keypoints_and_descriptors(gray_frame, detector)
        matches = matcher.match(reference_descriptors, descriptors)
        matches = sorted(matches, key=lambda x: x.distance)

        matching_result = cv2.drawMatches(reference_image, reference_keypoints, frame, keypoints, matches[:15], None, flags=2)
        cv2.imshow("Matching", matching_result)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
            break

def main():
    volvo_image = load_image('Car_mask.jpg')
    orb_detector = initialize_orb_detector()
    reference_keypoints, reference_descriptors = find_keypoints_and_descriptors(volvo_image, orb_detector)
    matcher = configure_matcher()
    video_capture = load_video('cars_on_highway_1080p.mp4')

    try:
        process_frames(video_capture, volvo_image, reference_keypoints, reference_descriptors, orb_detector, matcher)
    finally:
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
