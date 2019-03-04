import cv2
import os,sys

save_dir=sys.argv[1]
if os.path.isdir(save_dir):
    pass
else:
    os.mkdir(save_dir)
count=0
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS,30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
while(True):
    ret, frame = cap.read()
    cv2.imshow("capture", frame)
    if cv2.waitKey(1)  & 0xFF == ord('s'):
        cv2.imwrite(save_dir+str(count)+'.jpg', frame)
        count+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 
