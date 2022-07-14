####读取nc文件
import xarray as xr
data= xr.open_dataset('data.nc')

#####读取grib文件
import xarray as xr
import cfgrib
data=xr.open_dataset('data.grib',engine='cfgrib',backend_kwargs={'filter_by_keys':{'dataType': 'cf'}})

#####读取txt文件
data=np.loadtxt('data.txt').reshape((大小))[可切片]

#####读取npy文件
data=np.load('data.npy')
