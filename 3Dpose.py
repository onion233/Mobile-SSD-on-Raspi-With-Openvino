import cv2
import numpy as np 


import cv2

image = cv2.imread("./tools/data/0.jpg")



# cv2.imshow("Updated",image)

# cv2.waitKey(0)

test=np.zeros((1,3))
test[0]=[105,148.5,85]

objPoints=np.zeros((4,3))
objPoints[1]=[0,297,0]
objPoints[2]=[210,297,0]
objPoints[3]=[210,0,0]

imgPoints=np.zeros((4,2))
imgPoints[0]=[192,452]
imgPoints[1]=[214,38]
imgPoints[2]=[498,40]
imgPoints[3]=[494,464]

K=np.array([[314.1683654526395, 0, 377.1910435804826],[0, 314.3193854359332, 246.7049571605152],[0.000000,0.000000,1.000000]])
dist_coef=np.array([0.0112630109045513, -0.02437659818486941, 0.001105362347212322, 0.0009976530588027106, 0])
retval, rvec, tvec = cv2.solvePnP(objPoints,imgPoints.reshape((4,1,2)),K, dist_coef,flags=cv2.SOLVEPNP_P3P)

print(rvec)
print(tvec)
a=np.zeros((1,3))
impoints=cv2.projectPoints(objPoints, rvec, tvec, K, dist_coef) 
print(impoints[0].reshape(-1,2))
print(cv2.projectPoints(test, rvec, tvec, K, dist_coef)[0] )
# rmat, j = cv2.Rodrigues(rvec)

# #convert back to homgeneous coordinates
# pnp_tvec = np.zeros(4)
# pnp_tvec[3] = 1
# pnp_rmat = np.eye(4)
# pnp_tvec[:3] = tvec[:,0]
# pnp_rmat[:3,:3] = rmat
