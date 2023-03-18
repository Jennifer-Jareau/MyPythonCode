# gif动图制作
import imageio, os
paths=['path1/','path2/']
for path in paths:
    images = []
    files = os.listdir(path)
    for i in range(len(files)):
        images.append(imageio.imread(path+files[i]))
    imageio.mimsave(path+'out.gif',images,'GIF',duration=0.5)
    
    
# 拼接
import os
from PIL import Image
paths=['path1/','path2/']
for path in paths:
    images = []
    files = os.listdir(path)
    files.sort(key=lambda x:int(x[0:5]))              #以文件名前5个字从小到大排列，不能含有空格
    imgarray=np.array(Image.open(path+files[0]))
    for i in range(1,len(files)):
        imgarray0=np.array(Image.open(path+files[i]))
        imgarray=np.concatenate((imgarray,imgarray0),axis=0)   #axis=0为纵向排列，axis=1为横向排列
        img=Image.fromarray(imgarray)
    img_=img.convert('RGB')
    img_.save(path+'out.jpg')     # jpg不含alpha信息，须从RGBA格式转化成RGB格式
