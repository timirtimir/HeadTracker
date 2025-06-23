from basicFaceMeshModule import FaceMeshDetector
import cv2 as cv
from pynput.mouse import Controller
import pyautogui
import pyvjoy as vjoy

def main():
    cam_w, cam_h = pyautogui.size()
    x_scale, y_scale = 200, 120
    screen_origin = int(cam_w/2), int(cam_h/2)
    deadzone = 2
    smoothed_x, smoothed_y = 0, 0
    smoothing_factor = 0.8

    cap = cv.VideoCapture(0)
    cap.set(3, cam_w)
    cap.set(4, cam_h)

    mouse = Controller()
    detector = FaceMeshDetector()
    j = vjoy.VJoyDevice(1)

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        img, rel_x, rel_y = detector.get_relative_position(img, target_id=4)

        if rel_x is not None and rel_y is not None:
            smoothed_x = (smoothing_factor * smoothed_x) + ((1 - smoothing_factor) * rel_x)
            smoothed_y = (smoothing_factor * smoothed_y) + ((1 - smoothing_factor) * rel_y)
            percentage_X = (smoothed_x / x_scale) * 100
            percentage_Y = (smoothed_y / y_scale) * -100
            percentage_X = max(min(percentage_X, 100), -100)
            percentage_Y = max(min(percentage_Y, 100), -100)
            # mouse.position = (percentage_X, percentage_Y)
            if abs(percentage_X) > deadzone or abs(percentage_Y) > deadzone:
                vjoy_X = int((percentage_X + 100) / 200 * 32767)
                vjoy_Y = int((percentage_Y + 100) / 200 * 32767)
                
                # Set vJoy axes
                j.set_axis(vjoy.HID_USAGE_X, vjoy_X)
                j.set_axis(vjoy.HID_USAGE_Y, vjoy_Y)
                #mouse.position = ((rel_x * scale) + screen_origin[0], (rel_y * scale) + screen_origin[1])
            
            
            
        cv.imshow("Image", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()


