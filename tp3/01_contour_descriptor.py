import csv

import cv2 as cv
import numpy


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


def add_label():
    label = input("Ingrese label: ")
    description = input("Ingrese descripcion: ")
    with open('labels.csv', 'a',
              newline='') as file:
        writer = csv.writer(file)
        writer.writerow(numpy.append(int(label), description))
        print("SAVED LABEL")
    return label, description


green_color = (0, 255, 0)
red_color = (0, 0, 255)


def main():
    window_name = "TP1"
    other_window_name = "XD"
    cv.namedWindow(window_name)
    cv.namedWindow(other_window_name)
    cap = cv.VideoCapture(0)

    cv.createTrackbar("threshold", window_name, 100, 300, trackbar_dummy_function)
    cv.createTrackbar("kernel size", window_name, 10, 20, trackbar_dummy_function)

    label, description = add_label()

    while True:
        _, original_frame = cap.read()
        threshold_value = cv.getTrackbarPos("threshold", window_name)
        kernel_radius_value = cv.getTrackbarPos("kernel size", window_name)


        gray_frame = cv.cvtColor(original_frame, cv.COLOR_RGB2GRAY)

        _, thresh = cv.threshold(gray_frame, threshold_value, 255, 0)  # could be changed for adaptiveThreshold
        denoised_frame = denoise(thresh, cv.MORPH_ELLIPSE, kernel_radius_value)

        contours, _ = cv.findContours(denoised_frame, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        if len(contours) > 0:
            biggest_contour = get_biggest_contour(contours=contours)
            cv.drawContours(original_frame, [biggest_contour], -1, red_color, 3)

        cv.imshow(window_name, denoised_frame)
        cv.imshow(other_window_name, original_frame)

        if cv.waitKey(1) & 0xFF == ord('k'):
            if biggest_contour is not None:
                with open('hu_moments.csv', 'a',
                          newline='') as file:
                    writer = csv.writer(file)
                    hu_moments = cv.HuMoments(cv.moments(biggest_contour))
                    writer.writerow(numpy.append(int(label), hu_moments))
                    print("SAVED")


        if cv.waitKey(1) & 0xFF == ord('q'): # close if Q was pressed
            break

    cap.release()




main()
