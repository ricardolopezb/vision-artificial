import cv2 as cv
import numpy as np
from PIL import ImageColor

frame_window = 'Frame-Window'
screenshot_window = 'Screenshot-Window'
grabcut_result_window = 'Watershed-Result-Window'



def main():
    global points
    global frame
    global selected_key
    selected_key = 49  # 1 en ASCII
    points = []
    seeds = np.zeros((480,640), np.uint8)
    cv.namedWindow(frame_window)

    cap = cv.VideoCapture(0)
    
    while True:
        _, frame = cap.read()
        frame_copy = frame.copy()
        screenshot_copy = frame.copy()
        seeds_copy = seeds.copy()
        key = cv.waitKey(100) & 0xFF
        cv.imshow(frame_window, frame)

        if key == ord('q'):
            break

        if key == 32:
            # This line returns the width and height of the screen that will be used for the seed
            # x, y, w, h = cv.getWindowImageRect('Frame-Window')
            # print(x, y, w, h)
            cv.imshow(frame_window, screenshot_copy)

            mask = np.zeros(screenshot_copy.shape[:2], np.uint8)

            # These are arrays used by the algorithm internally. You just create two np.float64 type zero arrays
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)

            # usamos roi para agarrar el rect
            rect = cv.selectROI(frame_window, screenshot_copy, fromCenter=False, showCrosshair=True)
            # rect = (x1, y1), (x2, y2)

            cv.grabCut(screenshot_copy, mask, rect, bgdModel, fgdModel, 10, cv.GC_INIT_WITH_RECT)

            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

            img = screenshot_copy * mask2[:, :, np.newaxis]
            cv.imshow(frame_window, img)
            cv.waitKey()
            while True:
                key = cv.waitKey(100) & 0xFF
                if key == ord('q'):
                    break


    cap.release()


if __name__ == '__main__':
    main()