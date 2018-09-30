import pickle
import os
import json

# with open('./pickledir//10.pickle','rb') as p:
#     print(pickle.load(p))
#
# os.remove('C:\\Users\patchouli\AppData\Local\Temp\magick-3560Jkm711aLEl_Z')
# with open('./jsondir/2.json','r') as fp:
#     js=json.load(fp)
#     print(js)


# [os.remove(i) for i in  [os.path.join('./htmldir',j) for j in os.listdir('./htmldir')]]
# [os.remove(i) for i in  [os.path.join('./jpgdir',j) for j in os.listdir('./jpgdir')]]
# [os.remove(i) for i in  [os.path.join('./pickledir',j) for j in os.listdir('./pickledir')]]
# [os.remove(i) for i in  [os.path.join('./pdfdir',j) for j in os.listdir('./pdfdir')]]
# [os.remove(i) for i in  [os.path.join('./jsondir',j) for j in os.listdir('./jsondir')]]
# [os.remove(i) for i in  [os.path.join('./cvjpg',j) for j in os.listdir('./cvjpg')]]
#

import pdfkit
pdfkit.from_url('https://www.kesci.com/home/project/5ba0757c1e126e003c82b906','./kesai/test.pdf')