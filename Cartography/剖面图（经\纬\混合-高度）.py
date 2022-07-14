from metpy.cbook import get_test_data            ##使用Metpy计算斜剖线上的物理量
from metpy.interpolate import cross_section

start=(40,113.5)                                 ##确定剖面起止点，可以斜，可以不
end=(31,119)
u=data['u'][:,LL:,lat_u:lat_l,lon_l:lon_r].metpy.assign_crs(grid_mapping_name='latitude_longitude', earth_radius=6371229.0)       ##要使用Metpy计算，必须添加一些信息
v=data['v'][:,LL:,lat_u:lat_l,lon_l:lon_r].metpy.assign_crs(grid_mapping_name='latitude_longitude', earth_radius=6371229.0)
div=data['d'][:,LL:,lat_u:lat_l,lon_l:lon_r].metpy.assign_crs(grid_mapping_name='latitude_longitude', earth_radius=6371229.0)
omega=data['w'][:,LL:,lat_u:lat_l,lon_l:lon_r].metpy.assign_crs(grid_mapping_name='latitude_longitude', earth_radius=6371229.0)
u_cross = cross_section(u, start, end)
v_cross = cross_section(v, start, end)
div_cross = cross_section(div, start, end)
omega_cross = cross_section(omega, start, end)

#########重点：若斜剖，如何确定沿剖面的水平风大小？############
new_e1=[1.386,0.847]                          ##新x方向的基向量（非单位矢量）。原x轴，与经线平行，新x轴取与剖面垂直指向剖面顺时针方向90度
new_e2=[-0.847,1.386]                         ##新y方向的基向量（非单位矢量）。原y轴，与纬线平行，新y轴取与剖面行。这两行数据可先画斜剖线的矢量图，再根据图片测量可得
det=np.linalg.det([new_e1,new_e2])            ##组成新坐标系的基向量矩阵
det_e2=np.linalg.norm(new_e2)                 ##新y方向基向量长度
v_new=np.full((垂直层数,100),np.nan)           ##新建，上一步自动剖成100个
for l in range(垂直层数):
    for i in range(100):
        v_new[t,l,i]=np.matrix(new_e2)*np.matrix([u_cross[t,l,i],v_cross[t,l,i]]).T/det*det_e2
#########over! 原理：利用线性代数进行不同基向量下的转换############

#########画图############
fig=plt.figure(figsize=(4.5,4))
f=fig.add_axes([0.1,0.1,0.8,0.8])
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
f.invert_yaxis()
f.set_yscale('symlog')
plt.yticks([400,450,500,550,600,650,700,750,775,800,825,850,875,900,925,950,975,1000])
#f.set_xticklabels([r'115$^\degree$E',r'120$^\degree$E',r'125$^\degree$E',r'130$^\degree$E'])
f.set_yticklabels(['400','','500','','600','','700','','','','','850','','','','950','','1000'])
plt.ylim(ymin=1000, ymax=400)

c1=f.quiver(lon[::5],level_n,V[t,:,::5],W[t,:,::5],VV[t,:,::5],width=0.003,headwidth=3.5,zorder=2,cmap=cmap_wind,scale=350,norm=norm_wind,color='Black')
f.quiverkey(c1,1.09,-0.01,15,'15',fontproperties={'size':9})

DIV=ndimage.gaussian_filter(div_cross[t]*10**4,sigma=0)
c4=f.contourf(lon,level_n,DIV,cmap='RdYlBu_r')
cb=plt.colorbar(c4,extendfrac='auto',fraction=0.035,aspect=20,spacing='uniform',orientation='vertical',)
#cb.ax.tick_params(labelsize=10)

drawlandcross(f,start,end)
f.set_title(str(fname[t],encoding='utf-8'),loc='left',fontsize=10)
plt.savefig('/地址/文件名.png',dpi=650)
#plt.close()


#########地形覆盖函数############
def drawlandcross(f,start,end):
    top=xr.open_dataset("地址/china_near.nc")
    pz=(1-top['z']/44331.0)**(1.0/0.1903)*1013.255
    z=pz.metpy.assign_crs(grid_mapping_name='latitude_longitude', earth_radius=6371229.0)
    z=z*units.hectopascal
    z_cross=cross_section(z,start,end)
    lat_z=z_cross['y']
    lon_z=z_cross['x']
    c=f.fill_between(lon_z,1010,z_cross,facecolor='#D3D3D3',zorder=10)


