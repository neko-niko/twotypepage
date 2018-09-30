import cv2 as cv
import json
import os

json_lst = os.listdir('./jsondir')
print(json_lst)
for i in json_lst:
    with open(os.path.join('./jsondir',i),'r') as js:
        point_dict = json.load(js)
    point_lst = point_dict.values()
    lable=str(i).split('.')[0]
    img = cv.imread('./jpgdir/%s_0.jpg' % lable)
    for j in range(1,int(len(point_lst)/4+1)):
        cv.rectangle(img,tuple(list(point_lst)[j*4-4]),tuple(list(point_lst)[j*4-1]),(0,0,255),1,4,0)
    cv.imwrite('./cvjpg/%s_0.jpg' % lable,img)


# with open('./jsondir/5.json','r') as js:
#     ponit_dict = json.load(js)
#
# print(type(ponit_dict))
# ponit_list = ponit_dict.values()
# img = cv.imread('./jpgdir/5_0.jpg')
# for i in range(1,int((len(ponit_list)/4)+1)):
#     cv.rectangle(img,tuple(list(ponit_list)[i*4-4]),tuple(list(ponit_list)[i*4-1]),(0,0,255),1,4,0)
    # print(tuple(list(ponit_list)[i*4-4]))
# cv.namedWindow('image')
# cv.rectangle(img,(434,114),(2046,1182),(0,0,255),1,4,0)

# cv.imshow('image',img)
# cv.waitKey(0)
# cv.imwrite('./cvjpg/2_0.jpg',img)
# cv.destroyAllWindow()