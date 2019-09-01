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

    cond = np.sum(cond**2, axis=2) # Demora 48 segundos para o vídeo todo

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
  global img, has_selected, color

  if event == cv2.EVENT_RBUTTONDOWN:
    has_selected = False

  if event == cv2.EVENT_LBUTTONDOWN:
    color = img[y,x,:]
    has_selected = True
    print("({}, {}) {}".format(y, x, color) )

if __name__ == "__main__":
  # Test for image path argument
  if len(sys.argv) < 2:
    print("Please provide a path to a AVI or x264 video file.")
    exit(1)

  has_selected = False
  color = None

  # Load video
  vid = cv2.VideoCapture(sys.argv[1])

  # Setup to listen for mouse events
  cv2.namedWindow("Video")
  cv2.setMouseCallback("Video", mouse_callback)

  # Shows a copy to retain the original
  stop = False
  while not stop and vid.isOpened():
    ret, img = vid.read()

    if ret:
      if has_selected:
        show = color_range(img, color)
      else:
        show = img
      # Show it to the user
      cv2.imshow("Video", show)
    else:
      stop = True

    # Test if clicked any key to exit
    if cv2.waitKey(1) != -1:
      stop = True

  vid.release()
  cv2.destroyAllWindows()
