import cv2 as cv


def trackbar_dummy_function(x):
    print("DUMMY", x)



def main():
    window_name = "TP1"
    cv.namedWindow(window_name)
    cap = cv.VideoCapture(0)

    cv.createTrackbar("threshold", window_name, 0, 300, trackbar_dummy_function)

    while True:
        ret, frame = cap.read()
        threshold_value = cv.getTrackbarPos("threshold", window_name)
        gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        ret, thresh = cv.threshold(gray_frame, threshold_value, 255, 0) # could be changed for adaptiveThreshold
        cv.imshow(window_name, thresh)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


main()
