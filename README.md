# Webcam Painting
This is a simple project with Opencv Python to track an object and draw its path on the screen. The project was developed primarily as a display for various engineering recruiting events targeting middle school and high school students. It provides a good demo to start talking about machine vision, object tracking, and even a little remote sensing.

The program uses threading to improve processing speed; I have successfully run it on a mid level laptop with no lag. **However**, you cannot continuously draw on the screen. Eventually the rendering will start to lag. Clearing the current drawing will result in a few seconds of high speed frame display as the queued frames are rendered. This can be somewhat humorous.

### Use
To run the program you need to have compiled opencv 3.2 for python 2.7. I suggest [pyimagesearch](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/) for a guide to comile opencv from source. If you want to develop your own tracker, you can find a good tutorial on that site. The painting code should run in python3 after you edit the code some, i.e. '''python from queue import Queue''' instead of '''python from Queue import Queue'''. Once all this is taken care of, CD into the folder and run paint.py from the terminal.

Once you run the code, you should see a red square in the upper left hand corner of the screen. Center what you want to track over the square and press "c" on your keyboard. The red square should now move to to the left hand center of the screen. Again center what you want to track over the square and press "c". Continue this seven more times to capture any color differences due to light variability in front of your camera. Once calibration is finished, the program estimates a minimum and maximum hsv color range to look for and will immediately start tracking and drawing your objects path. ***I have found that a bright led works best; it limits the effect of shadows and provides a narrow color range..*** I'm using a pen with a white LED. Holding the pen vertically with your finger pressed against the LED helps keep a consistant appearence on the webcam.

I'm using a circle drawn at the centroid of the tracked object to visualize the path. This has pros and cons, namely that if you move to fast you get polka dots not a smooth line. However, I thought that overall it looked more natural, so long as you move slowly and smoothly.

### Commands
Whats a webcam painting program without some easy ways to change colors or line sizes? The program listens for several specific keyboard inputs which are:

#### Colors
r => changes color to red

b => changes color to blue

g => changes color to green

y => changes color to yellow

o => changes color to orange

k => changes color to black

w => changes color to white

#### Line sizes
s => changes size to 5 pixels

m => changes size to 10 pixels

l => changes size to 15 pixels

#### Other features
c => clears all drawings on the screen

p => pauses drawing

esc => exits the program
