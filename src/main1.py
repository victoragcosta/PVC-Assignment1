import sys
import numpy as np
import cv2

# Treats all mouse events
def mouse_callback(event, x, y, flags, params):
  global img, is_grayscale
  if event == cv2.EVENT_LBUTTONDOWN:
    if is_grayscale:
      print("({}, {}) {}".format(y, x, img[y,x,0]) )
    else:
      print("({}, {}) {}".format(y, x, img[y,x,:]) )

def check_grayscale(img:np.ndarray):
  return (img[:,:,0] == img[:,:,1]).all() and (img[:,:,0] == img[:,:,2]).all()

if __name__ == "__main__":
  # Test for image path argument
  if len(sys.argv) < 2:
    print("Please provide a path to a JPEG image file.")
    exit(1)

  # Load image
  img = cv2.imread(sys.argv[1])
  is_grayscale = check_grayscale(img)

  # Show it to the user
  cv2.imshow("Image", img)
  # Setup to listen for mouse events
  cv2.setMouseCallback("Image", mouse_callback)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
