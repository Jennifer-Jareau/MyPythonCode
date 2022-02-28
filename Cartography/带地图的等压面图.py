##需要有地图文件
###以下为绘图前设置函数，参数一：画布名；参数二：经纬度范围；参数三、四：经纬度绘图间隔，参数五、六：经纬度标注起始长度（比如绘图从23N开始，但是标注从25N开始，此参数即为2）
def startup(f,extent_,spec_lon,spec_lat,gap_lon,gap_lat):
    lon_formatter = cticker.LongitudeFormatter()
    lat_formatter = cticker.LatitudeFormatter()
    f.xaxis.set_major_formatter(lon_formatter)
    f.yaxis.set_major_formatter(lat_formatter)
    plt.xticks(fontsize=30)                                                                     #字体大小
    plt.yticks(fontsize=30)
    f.add_feature(cfeature.COASTLINE.with_scale('50m'),edgecolor='grey',linewidths=1)           #海岸线边界  
    #f.add_feature(cfeature.LAKES, alpha=0.5)                                                   #湖泊（贝加尔湖等）
    f.set_extent(extent_, crs=ccrs.PlateCarree())
    f.set_xticks(np.arange(extent_[0]+gap_lon,extent_[1],spec_lon), crs=ccrs.PlateCarree())
    f.set_yticks(np.arange(extent_[2]+gap_lat,extent_[3],spec_lat), crs=ccrs.PlateCarree())

def drawboundary(f):
    china = shpreader.Reader('/xxxxxxxxxxxxxxxxxxxxxxx/bou2_4l.dbf').geometries()               #地图文件的位置
    f.add_geometries(china,ccrs.PlateCarree(),facecolor='none', edgecolor='grey',zorder = 2)    


###准备工作
leftlon,rightlon,lowerlat,upperlat=(90,155,20,55)                                               #绘图范围
extent=[leftlon,rightlon,lowerlat,upperlat]
proj = ccrs.PlateCarree(central_longitude=0)
fig=plt.figure(figsize=(12,7))
f= fig.add_axes([0.1,0.1,0.85,0.9],projection = proj)
startup(f,extent,20,10,0,0)
drawboundary(f)

###绘制风矢，小于5的不画，同时画两个高度的风，确保比例相等
cmap_wind_1 = mpl.colors.ListedColormap(['#00000000','black'])                            #500hPa风矢黑色，保留>15m/s
bounds_wind_1= [15]
norm_wind_1= mpl.colors.BoundaryNorm(bounds_wind_1, cmap_wind_1.N)
cmap_wind_2 = mpl.colors.ListedColormap(['#00000000','red'])                              #700hPa风矢红色，保留>8m/s
bounds_wind_2 = [8]
norm_wind_2 = mpl.colors.BoundaryNorm(bounds_wind_2, cmap_wind_2.N)
U_1=u[t,2]
V_1=v[t,2]
speed_1=(U_1**2+V_1**2)**0.5                                                              #以水平风速作为箭头长度的参考，scale用于固定相对长度，要确保两个scale一致
c1=f.quiver(lon[::10],lat[::10],U_1[::10,::10],V_1[::10,::10],speed_1[::10,::10],width=0.0027,cmap=cmap_wind_1,norm=norm_wind_1,scale=400,headwidth=4,zorder=2,transform=ccrs.PlateCarree())
f.quiverkey(c1,1.07,0.01,15,'15',fontproperties={'size':20})                              #展示15m/s的风矢长度，写一次就够了
U_2=u[t,3]
V_2=v[t,3]
speed_2=(U_2**2+V_2**2)**0.5                                                              #同上，确保两个scale一致
c2=f.quiver(lon[::10],lat[::10],U_2[::10,::10],V_2[::10,::10],speed_2[::10,::10],width=0.0027,cmap=cmap_wind_2,norm=norm_wind_2,scale=400,headwidth=4,zorder=2,transform=ccrs.PlateCarree())

