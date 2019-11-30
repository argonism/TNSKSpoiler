import cv2
import numpy as np
 
#画像の読み込み
I1 = cv2.imread('testimg/out1.png', cv2.IMREAD_GRAYSCALE)
I2 = cv2.imread('testimg/out2.png', cv2.IMREAD_GRAYSCALE)
I3 = cv2.imread('testimg/out3.png', cv2.IMREAD_GRAYSCALE)
 
 
#絶対値の求めたのち、背景差分を求める
img_diff1 = cv2.absdiff(I2,I1)
img_diff2 = cv2.absdiff(I3,I2)

cv2.imshow("img_diff1",img_diff1)
cv2.waitKey(0)
cv2.imshow("img_diff2",img_diff2)
cv2.waitKey(0)
cv2.imshow("img_diff1 - img_diff2",cv2.absdiff(img_diff1, img_diff2))
cv2.waitKey(0)

print("2  :", np.linalg.norm(img_diff1))
print("2  :", np.linalg.norm(img_diff2))
print("2  :", np.linalg.norm(cv2.absdiff(img_diff1, img_diff2)))

 
 
#論理積を算出するには、bitwise_and()関数
Im = cv2.bitwise_and(img_diff1, img_diff2)
 
 
#二値化処理
img_th = cv2.threshold(Im, 10, 255,cv2.THRESH_BINARY)[1]
 
#膨張処理・収縮処理を施してマスク画像を生成
operator = np.ones((3,3), np.uint8)
img_dilate = cv2.dilate(img_th, operator, iterations=4)
img_mask = cv2.erode(img_dilate,operator,iterations=4)
 
#マスク画像を使って対象を切り出す
img_dst = cv2.bitwise_and(I3, img_mask)
 
#表示
cv2.imshow("Show BACKGROUND SUBSTRACTION image",img_dst)
cv2.waitKey(0)
cv2.destroyAllWindows()