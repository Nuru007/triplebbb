import sys
try:
    import cv2
    print("cv2 version:", cv2.__version__)
except ImportError:
    print("cv2 is not installed")
