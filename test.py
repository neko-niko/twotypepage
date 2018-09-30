import ghostscript
from wand.image import Image
import pdfkit
import os
import random
import pickle
import json

text_lst=os.listdir("./textdir")
text_path_lst=[]
for i in text_lst:
    text_path_lst.append(os.path.join("./textdir",i))
# print(text_path_lst)
img_lst=os.listdir("./handle_img_dir")
img_path_lst=[]
for i in img_lst:
    img_path_lst.append(os.path.join("./handle_img_dir",i))
print(img_lst)
gen_len=[2,3,4]
html_struct=[]

for i in range(50):
    lst=[]
    for i in range(random.choice(gen_len)):
        lst.append(random.choice([2,2,1,1]))    #1代表文本，2代表图片
    html_struct.append(lst)
print(html_struct)
name=1

for jiegou in html_struct:
    page_name = 1           #此文本结构的页数初始化
    text_block_name=1       #此文本结构的文本块数初始化
    img_block_name=1        #此文本结构的图片块数初始化
    body_str=''             #生成html的body的字符串初始化
    print(jiegou[0]==1)
    if jiegou[0]==1:
        global_level=108     #如果此pdf的第一个块为文本块，定义初始全局高度为108
    elif jiegou[0]==2:
        global_level=114    #如果此pdf的第一个块为图像块，则定义初始全局高度为114
    else:
        raise Exception("初始化文本结构时错误")
    pickle_dict = {}
    for i in range(len(jiegou)):
        if jiegou[i]==1:        #当块为文本时的初始化部分
            if i==0:            #如果此块为第一个块，则初始化块的起始高度为定义的全局高度
                text_block_start_level=global_level
            elif jiegou[i-1]==1:      #如果此块不是第一个块并且上一个块为文本块，则起始高度为之前处理过后的全局高度+20
                global_level+=25
                text_block_start_level=global_level
            else:                   #如果此块不是第一个块且上一个块为图像块，则起始高度为之前处理过得全局高度+122
                global_level+=130
                text_block_start_level=global_level
            text_block_level=0      #此块的总高度初始化为0
            with open(random.choice(text_path_lst),'r',encoding='utf-8') as txt:
                total_str=txt.read()
            txt_len = (len(total_str)//60)+1      #每60个字符串一行 计算总行数

            for j in range(txt_len):
                if j==txt_len-1:            #如果此行为此文本块的最后一行 则做特殊处理
                    global_level += 80
                    text_block_level += 80
                else:
                    global_level += 102       #如果此行为此文本块的非最后一行，则全局高度和此块高度+100
                    text_block_level += 102
                    print("+100")
                if global_level>=3352:      #如果在此过程中，总高度超出一页高度
                    text_str='text%s' % (text_block_name)
                    if page_name==1:
                        pickle_dict[str(text_str+'_1')]=(520,int(text_block_start_level))
                        pickle_dict[str(text_str+'_2')]=(1980,int(text_block_start_level))
                        pickle_dict[str(text_str+'_3')]=(520,int(text_block_start_level+text_block_level))
                        pickle_dict[str(text_str+'_4')]=(1980,int(text_block_start_level+text_block_level))
                    print("第%s页的文本块%s的水平距离从%s到%s()" % (page_name,text_block_name,text_block_start_level,text_block_start_level+text_block_level))  #保存第一页的数据信息
                    print("第%s页的文本块%s的垂直距离从%s到%s()" % (page_name,text_block_name,590,1570))
                    if page_name==1:
                        with open('./pickledir/%s.pickle' % (name),'wb') as pic:
                            pickle.dump(pickle_dict,pic)
                    page_name+=1        #页数+1
                    text_block_name=1       #文本块计数归1
                    img_block_name=1        #图像块计数归1
                    text_block_level=80    #块的高度置为此行在下一页的高度100
                    global_level=108         #总高度置位在下一页中的起始高度加此行的作用即为108
                    text_block_start_level=global_level
                body_str += '''<h3 align="center">{text}</h3>'''.format(text=total_str[j * 60:(j + 1) * 60])
            if page_name==1:
                text_str = 'text%s' % (text_block_name)
                pickle_dict[str(text_str + '_1')] = (520, int(text_block_start_level))
                pickle_dict[str(text_str + '_2')] = (1920, int(text_block_start_level))
                pickle_dict[str(text_str + '_3')] = (520, int(text_block_start_level + text_block_level))
                pickle_dict[str(text_str + '_4')] = (1920, int(text_block_start_level + text_block_level))
            print("第%s页的文本块%s的水平距离从%s到%s" % (page_name,text_block_name,text_block_start_level,text_block_start_level+text_block_level))
            print("第%s页的文本块%s的垂直距离从%s到%s" % (page_name, text_block_name, 520, 1570))
            text_block_name+=1

        if jiegou[i]==2:
            img=random.choice(img_lst)
            width=int(str(img).split('.')[0].split('_')[0])*2.5
            height=int(str(img).split('.')[0].split('_')[1].split('$')[0])*2.5
            # 当块为图像块时的初始化
            if i==0:             #如果此块为第一个块，则初始化块的起始高度为定义的全局高度
                img_block_start_level=global_level
            elif jiegou[i-1]==1:    #如果此块不是第一个块并且上一个块为文本块，则起始高度为总高+40
                global_level+=32
                img_block_start_level=global_level
            else:    #如果此块不是第一个块并且上一个块为图像块，则起始高度为总高+140
                global_level+=135
                img_block_start_level=global_level
            if height+global_level>=3352:       #如果当前总高度+图片高度大于一定范围
                page_name+=1    #页数+1
                text_block_name=1   #文本块计数置1
                img_block_name=1    #图像块计数置1
                global_level=114    #初始高度置114（下一张图片的第一个块必定为图像块）
                img_block_start_level=114   #图像块的起始位置置114
            img_path="../handle_img_dir/{img_}".format(img_=img)
            body_str+='''<p align="center"><img src="{path_}"/></p><br>'''.format(path_=img_path)
            img_str='img'+str(img_block_name)
            pickle_dict[img_str+'_1']=(int(1240-(((width)/2)+6)),int(img_block_start_level))
            pickle_dict[img_str+'_2']=(int(1240+(((width)/2)+6)),int(img_block_start_level))
            pickle_dict[img_str+'_3']=(int(1240-(((width)/2)+6)),int(img_block_start_level+height+8))
            pickle_dict[img_str+'_4']=(int(1240+(((width)/2)+6)),int(img_block_start_level+height+8))
            print("第%s页的图像块%s的水平距离从%s到%s" % (page_name,img_block_name,img_block_start_level,img_block_start_level+height+8))
            print("第%s页的图像块%s的垂直距离从%s到%s" % (page_name,img_block_name,1240-(((width)/2)+6),1240+(((width)/2)+6)))
            global_level=height+8+global_level
            img_block_name+=1

    if page_name==1:
        with open('./pickledir/%s.pickle' % (name), 'wb') as pic:
            pickle.dump(pickle_dict, pic)
        with open('./jsondir/%s.json' % (name), 'w') as js:
            json.dump(pickle_dict,js)

    html_str='''<!DOCTYPE html>
 <html lang="en">
<head>
     <meta charset="UTF-8">
     <title></title>
 </head>
 <body>
 {body_str}
 </body>
 </html>'''.format(body_str=body_str)
    html_output_path="./htmldir//%s.html" % name
    with open(html_output_path,'w',encoding='utf-8') as html:
        html.write(html_str)
    pdf_path="./pdfdir//%s.pdf" % name
    pdfkit.from_file(html_output_path,pdf_path)

    pdf=Image(filename=pdf_path,resolution=300)
    jpg=pdf.convert("jpg")
    req_image=[]
    for img in jpg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpg'))
    jpg_name=0
    for img in req_image:
        with open("./jpgdir//%s_%s.jpg" %(name,jpg_name),'wb') as ff:
            ff.write(img)
        jpg_name+=1
    name+=1
    jpg_path=[os.path.join('./jpgdir',i) for i in os.listdir('./jpgdir')]
    for img_ in jpg_path:
        if '_0' not in str(img_):
            os.remove(img_)


# 放大倍数2.5
# 水平起始位置118
# <h3>型标签字符垂直起始位置370
# <h3>型标签字符垂直结束位置2100
# <h3>型标签字符行间距60
# <h3>型标签字符一行宽度约为100
# <h3>型标签字符起始位置与实际起始位置间隔4
# 两图片间间隔为144
# 图片文字间间隔为152鉴于<h3>型字符与实际位置与起始位置之间的间隔，建议定义为148
# 水平结束位置3348，由于同上原因，建议定义为3352


# for path in text_path_lst:
#     with open(path,'r',encoding='utf-8') as txt:
#         total_str=txt.read()
#     length=(len(total_str)//60)+1
#     synthesis_str = ''
#     for i in range(length):
#         cache_str='''<h3 align="center">{text}</h3>'''.format(text=total_str[i*60:(i+1)*60])    #一段html文档
#         synthesis_str+=cache_str        #将多段html文档合成
#     html_str='''<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title></title>
# </head>
# <body>
# {body_str}
# </body>
# </html>'''.format(body_str=synthesis_str)
#
#
#     html_output_path="./htmldir//%s.html" % name
#     with open(html_output_path,'w',encoding='utf-8') as html:
#         html.write(html_str)
#     pdf_path="./pdfdir//%s.pdf" % name
#     pdfkit.from_file(html_output_path,pdf_path)
#
#     pdf=Image(filename=pdf_path,resolution=300)
#     jpg=pdf.convert("jpg")
#     req_image=[]
#     for img in jpg.sequence:
#         img_page = Image(image=img)
#         req_image.append(img_page.make_blob('jpg'))
#     jpg_name=0
#     for img in req_image:
#         with open("./jpgdir//%s_%s.jpg" %(name,jpg_name),'wb') as ff:
#             ff.write(img)
#         jpg_name+=1
#     name+=1

# 放大倍数2.5
# 水平起始位置118
# <h3>型标签字符垂直起始位置370
# <h3>型标签字符垂直结束位置2100
# <h3>型标签字符行间距60
# <h3>型标签字符一行宽度约为100
# <h3>型标签字符起始位置与实际起始位置间隔4
# 两图片间间隔为144
# 图片文字间间隔为152鉴于<h3>型字符与实际位置与起始位置之间的间隔，建议定义为148
# 水平结束位置3348，由于同上原因，建议定义为3352
