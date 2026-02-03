from basicFaceMeshModule import FaceMeshDetector
import cv2 as cv
import pyautogui
import keyboard as kb
import pyvjoy as vjoy
import time
import threading 

class HeadTracker:
    def __init__(self, x_scale = 200, y_scale = 120, deadzone_base = 0.1, threshold = 88):
        # Initialise camera and vJoy constants 
        self.cam_w, self.cam_h = pyautogui.size()
        self.rel_x, self.rel_y = 0, 0
        self.percentage_x, self.percentage_y = 0, 0
        self.prev_x, self.prev_y = 0, 0
        self.vjoy_centre = 32768 // 2
        self.vjoy_x, self.vjoy_y = self.vjoy_centre, self.vjoy_centre
        self.vjoy_status = False
        self.deadzone_x, self.deadzone_y = 0, 0
        self.initial_len_line = None
        self.below_threshold = False
        self.stop_thread = threading.Event()

        self.x_scale, self.y_scale = x_scale, y_scale
        self.threshold = threshold
        self.deadzone_base = deadzone_base

        # Initialise camera
        self.cap = cv.VideoCapture(0)
        self.cap.set(3, self.cam_w)
        self.cap.set(4, self.cam_h)

        # Initialise FaceMeshDetector and vJoy device
        self.detector = FaceMeshDetector(minDetectCon=0.7, minTrackCon=0.7)
        
        self.j = self.initialise_vjoy()
    def run(self):
        while not self.stop_thread.is_set():
            if self.j is not None:
                self.vjoy_status = True
                success, img = self.cap.read()
                if not success:
                    continue
                img = cv.flip(img, 1)
                img, self.rel_x, self.rel_y = self.detector.get_relative_position(img, target_id=4, draw=False)
                lm_list = self.detector.get_lm_list(img)
                # Logic for blink detection
                if len(lm_list) != 0:
                    x1, y1 = lm_list[386][1], lm_list[386][2]
                    x2, y2 = lm_list[374][1], lm_list[374][2]

                    cv.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    len_line = ((x2 - x1) + (y2 - y1))
                    if self.initial_len_line is None:
                        self.initial_len_line = len_line
                    else:
                        line_percentage = len_line / self.initial_len_line * 100
                        # if self.below_threshold and line_percentage >= self.threshold:
                        #     pyautogui.press('y')
                        # elif not self.below_threshold and line_percentage < self.threshold:
                        #     pyautogui.press('y')
                        self.below_threshold = line_percentage < self.threshold
                if self.rel_x is not None and self.rel_y is not None:
                    # Set percentage values based on the relative position
                    self.percentage_x = (self.rel_x / self.x_scale) * 100
                    self.percentage_y = (self.rel_y / self.y_scale) * -100
                    self.percentage_x = max(min(self.percentage_x, 100), -100)
                    self.percentage_y = max(min(self.percentage_y, 100), -100)

                    # Set deadzone values that increase linearly for smoothing
                    self.deadzone_x = self.deadzone_base + self.percentage_x/100
                    self.deadzone_y = self.deadzone_base + self.percentage_y/100

                    # Implement the deadzone logic and move the vJoy axes
                    if abs(self.percentage_x - self.prev_x) > self.deadzone_x:   
                        self.vjoy_x = int((self.percentage_x + 100) / 200 * 32768)
                        self.prev_x = self.percentage_x
                    if abs(self.percentage_y - self.prev_y) > self.deadzone_y:   
                        self.vjoy_y = int((self.percentage_y + 100) / 200 * 32768)
                        self.prev_y = self.percentage_y  
                    self.j.set_axis(vjoy.HID_USAGE_X, self.vjoy_x)
                    self.j.set_axis(vjoy.HID_USAGE_Y, self.vjoy_y)
            else:
                self.vjoy_status = False
                self.j = self.initialise_vjoy()
            time.sleep(0.004)
        # Exit program and recenter the joystick
        self.cap.release()
        self.j.set_axis(vjoy.HID_USAGE_X, self.vjoy_centre)
        self.j.set_axis(vjoy.HID_USAGE_Y, self.vjoy_centre)
    def stop(self):
        self.stop_thread.set()
    def initialise_vjoy(self):
        try:
            return vjoy.VJoyDevice(1)
        except:
            return None