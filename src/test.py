import cv2
import unittest

from detector import process_image, find_mug


class TestMugDetection(unittest.TestCase):
    def test_localization(self):
        images = ['125.0.jpg', '142.0.jpg', '197.0.jpg', '266.0.jpg', '285.0.jpg', '389.0.jpg']
        mug_coords = [None, (950, 130), (1000, 290), (530, 230), (800, 500), (1080, 420)]

        for filename, coords in zip(images, mug_coords):
            image = cv2.imread('test_images/' + filename)
            thresh = process_image(image)
            rect = find_mug(thresh)
            if rect is None:
                assert coords is None
                continue
            x, y, w, h = rect
            assert x <= coords[0] <= x + w and y <= coords[1] <= y + h

if __name__ == '__main__':
    unittest.main()
