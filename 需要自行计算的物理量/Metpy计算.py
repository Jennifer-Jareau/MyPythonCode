# 位温/相当位温
太无语了写完的代码被我删了，有时间再来



# 水汽通量/水汽通量散度
data=xr.open_dataset(file_name[FF])
q=data['q']
u=data['u']
v=data['v']
V=(u**2+v**2)**0.5
Q=q*V/(constants.g.magnitude)   #去单位
qu=q*u
qv=q*v

lon=data['longitude']
lat=data['latitude']
times=data['time']
levels=data['level']
dx,dy = mpcalc.lat_lon_grid_deltas(lon,lat)
Qdiv=xr.DataArray(np.zeros((48,23,141,221)), coords=[times,levels,lat,lon], dims=['time', 'level','latitude','longitude'])
for t in range(len(data['time'])):
    for l in range(len(data['level'])):
        Qdiv[t,l]= mpcalc.divergence(u=qu[t,l],v=qv[t,l],dx=dx,dy=dy)
#完了就按需保存
