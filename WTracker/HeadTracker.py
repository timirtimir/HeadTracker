from basicFaceMeshModule import FaceMeshDetector
import cv2 as cv
import pyautogui
import pyvjoy as vjoy

def main():
    # Initialize camera and vJoy constants
    cam_w, cam_h = pyautogui.size()
    x_scale, y_scale = 200, 120
    prev_x, prev_y = 0, 0
    vjoy_x, vjoy_y = int(32767/2), int(32767/2)
    deadzone_x, deadzone_y = 0, 0
    deadzone_base = 0.1

    # Initialize camera
    cap = cv.VideoCapture(0)
    cap.set(3, cam_w)
    cap.set(4, cam_h)

    # Initialize FaceMeshDetector and vJoy device
    detector = FaceMeshDetector(minDetectCon=0.7, minTrackCon=0.7)
    print(detector.minDetectCon, detector.minTrackCon)
    j = vjoy.VJoyDevice(1)

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        img, rel_x, rel_y = detector.get_relative_position(img, target_id=4, draw=False)
        lm_list = detector.get_lm_list(img)
        if len(lm_list) != 0:
            x1, y1 = lm_list[386][1], lm_list[386][2]
            x2, y2 = lm_list[374][1], lm_list[374][2]

            cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            
        if rel_x is not None and rel_y is not None:
            # Set percentage values based on the relative position
            percentage_x = (rel_x / x_scale) * 100
            percentage_y = (rel_y / y_scale) * -100
            percentage_x = max(min(percentage_x, 100), -100)
            percentage_y = max(min(percentage_y, 100), -100)

            # Set deadzone values that increase linearly for smoothing
            deadzone_x = deadzone_base + percentage_x/100
            deadzone_y = deadzone_base + percentage_y/100

            # Implement the deadzone logic and move the vJoy axes
            if abs(percentage_x - prev_x) > deadzone_x:   
                vjoy_x = int((percentage_x + 100) / 200 * 32767)
                prev_x = percentage_x
            if abs(percentage_y - prev_y) > deadzone_y:   
                vjoy_y = int((percentage_y + 100) / 200 * 32767)
                prev_y = percentage_y  
            print(deadzone_x, deadzone_y)
            j.set_axis(vjoy.HID_USAGE_X, vjoy_x)
            j.set_axis(vjoy.HID_USAGE_Y, vjoy_y)
            
            
            
        cv.imshow("Image", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()


