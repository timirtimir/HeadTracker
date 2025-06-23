import cv2 as cv
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self, staticMode = False, maxFaces = 1, minDetectCon = 0.7, minTrackCon = 0.7):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectCon = minDetectCon
        self.minTrackCon = minTrackCon
        self.origin_point = None

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces = self.maxFaces, static_image_mode = self.staticMode, min_detection_confidence = self.minDetectCon, min_tracking_confidence = self.minTrackCon) #self.staticMode, self.maxFaces, self.minDetectCon, self.minTrackCon
        self.drawSpec = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)

    def findFaceMesh(self, img, draw = True, target_id = None):

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = self.faceMesh.process(imgRGB)
        target_coord = None
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_TESSELATION, self.drawSpec, self.drawSpec)
                
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw , ic = img.shape
                    x, y = int(lm.x*iw), int(lm.y*ih)
                    if id == target_id:
                        target_coord = (x, y)
                        #print(target_coord)
        return img, target_coord   
    
    def get_relative_position(self, img, target_id=4, draw=True):
        img, coord = self.findFaceMesh(img, draw=draw, target_id=target_id)
        rel_x, rel_y = None, None
        if coord is not None:
            if self.origin_point is None:
                self.origin_point = coord
            rel_x = coord[0] - self.origin_point[0]
            rel_y = coord[1] - self.origin_point[1]
        return img, rel_x, rel_y
    
# def main():
#     wCam, hCam = 1280, 720
#     cap = cv.VideoCapture(0)
#     cap.set(3, wCam)
#     cap.set(4, hCam)
#     pTime = 0
#     detector = FaceMeshDetector()
#     while True: 
#         success, img = cap.read()
#         img = cv.flip(img, 1)
#         img, rel_x, rel_y = detector.get_relative_position(img, target_id=4)
#         if rel_x is not None and rel_y is not None:
#             print(rel_x, rel_y)
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#         cv.putText(img, f'FPS: {int(fps)}', (20, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
#         cv.imshow("Image", img)
#         if cv.waitKey(1) & 0xFF == ord('q'): 
#             break
        
#     cap.release()
#     cv.destroyAllWindows()
    
# if __name__ == '__main__':
#     main()
    