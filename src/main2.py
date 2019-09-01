import sys
import numpy as np
import cv2

def check_grayscale(img:np.ndarray):
  return (img[:,:,0] == img[:,:,1]).all() and (img[:,:,0] == img[:,:,2]).all()

def color_range(img:np.ndarray, color:np.ndarray, gray=False):
  img_float = np.float64(img)

  if not gray:
    # Calculates euclidean distance and generates boolean matrix
    # that selects pixels within 13 color units from color
    cond = img_float[:,:,:] - color
    cond = cond[:,:,0]**2 + cond[:,:,1]**2 + cond[:,:,2]**2
    cond = cond < 169
  else:
    # Calculates difference and generates boolean matrix
    # that selects pixels within 13 brightness levels
    cond = np.abs(img_float[:,:,0].squeeze() - color)
    cond = cond < 13

  # Modify a copy
  img_copy = img.copy()
  img_copy[cond] = (0,0,255)
  return img_copy

# Treats all mouse events
def mouse_callback(event, x, y, flags, params):
  global img, is_grayscale, show

  if event == cv2.EVENT_LBUTTONDOWN:
    if is_grayscale:
      print("({}, {}) {}".format(y, x, img[y,x,0]) )
      show = color_range(img, img[y,x,0], gray=True)
    else:
      print("({}, {}) {}".format(y, x, img[y,x,:]) )
      show = color_range(img, img[y,x,:], gray=False)

if __name__ == "__main__":
  # Test for image path argument
  if len(sys.argv) < 2:
    print("Please provide a path to a JPEG image file.")
    exit(1)

  # Load image
  img = cv2.imread(sys.argv[1])
  is_grayscale = check_grayscale(img)

  # Setup to listen for mouse events
  cv2.namedWindow("Image")
  cv2.setMouseCallback("Image", mouse_callback)

  # Shows a copy to retain the original
  show = img.copy()
  stop = False
  while not stop:
    # Show it to the user
    cv2.imshow("Image", show)
    # Test if clicked any key to exit
    if cv2.waitKey(5) != -1:
      stop = True

  cv2.destroyAllWindows()
