import cv2 as cv


def trackbar_dummy_function(x):
    pass


def denoise(frame, method, radius):
    kernel = cv.getStructuringElement(method, (radius, radius))
    opening = cv.morphologyEx(frame, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
    return closing


def get_biggest_contour(contours):
    max_cnt = contours[0]
    for cnt in contours:
        if cv.contourArea(cnt) > cv.contourArea(max_cnt):
            max_cnt = cnt
    return max_cnt


def compare_contours(contour_to_compare, saved_contours, max_diff):
    for contour in saved_contours:
        if cv.matchShapes(contour_to_compare, contour, cv.CONTOURS_MATCH_I2, 0) < max_diff:
            return True
    return False

def main():
    window_name = "TP1"
    cv.namedWindow(window_name)
    cap = cv.VideoCapture(0)

    cv.createTrackbar("threshold", window_name, 100, 300, trackbar_dummy_function)
    cv.createTrackbar("kernel size", window_name, 10, 20, trackbar_dummy_function)

    contour_color = (255, 0, 0)
    saved_contours = []

    while True:
        ret, frame = cap.read()

        threshold_value = cv.getTrackbarPos("threshold", window_name)
        kernel_radius_value = cv.getTrackbarPos("kernel size", window_name)

        gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        _, thresh = cv.threshold(gray_frame, threshold_value, 255, 0) # could be changed for adaptiveThreshold
        denoised_frame = denoise(thresh, cv.MORPH_ELLIPSE, kernel_radius_value)

        contours, _ = cv.findContours(denoised_frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            biggest_contour = get_biggest_contour(contours=contours)
            # hu_moments = get_hu_moments(contour=biggest_contour)
            if compare_contours(contour_to_compare=biggest_contour, saved_contours=saved_contours, max_diff=1):
                cv.drawContours(denoised_frame, biggest_contour, -1, contour_color, 20)
            cv.drawContours(denoised_frame, biggest_contour, -1, contour_color, 3)
        
        cv.imshow(window_name, denoised_frame)

        if cv.waitKey(1) & 0xFF == ord('k'):
            print("Pressed k")
            if biggest_contour is not None:
                print("biggest contour found")
                # save_moment(hu_moments=hu_moments, file_name="hu_moments.txt")
                saved_contours.append(biggest_contour)

        if cv.waitKey(1) & 0xFF == ord('q'): # close if Q was pressed
            break

    cap.release()


main()
