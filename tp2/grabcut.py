import cv2 as cv
import numpy as np

def create_and_resize_window(window_name, width, height):
    cv.namedWindow(window_name, cv.WINDOW_KEEPRATIO)
    cv.resizeWindow(window_name, width, height)

def grabcut_and_display():
    camera = cv.VideoCapture(0)
    
    print('Press ENTER to capture the image')
    input()

    _, image = camera.read()
    image = cv.flip(image, 1)

    mask = np.zeros(image.shape[:2], np.uint8)

    rectangle = cv.selectROI("Select frame", image, fromCenter=False, showCrosshair=True)


    cv.grabCut(image, mask, rectangle, None, None, 10, cv.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    image = image * mask2[:, :, np.newaxis]

    cv.imshow("Output with the mask", image)
    
    cv.waitKey()

if __name__ == "__main__":
    grabcut_and_display()
    cv.destroyAllWindows()
