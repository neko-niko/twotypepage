import ghostscript
import json
import random
import os
import pdfkit
from wand.image import Image

class GeneratePage(object):     #实现了包含两种类别图片的框选
    def __init__(self):
        self.text_lst = os.listdir('./textdir')
        self.img_lst = os.listdir('./handle_img_dir')
        self.table_lst = os.listdir('./tbdir')
        self.title_lst  = os.listdir('./titledir')
        self.lth = [2,3,4]
        self.name = 0
    def generate_html(self):
        self.name += 1
        html_strcut = []
        html_strcut.append(10)
        keys_lst = []       #表示为文本（1）或图片（2）
        values_lst = []     #表示文本或图片的具体路径
        # html_lst
        total_len = random.choice(self.lth)
        for _ in range(total_len):
            html_strcut.append(random.choice([1,2,2,3]))
        body_str = ''
        for i in html_strcut:
            if i == 10:         #如果为主标题
                keys_lst.append(i)
                title_path = os.path.join('./titledir',random.choice(self.title_lst))
                values_lst.append(title_path)
                with open(title_path,'r',encoding='utf-8') as title:
                    title = title.read()
                body_str += '''<h1 align="center">{main_title}</h1>'''.format(main_title = title)
            if i == 1:
                keys_lst.append(i)
                text_path = os.path.join('./textdir',random.choice(self.text_lst))
                values_lst.append(text_path)
                with open(text_path,'r',encoding='utf-8') as text:      #如果为1，随机读取一个文本
                    total_text = text.read()
                text_len = int((len(total_text)/60) + 1)         #计算行数
                for line_num in range(text_len):
                    body_str +=  '''<h3 align="center">{text}</h3>'''.format(text = total_text[60*line_num:60*(line_num+1)])
            if i == 2:
                keys_lst.append(2)
                lable = random.choice([1,2])        #随机选取图片或表格
                if lable == 1:
                    img = random.choice(self.img_lst)
                    values_lst.append("./handle_img_dir\\{img_}".format(img_ = img))
                    img_path = "../handle_img_dir/{img_}".format(img_ = img)
                    body_str += '''<p align="center"><img src="{path_}"/></p><br>'''.format(path_=img_path)
                else:
                    img = random.choice(self.table_lst)
                    values_lst.append("./tbdir\\{img_}".format(img_ = img))
                    img_path = "../tbdir/{img_}".format(img_ = img)
                    body_str += '''<p align="center"><img src="{path_}"/></p><br>'''.format(path_=img_path)
            if i == 3:
                keys_lst.append(3)
                text_path = os.path.join('./textdir', random.choice(self.text_lst))
                values_lst.append(text_path)
                lt_path = os.path.join('./titledir',random.choice(self.title_lst))
                with open(lt_path,'r',encoding='utf-8') as title:
                    title = title.read()
                body_str += '''<h3 align="center">{little_title}</h3>'''.format(little_title = title)
                with open(text_path,'r',encoding='utf-8') as text:
                    total_text = text.read()
                text_len = int((len(total_text)/60) + 1)         #计算行数
                for line_num in range(text_len):
                    body_str +=  '''<h3 align="center">{text}</h3>'''.format(text = total_text[60*line_num:60*(line_num+1)])
        html_str = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title></title> </head><body>{body_str}</body></html>'''.format(body_str=body_str)
        with open('./htmldir/%s.html' % self.name,'w',encoding='utf-8') as html:
            html.write(html_str)
        return keys_lst,values_lst,'./htmldir/%s.html' % self.name

    def generate_pdf(self,html_path):
        pdf_path = './pdfdir/%s.pdf' % self.name
        pdfkit.from_file(html_path,pdf_path)
        return pdf_path

    def generate_png(self,pdf_path):
        img_name = 1
        pdf = Image(filename=pdf_path,resolution=300)
        png = pdf.convert("png")
        rep_image = []
        for img in png.sequence:
            img_page = Image(img)
            rep_image.append(img_page.make_blob('png'))

        for img in rep_image:
            with open('./jpgdir/%s_%s.png' % (self.name,img_name),'wb') as ff:
                ff.write(img)
            img_name += 1

    def cal_block_size(self,struct,file_path):
        if len(struct) != len(file_path):           #判断基本结构是否匹配
            raise Exception("信息结构与指定文件长度不匹配")
        else:
            block_len = len(struct)
            for i in range(block_len):
                print(file_path[i].split('\\')[0].split('/')[-1])
                if (struct[i] == 1 and 'text' not in file_path[i].split('\\')[0].split('/')[-1]) or \
                        (struct[i] == 2 and ('img' not in file_path[i].split('\\')[0].split('/')[-1] and 'tb' not in file_path[i].split('\\')[0].split('/')[-1])) or\
                        (struct[i] == 10 and 'title' not in file_path[i].split('\\')[0].split('/')[-1]):
                    raise Exception("指定的类型与指定的文件不匹配")
        block_dict = {}
        page_cot = 1
        text_block_cot = 1
        img_block_cot = 1
        tb_block_cot = 1
        lt_block_cot = 1
        if struct[0] != 10:
            if struct[0] == 1 or struct[0] == 3:      #如果第一个块为文本块
                global_level = 108  #定义全局高度为108
            elif struct[0] == 2:    #如果第一个块为图像块
                global_level = 114  #定义全局高度为114
            else:
                raise Exception('初始化全局高度时错误，请检查您输入的结构信息是否符合规定')
        else:
            print('此块有主标题')
            del struct[0]
            del file_path[0]
            block_dict['maintitle_1'] = (700,128)
            block_dict['maintitle_2'] = (1778,128)
            block_dict['maintitle_3'] = (700,212)
            block_dict['maintitle_4'] = (1778,212)
            if struct[0] == 1 or struct[0] == 3:
                global_level = 252
            elif struct[0] == 2:
                global_level = 259
            else:
                raise Exception('初始化全局高度时错误，请检查您输入的结构信息是否符合规定')
            # if struct[0] == 1:
            #     global_level =
        for block in range(len(struct)):
            if struct[block] == 1:  #如果此块为文本块
                if block == 0:      #如果此块为第一个块
                    text_block_start_level = global_level
                elif struct[block-1] == 1 or struct[block-1] == 3:  #如果上一块为文本块
                    global_level += 25      #整体高度+25
                    text_block_start_level = global_level
                else:                       #如果上一块为图像块
                    global_level += 130     #整体高度+130
                    text_block_start_level = global_level
                # text_block_level = 0
                # with open(file_path,'r',encoding='utf-8') as text:
                #     total_text = text.read()
                # text_len = (len(total_text)/60) + 1     #每行字为60，计算总行数
                # for line in range(text_len):
                #     if line == text_len - 1:        #若此行为最后一行。特殊处理

                global_level,page_cot,text_block_cot,img_block_cot,block_dict = \
                self.cal_text(file_path[block],global_level,page_cot,text_block_start_level,text_block_cot,img_block_cot,block_dict)
                if page_cot != 1:
                    print('页码超过1，跳出')
                    break
                else:
                    continue
            elif struct[block] == 2:      #如果此块为图像块
                img = file_path[block]
                lable = str(img).split('\\')[0]
                print('lable为：'+lable)
                width = int(str(img).split('\\')[-1].split('.')[0].split('_')[0]) * 2.5
                height = int(str(img).split('\\')[-1].split('.')[0].split('_')[1].split('$')[0]) * 2.5
                if block == 0:
                    img_block_start_level = global_level
                elif struct[block-1] == 1 or struct[block-1] == 3:
                    global_level += 32
                    img_block_start_level = global_level
                else:
                    global_level += 135
                    img_block_start_level = global_level

                if height + global_level > 3400:            #如果图像高度+原高度之和大于3352，则保存数据到本地，并跳出
                    with open('./jsondir/%s.json' % self.name,'w') as js:
                        json.dump(block_dict,js)
                    break
                else:
                    if 'img' in lable:
                        block_name = 'img' + str(img_block_cot)
                        block_dict[block_name+'_1']=(int(1240-(((width)/2)+6)),int(img_block_start_level))
                        block_dict[block_name+'_2']=(int(1240+(((width)/2)+6)),int(img_block_start_level))
                        block_dict[block_name+'_3']=(int(1240-(((width)/2)+6)),int(img_block_start_level+height+8))
                        block_dict[block_name+'_4']=(int(1240+(((width)/2)+6)),int(img_block_start_level+height+8))
                        global_level = height + 8 + global_level
                        img_block_cot += 1
                    else:
                        block_name = 'table' + str(tb_block_cot)
                        block_dict[block_name+'_1']=(int(1240-(((width)/2)+6)),int(img_block_start_level))
                        block_dict[block_name+'_2']=(int(1240+(((width)/2)+6)),int(img_block_start_level))
                        block_dict[block_name+'_3']=(int(1240-(((width)/2)+6)),int(img_block_start_level+height+8))
                        block_dict[block_name+'_4']=(int(1240+(((width)/2)+6)),int(img_block_start_level+height+8))
                        global_level = height + 8 + global_level
                        tb_block_cot += 1
            elif struct[block] == 3:
                global_level += 102
                if block == 0:  # 如果此块为第一个块
                    # text_block_start_level = global_level
                    pass
                elif struct[block - 1] == 1 or struct[block - 1] == 3:  # 如果上一块为文本块
                    global_level += 25  # 整体高度+25
                    # text_block_start_level = global_level
                else:  # 如果上一块为图像块
                    global_level += 130  # 整体高度+130
                    # text_block_start_level = global_level
                text_block_start_level = global_level
                block_name = 'lt' + str(lt_block_cot)
                block_dict[block_name+'_1'] = (830,int(global_level-102))
                block_dict[block_name+'_2'] = (1648,int(global_level-102))
                block_dict[block_name+'_3'] = (830,int(global_level-4))
                block_dict[block_name+'_4'] = (1648,int(global_level-4))
                lt_block_cot += 1
                global_level, page_cot, text_block_cot, img_block_cot, block_dict = \
                    self.cal_text(file_path[block], global_level, page_cot, text_block_start_level, text_block_cot,
                                  img_block_cot, block_dict)
                if page_cot != 1:
                    print('页码超过1，跳出')
                    break
                else:
                    continue
        if page_cot == 1:       #如果将当前的所有块都添加后，总页数依然为1，则保存数据到本地
            with open('./jsondir/%s.json' % self.name,'w') as js:
                json.dump(block_dict,js)
        # else:
        #     page_cot = 1
        #     text_block_cot = 1
        #     img_block_cot = 1
        #     tb_block_cot = 1
        #     block_dict = {}
        #     block_dict['maintitle_1'] = (700,128)
        #     block_dict['maintitle_2'] = (1778,128)
        #     block_dict['maintitle_3'] = (700,200)
        #     block_dict['maintitle_4'] = (1778,200)

    def cal_text(self,path,global_level,page_cot,text_block_start_level,text_block_cot,img_block_cot,block_dict):
        '''文本路径，全局高度，页码，文本块起始高度，文本块计数，图像块计数，块字典'''
        text_block_level = 0
        with open(path, 'r', encoding='utf-8') as text:
            total_text = text.read()
        text_len = (len(total_text) // 60) + 1  # 每行字为60，计算总行数
        for line in range(text_len):
            if line == text_len - 1:  # 若此行为最后一行。特殊处理
                global_level += 80
                text_block_level += 80
            else:
                global_level += 102
                text_block_level += 102
            if global_level > 3352:     #如果在此过程中，总高度大于某一值
                block_name = 'text%s'  % text_block_cot
                if page_cot == 1:       #如果此时页码为1，块字典中写入此块的信息
                    block_dict[str(block_name + '_1')] = (520, int(text_block_start_level))
                    block_dict[str(block_name + '_2')] = (1980, int(text_block_start_level))
                    block_dict[str(block_name + '_3')] = (520, int(text_block_start_level + text_block_level))
                    block_dict[str(block_name + '_4')] = (1980, int(text_block_start_level + text_block_level))
                    with open('./jsondir/%s.json' % (self.name),'w') as js:
                        json.dump(block_dict,js)
                page_cot += 1
                text_block_cot = 1
                img_block_cot = 1
                text_block_level = 80
                global_level = 188
                text_block_start_level = global_level - 80
        else:
            if page_cot == 1:
                block_name = 'text%s' % text_block_cot
                block_dict[str(block_name + '_1')] = (520, int(text_block_start_level))
                block_dict[str(block_name + '_2')] = (1980, int(text_block_start_level))
                block_dict[str(block_name + '_3')] = (520, int(text_block_start_level + text_block_level))
                block_dict[str(block_name + '_4')] = (1980, int(text_block_start_level + text_block_level))
                text_block_cot += 1
        return global_level,page_cot,text_block_cot,img_block_cot,block_dict





if __name__=='__main__':
    caozuo = GeneratePage()
    for _ in range(10):
        keys,values,html_path = caozuo.generate_html()
        caozuo.cal_block_size(struct=keys,file_path=values)
        print(keys,values)
        pdf_path = caozuo.generate_pdf(html_path)
        caozuo.generate_png(pdf_path)
        # caozuo.cal_block_size(keys,values)
