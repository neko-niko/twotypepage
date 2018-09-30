from PIL import Image
import os
import time
import hashlib
md5=hashlib.md5()
img_lst=os.listdir("./val2017")
img_path_lst=[]
for i in img_lst:
    img_path_lst.append(os.path.join("./val2017",i))

size_lst=[]
for i in img_path_lst:
    img=Image.open(i)
    # print("图片宽高为："+str(img.size))
    size_tuple=img.size
    if size_tuple not in size_lst:
        size_lst.append(size_tuple)
        img.save("./handle_img_dir/%s_%s.jpg" % (size_tuple[0],size_tuple[1]))
    else:
        now_time=str(time.time())
        md5.update(now_time.encode("utf-8"))
        img.save("./handle_img_dir/%s_%s$%s.jpg"% (size_tuple[0],size_tuple[1],md5.hexdigest()))
# print(len(os.listdir("./handle_img_dir")))
