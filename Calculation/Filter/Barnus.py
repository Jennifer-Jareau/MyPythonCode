import Barnes
import xarray as xr
import numpy as np

data=xr.open_dataset('****/data.nc')
z=data['z'].data.transpose()               ##换轴
Barnes.bns(z,3000.0,'z3k.txt')             ##两次低通滤波
Barnes.bns(z,150000.0,'z150k.txt')





def read_bns(file):
    f=open(file,'r+')
    txt=[]
    for line in f:
        line = line.strip("\n")
        line = line.split()
        txt.append(line)
    tt= np.concatenate(txt).reshape(13,111,151)
    return tt.astype(float)

def filter_res(high,low):
    b11=read_bns(high)
    b21=read_bns(low)
    bns=b11-b21
    stk=np.array([b11,bns,b21])
    return stk

stk_z=filter_res('z3k.txt','z150k.txt')

lon=np.arange(90,130.25,0.25)[5:-5]         #滤波后数据比元数据每边小了5
lat=np.arange(50,19.75,-0.25)[5:-5]
level=data['level'].data
scale=['high','band','low']

ds=xr.Dataset({
        'z':(['scale','level','lat','lon'],stk_z),},

  coords={'scale':(['scale'],scale),
          'level':(['level'],level),
          'lat':(['lat'],lat),
          'lon':(['lon'],lon),}
)
ds.to_netcdf('Barnes.nc')
