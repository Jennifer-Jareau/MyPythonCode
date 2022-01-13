# 此为某一时次、某一站点的；雷达数据读取
all=[366,367,367,367,372,372,372,369,365,363,361]
bll=np.zeros(12)
for i in range(12):
    bll[i]=np.sum(all[0:i])           # all是每个仰角所含径向的条数，bll是all前i项和。共11个仰角。
print(bll)
yj=np.full([4041,460],np.nan)
fwj=np.full([4041,460],np.nan)
jx=np.full([4041,460],np.nan)
fsl=np.full([4041,460],np.nan)
x=np.full([4041,460],np.nan)
y=np.full([4041,460],np.nan)
z=np.full([4041,460],np.nan)        # 仰角、方位角、径向、反射率、转化为局地直角坐标系后x、y、z坐标值。大小是总径向数*一条径向上数据个数，用缺测填充
for i in range(11):
    m=int(bll[i])
    n=int(bll[i+1])                   # m和n分别表示该仰角下第一条径向和最后一条径向在所有径向中的序号
    print(m,n)
    yj[m:n],fwj[m:n],jx[m:n],fsl[m:n]=radar_read('文件目录/文件名',i)                                     # 函数一：输入文件、仰角，输出仰角、方位角、径向、反射率
    x[m:n],y[m:n],z[m:n]=np.array(sph2cart(yj[m:n],fwj[m:n],jx[m:n]),dtype=float)                        # 函数二：输入仰角、方位角、径向，输出局地直角坐标系x、y、z坐标值
  
  
  ####以下是函数
  def radar_read(file_path,K):
    kk=K+1
    pi=np.pi
    # 读数据
    data=np.fromfile(file_path,np.uint8,count=-1)
    data=data.reshape([3994,2432])#################################################################需修改，基本上是xxxx*2432
    if data[0,72]==11:
        phi=[0.50,0.50,1.45,1.45,2.40,3.35,4.30,5.25,6.2,7.5,8.7,10,12,14,16.7,19.5]
    if data[0,72]==21:
        phi=[0.50,0.50,1.5,1.5,2.40,3.4,4.30,6.00,9.90,14.6,19.5]
    if data[0,72]==31:
        phi=[0.50,0.50,1.50,1.50,2.50,2.50,3.50,4.50]
    if data[0,72]==32:
        phi=[0.50,0.50,2.50,3.50,4.50]                                                 # 确认仰角模式
    g1=np.zeros([len(data),460])
    h1=np.zeros([len(data),460])
    i1=np.zeros([len(data),460])
    j1=np.zeros([len(data),460])
    yjxu=np.zeros([len(data),460])
    count=0
    while count<len(data):
        #print( "径向数据编号 : ",count)
        b1=data[count,44]+256*data[count,45]				#仰角序数
        yjxu[count,:]=data[count,44]+256*data[count,45]
        c1=(data[count,36]+256*data[count,37])/8*180/4096				#方位角
        d1=data[count,54]+256*data[count,55]				#径向库
        #print( "仰角序数,方位角,径向库 : ",b1,c1,d1)
        if d1==0:
            count+=1
            continue
        else:
            count+=1
        i=0
        while i<460:
            g1[count-1,i]=phi[b1-1]									#仰角
            h1[count-1,i]=c1												#方位角
            i1[count-1,i]=0.5+i-1											#径向
            if i>d1:																	#反射率
                j1[count-1,i]=0
            else:
                if data[count-1,128+i]==0:							#无数据
                    j1[count-1,i]=0
                else:
                    if data[count-1,128+i]==1:						#距离模糊
                        j1[count-1,i]=0
                    else:																#数据正常
                        j1[count-1,i]=(data[count-1,128+i]-2)/2-32
            i+=1
    n=kk																#选取第三个仰角的数据
    a2=0															#仰角序数
    while a2<len(data):
        if data[a2,44]>(n-1):
            break
        a2+=1
    a3=a2
    while a3<len(data):
        if data[a3,44]>(n):
            break
        a3+=1
    yj=g1[a2:a3,:]
    fwj=h1[a2:a3,:]
    jx=i1[a2:a3,:]
    fsl=j1[a2:a3,:]                  # 忘了具体在干嘛了，反正是因为每个仰角径向数目不一样，必须一个一个导出
    return yj,fwj,jx,fsl

def sph2cart(elevation,azimuth,r):
    ele,a= np.deg2rad([elevation,azimuth])               # 角度转化成弧度
    y=r*np.cos(ele)*np.cos(a)
    x= r * np.cos(ele) * np.sin(a)
    z = r * np.sin(ele)
    return x,y,z
