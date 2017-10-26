from collections import deque
from threading import Thread
import numpy as np
import cv2


class Follow():

    def __init__(self):

        # Capture the webcam
        self.camera = cv2.VideoCapture(-1)
        self.camera.set(3,1920)
        self.camera.set(4,1080)

        # Ball (BGR)
        self.bl = [40, 60, 130]
        self.bu = [55, 255, 255]

        # Points for our tracker
        self.bpts = deque()

        # Line trail
        self.line = (0, 89, 217)

        # Min/max radius
        self.min_radius = 10
        self.max_radius = 100

        # Line thickness
        self.buff = 10

        # Pause drawing
        self.pause = 0

        # Size of roi square
        self.roi_size = 10

        # List of colors
        self.colors = {
            114: (0, 0, 255),     # red
            98: (255, 0, 0),      # blue
            103: (85, 255, 127),  # green
            121: (0, 255, 255),   # yellow
            111: (0, 89, 217),    # orange
            107: (0, 0, 0),       # black
            119: (255, 255, 255)  # white
        }

        # Morphology Kernel
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))



    def calibrate(self):

        # Roi size
        r = self.roi_size

        # Calibration count
        i = 0

        while not self.pause:

            # Grab the current web frame
            frame = self.camera.read()[1]

            # Deep copy
            img = frame.copy()

            # Size of frame
            y, x, _ = np.shape(img)

            # Image locations
            if i == 0:
                xx, yy = int(x - x/10), int(y/8)                    # Upper Left
            elif i == 1:
                xx, yy = int(x - x/10), int(y - y/2)                # Center Left
            elif i == 2:
                xx, yy = int(x - x/10), int(y - y/8)                # Lower Left
            elif i == 3:
                xx, yy = int(x - x/2), int(y/8)                     # Upper Center
            elif i == 4:
                xx, yy = int(x - x/2), int(y - y/2)                 # Center Center
            elif i == 5:
                xx, yy = int(x - x/2), int(y - y/8)                 # Lower Center
            elif i == 6:
                xx, yy = int(x/10), int(y/8)                        # Upper Right
            elif i == 7:
                xx, yy = int(x/10), int(y - y/2)                    # Center Right
            elif i == 8:
                xx, yy = int(x/10), int(y - y/8)                    # Lower Right

            # Draw square
            cv2.rectangle(img, (xx-r, yy-r), (xx+r, yy+r), (0, 0, 255), 2)

            # Flip frame to help with movement
            img = cv2.flip(img, 1)

            # Show the frame
            cv2.imshow('Frame', img)

            # exit on escape
            k = cv2.waitKey(5) & 0xFF

            if k == 27:
                self.halt = 1
                break

            # Capture color on c
            if k == 99:
                roi = frame[yy-r:yy+r,xx-r:xx+r]

                # Append the hsv data for statistics
                if 'hsv' in locals():
                    np.append(hsv, cv2.cvtColor(roi, cv2.COLOR_BGR2HSV))
                else:
                    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                i += 1

                if i == 9:
                    break

        image_mean = np.ceil(hsv.mean(axis=(0,1)))
        image_std = np.ceil(hsv.std(axis=(0,1)))

        self.bl = image_mean - image_std * 2
        self.bu = image_mean + image_std * 2





    def filter_objects(self, cnts):

        c = max(cnts, key=cv2.contourArea)

        ((x, y), radius) = cv2.minEnclosingCircle(c)

        if radius > self.min_radius and radius < self.max_radius:

            M = cv2.moments(c)

            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            return ((int(x), int(y)), int(radius), center)

        return ((0, 0), 0, None)





    def track(self, hsv):

        # Construct a mask
        mask = cv2.inRange(hsv, self.bl, self.bu)
        mask = cv2.erode(mask, self.kernel, iterations=1)
        mask = cv2.dilate(mask, self.kernel, iterations=1)

        # Short code for frame
        frame = self.frame

        # Find contours in the mask and initialize the current (x,y) center of ball
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        # Continue only if at least one contour was found
        if len(cnts) > 0 and not self.pause:

            ((x, y), radius, center) = self.filter_objects(cnts)

            # Update the points deque
            if center is not None:
                self.bpts.append([center, self.line, self.buff])

        for p in self.bpts:
            cv2.circle(frame, p[0], p[2], p[1], -1)

        # First flip image... Don't want to have to write backwards ;-)
        frame = cv2.flip(frame, 1)

        return frame





    # Use a thread for speed
    def start_thread(self):

        # Stop flag
        self.halt = 0

        # Initialize thread
        self.t = Thread(target=self.update)

        # Make daemon (dies automatically)
        self.t.daemon = True

        # Start the thread
        self.t.start()




    # Thread worker function
    def update(self):

        while not self.halt:

            # Grab the current web frame
            self.frame = self.camera.read()[1]

        # Release the Camera
        self.camera.release()

        # Destroy all windows
        cv2.destroyAllWindows()





    def capture(self):

        # Wait a moment until we have a frame instance
        cv2.waitKey(500) & 0xFF

        # Loop untill we stop
        while not self.halt:

            # Convert to HSV colorspace
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            # Look for balls
            frame = self.track(hsv)

            # show the frame to our screen
            cv2.imshow("Frame", frame)

            # exit on escape
            k = cv2.waitKey(5) & 0xFF

            if k == 27:
                self.halt = 1
                break

            # Pause (p)
            elif k == 112:
                if self.pause:
                    self.pause = 0
                else:
                    self.pause = 1

            # Clear the screen ( c )
            elif k == 99:
                self.bpts = deque()

            # Colors
            elif k in self.colors:
                self.line = self.colors[k]

            # Draw small ( s )
            elif k == 115:
                self.buff = 5

            # Draw medium ( m )
            elif k == 109:
                self.buff = 10

            # Draw large ( l )
            elif k == 108:
                self.buff = 15


tracker = Follow()
tracker.calibrate();
tracker.start_thread()
tracker.capture()
