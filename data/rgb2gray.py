import cv2
import os

def read_path(file_pathname):
    #遍历该目录下的所有图片文件
    for filename in os.listdir(file_pathname):
        print(filename)
        img = cv2.imread(file_pathname+'/'+filename)
        ####change to gray
      #（下面第一行是将RGB转成单通道灰度图，第二步是将单通道灰度图转成3通道灰度图）
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        image_np=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        #####save figure
        cv2.imwrite('./test_images'+"/"+filename,image_np)       


#读取的目录
read_path("./test_images1")
#print(os.getcwd())
