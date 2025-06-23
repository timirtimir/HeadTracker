from basicFaceMeshModule import FaceMeshDetector
import cv2 as cv
import pyautogui
import pyvjoy as vjoy

def main():
    cam_w, cam_h = pyautogui.size()
    x_scale, y_scale = 200, 120
    prev_x, prev_y = 0, 0
    vjoy_X, vjoy_Y = int(32767/2), int(32767/2)
    deadzone_x, deadzone_y = 0, 0
    deadzone_base = 0.1


    cap = cv.VideoCapture(0)
    cap.set(3, cam_w)
    cap.set(4, cam_h)

    detector = FaceMeshDetector(minDetectCon=0.7, minTrackCon=0.7)
    print(detector.minDetectCon, detector.minTrackCon)
    j = vjoy.VJoyDevice(1)

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        img, rel_x, rel_y = detector.get_relative_position(img, target_id=4)

        if rel_x is not None and rel_y is not None:
            percentage_X = (rel_x / x_scale) * 100
            percentage_Y = (rel_y / y_scale) * -100
            percentage_X = max(min(percentage_X, 100), -100)
            percentage_Y = max(min(percentage_Y, 100), -100)

            deadzone_x = deadzone_base + percentage_X/100
            deadzone_y = deadzone_base + percentage_Y/100
            if abs(percentage_X - prev_x) > deadzone_x:   
                vjoy_X = int((percentage_X + 100) / 200 * 32767)
                prev_x = percentage_X
            if abs(percentage_Y - prev_y) > deadzone_y:   
                vjoy_Y = int((percentage_Y + 100) / 200 * 32767)
                prev_y = percentage_Y  
            print(deadzone_x, deadzone_y)
            j.set_axis(vjoy.HID_USAGE_X, vjoy_X)
            j.set_axis(vjoy.HID_USAGE_Y, vjoy_Y)
            
            
            
        # cv.imshow("Image", img)
        # if cv.waitKey(1) & 0xFF == ord('q'):
        #     break
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()


