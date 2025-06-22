from basicFaceMeshModule import FaceMeshDetector
import cv2 as cv
from pynput.mouse import Controller
import pyautogui

def main():
    cam_w, cam_h = pyautogui.size()
    scale = 2
    screen_origin = int(cam_w/2), int(cam_h/2)
    print(screen_origin)
    cap = cv.VideoCapture(0)
    cap.set(3, cam_w)
    cap.set(4, cam_h)

    mouse = Controller()
    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        img = cv.flip(img, 1)
        img, rel_x, rel_y = detector.get_relative_position(img, target_id=4)

        if rel_x is not None and rel_y is not None:
            mouse.position = ((rel_x * scale) + screen_origin[0], (rel_y * scale) + screen_origin[1])
            # print(screen_origin[0], rel_x)
            
        cv.imshow("Image", img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()


