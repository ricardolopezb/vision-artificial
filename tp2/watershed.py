import cv2 as cv
import numpy as np
from PIL import ImageColor

base_colours = ['#37AB65', '#3DF735', '#AD6D70', '#EC2504', '#8C0B90', '#C0E4FF', '#27B502', '#7C60A8', '#CF95D7',
                '#37AB65']
frame_window = 'Frame-Window'
screenshot_window = 'Screenshot-Window'
seeds_map_window = 'Seeds-Map-Window'
watershed_result_window = 'Watershed-Result-Window'


def watershed(img):
    markers = cv.watershed(img, np.int32(seeds))

    img[markers == -1] = [0, 0, 255]
    for n in range(1, 10):
        img[markers == n] = ImageColor.getcolor(base_colours[n], "RGB")

    cv.imshow(watershed_result_window, img)

    cv.waitKey()


def click_event(event, x, y, _flags, _params):
    if event == cv.EVENT_LBUTTONDOWN:
        val = int(chr(selected_key))
        points.append(((x, y), val))
        cv.circle(seeds, (x, y), 7, (val, val, val), thickness=-1)


def main():
    global points
    global seeds
    global frame
    global selected_key
    selected_key = 49  # 1 en ASCII
    points = []
    seeds = np.zeros((480,640), np.uint8)
    cv.namedWindow(frame_window)
    cv.namedWindow(screenshot_window)
    cv.namedWindow(seeds_map_window)


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
            cv.setMouseCallback(screenshot_window, click_event)

            # This line returns the width and height of the screen that will be used for the seed
            # x, y, w, h = cv.getWindowImageRect('Frame-Window')
            # print(x, y, w, h)

            while True:
                for point in points:
                    color = ImageColor.getcolor(base_colours[point[1]], "RGB")
                    val = point[1] * 20

                    x = point[0][0]
                    y = point[0][1]
                    cv.circle(screenshot_copy, (x, y), 7, val, thickness=-1)
                    cv.circle(seeds_copy, (x, y), 7, val, thickness=-1)
                    cv.putText(screenshot_copy, str(point[1]), (x - 20, y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.7,
                                color, 3)

                map = cv.applyColorMap(seeds_copy, cv.COLORMAP_JET)
                cv.imshow(seeds_map_window, map)
                cv.imshow(screenshot_window, screenshot_copy)


                key2 = cv.waitKey(100) & 0xFF

                if ord('1') <= key2 <= ord('9'):
                    selected_key = key2

                if key2 == ord('t'):
                    watershed(frame.copy())
                    points = []
                    seeds = np.zeros((480, 640), np.uint8)

                if key2 == ord('q'):
                    cv.destroyAllWindows()
                    break


    cap.release()


if __name__ == '__main__':
    main()