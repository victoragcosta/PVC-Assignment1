import sys
import cv2
import numpy as np

if len(sys.argv) < 2:
  exit(1)

cap = cv2.VideoCapture(sys.argv[1])
out_name = '.'.join(sys.argv[1].split('.')[:-1])+'.avi'

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(out_name,fourcc, 20.0, (1920,1080))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
