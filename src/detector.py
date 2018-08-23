from collections import deque

import cv2
import numpy as np

from video_stream import VideoStream


def process_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blue_lower = np.array((85, 64, 23), "uint8")
    blue_upper = np.array((117, 176, 179), "uint8")
    return cv2.inRange(hsv, blue_lower, blue_upper)


def find_mug(image):
    _, contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours):
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 4000:
            return cv2.boundingRect(max_contour)


def calculate_sequence(in_path, out_path, debug=False):
    sequence = []
    detections = deque(10 * [False], 10)
    object_present = False
    with VideoStream(in_path, loop=False) as stream:
        while True:
            image = stream.read()
            if image is None:
                break

            thresh = process_image(image)
            rect = find_mug(thresh)
            detections.append(rect is not None)
            if rect is not None:
                x, y, w, h = rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            object_detected = sum(detections) >= 5
            if object_detected != object_present:
                text = 'Appeared' if object_detected else 'Disappeared'
                sequence_frame = cv2.resize(image, None, fx=0.25, fy=0.25)
                cv2.putText(sequence_frame, text, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                sequence.append(sequence_frame)
            object_present = object_detected

            if debug:
                if len(sequence):
                    cv2.imshow("Emergence", sequence[-1])

                cv2.imshow("Card Detector", image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    if debug:
        cv2.destroyAllWindows()
    cv2.imwrite(out_path, image_grid(sequence))


def image_grid(images, row_size=4):
    if len(images):
        blank = np.full_like(images[0], 255)
    else:
        return np.full((250, 250, 3), 255)
    rows = [[img for img in images[i * row_size:(i + 1) * row_size]] for i in range(len(images) // row_size)]
    if len(images) % row_size:
        rows.append([img for img in images[-(len(images) % row_size):]] +
                    [blank for _ in range(row_size - len(images) % row_size)])
    rows = [np.concatenate(row, axis=1) for row in rows if len(row)]
    return np.concatenate(rows)


if __name__ == "__main__":
    calculate_sequence("../mug.ogv", "static/sequence.jpg", True)
    cv2.imshow("Sequence", cv2.imread("static/sequence.jpg"))
    cv2.waitKey(0)
