import cv2 as cv


def trackbar_dummy_function(x):
    pass


def denoise(frame, method, radius):
    kernel = cv.getStructuringElement(method, (radius, radius))
    opening = cv.morphologyEx(frame, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
    return closing


def get_biggest_contour(contours):
    if len(contours) == 0:
        return None
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
def add_label(contour, frame, label, color):
    M = cv.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv.putText(frame, label, (cX-31, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


green_color = (0, 255, 0)
red_color = (0, 0, 255)

def get_contour_label(contour_labels_dict, compare_contour):
    for label, contour in contour_labels_dict.items():
        if cv.matchShapes(compare_contour, contour, cv.CONTOURS_MATCH_I2, 0) < 1:
            return label
    return "Not Found"

def main():
    window_name = "TP1"
    other_window_name = "XD"
    cv.namedWindow(window_name)
    cv.namedWindow(other_window_name)
    cap = cv.VideoCapture(0)

    cv.createTrackbar("threshold", window_name, 100, 300, trackbar_dummy_function)
    cv.createTrackbar("kernel size", window_name, 10, 20, trackbar_dummy_function)

    my_contours_dict = {}
    saved_contours = my_contours_dict.values()

    while True:
        _, original_frame = cap.read()
        threshold_value = cv.getTrackbarPos("threshold", window_name)
        kernel_radius_value = cv.getTrackbarPos("kernel size", window_name)


        gray_frame = cv.cvtColor(original_frame, cv.COLOR_RGB2GRAY)
        _, thresh = cv.threshold(gray_frame, threshold_value, 255, 0) # could be changed for adaptiveThreshold
        denoised_frame = denoise(thresh, cv.MORPH_ELLIPSE, kernel_radius_value)

        contours, _ = cv.findContours(denoised_frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            for contour in contours:
                contour_color = green_color if compare_contours(contour, saved_contours, 1) else red_color
                cv.drawContours(denoised_frame, [contour], -1, contour_color, 3) # this should work but its not working
                cv.drawContours(original_frame, [contour], -1, contour_color, 3)
                add_label(contour, original_frame, get_contour_label(my_contours_dict, contour), contour_color)

        cv.imshow(window_name, denoised_frame)
        cv.imshow(other_window_name, original_frame)

        biggest_contour = get_biggest_contour(contours=contours)

        if cv.waitKey(1) & 0xFF == ord('k'):
            if biggest_contour is not None:
                input_label = input("Set a label for the contour: ")
                my_contours_dict[input_label] = biggest_contour

        if cv.waitKey(1) & 0xFF == ord('q'): # close if Q was pressed
            break

    cap.release()


main()
