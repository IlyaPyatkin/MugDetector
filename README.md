# MugDetector
This is a project based on OpenCV to detect and localize the blue mug in mug.ogv video.
Recognition is done by color masking and finding the biggest contour of sufficient size.
To start realtime video mug detection run detection.py.

The server functionality allows to upload a video and using such recognition to identify moments when 
the mug enters or leaves the view, which are then shown as a labeled sequence of images. 
The server is run using Flask. To start it run server.py.

Allowed file extensions are: ogv, mp4, avi.
