
def startup(f,extent_,spec_lon,spec_lat,font,flag):
    """
    restrict drawing extent, and axis label
    """
    lon_formatter = cticker.LongitudeFormatter()
    lat_formatter = cticker.LatitudeFormatter()
    f.xaxis.set_major_formatter(lon_formatter)
    f.yaxis.set_major_formatter(lat_formatter)
    f.xaxis.set_minor_locator(MultipleLocator(5))
    f.yaxis.set_minor_locator(MultipleLocator(5))
    plt.xticks(fontsize=font)
    plt.yticks(fontsize=font)
    f.add_feature(cfeature.COASTLINE.with_scale('50m'),edgecolor='grey',linewidths=0.7)
    f.set_extent(extent_, crs=ccrs.PlateCarree())
    f.set_xticks(np.arange(extent_[0],extent_[1]+1,spec_lon), crs=ccrs.PlateCarree())
    f.set_yticks(np.arange(extent_[2],extent_[3]+1,spec_lat), crs=ccrs.PlateCarree())
    if flag!=0:
        f.set_yticklabels([])
    
def drawboundary(f):
    """
    add national & province boundaries
    """
    china = shpreader.Reader('/Volumes/xx/xx.dbf').geometries()
    f.add_geometries(china,ccrs.PlateCarree(),facecolor='none', edgecolor='grey',linewidths=0.5,zorder = 2)

def draw_quiver(f,u,v,GG,color,scale,stander,standername,lpos,flag):
    """
    eliminate vectors weaker than 15
    """
    # cmap_wind = mpl.colors.ListedColormap(['#00000000','black'])
    # bounds_wind= [15]
    # norm_wind= mpl.colors.BoundaryNorm(bounds_wind, cmap_wind.N)
    # c1=f.quiver(lon[::10],lat[::10],U_1[::10,::10],V_1[::10,::10],speed_1[::10,::10],width=0.0027,cmap=cmap_wind,norm=norm_wind,
    #             scale=400,headwidth=4,zorder=2,transform=ccrs.PlateCarree())

    c=f.quiver(lon[::GG],lat[::GG],u[::GG,::GG].data,v[::GG,::GG].data,color=color,width=0.006,scale=scale,
                headwidth=2.5,zorder=2,transform=ccrs.PlateCarree())
    if flag:
        f.quiverkey(c,0.85,-0.2,stander,standername,labelpos=lpos,labelsep=0.05,fontproperties={'size':7})

def draw_lines(f,var,linelevels,color,sigma,lw):
    VAR=ndimage.gaussian_filter(var,sigma=sigma) #, linestyles='-'
    c = f.contour(lon, lat, VAR, colors=color, levels=linelevels,linewidths=lw, transform=ccrs.PlateCarree())
    cb=f.clabel(c,fontsize=8,fmt='%1.0f',zorder=6,)
    
def draw_lines_eliminate0(f, var, linelevels, color, sigma, lw, fmt):
    """
    eliminate 0.0 line for anomalies or bold it
    """
        VAR = ndimage.gaussian_filter(var, sigma=sigma)
        if 0.0 in linelevels:
            levels = [lvl for lvl in linelevels if lvl != 0.0]
            c = f.contour(lon, lat, VAR, colors=color, levels=levels, linewidths=lw, transform=ccrs.PlateCarree(), zorder=5)
            f.clabel(c, fontsize=8, fmt=fmt, zorder=6)
#             c0 = f.contour(lon, lat, VAR, colors=color, levels=[0.0],linewidths=lw + 0.5, transform=ccrs.PlateCarree(), zorder=5)
#             f.clabel(c0, fontsize=8, fmt=fmt, zorder=6)
        else:
            c = f.contour(lon, lat, VAR, colors=color, levels=linelevels,linewidths=lw, transform=ccrs.PlateCarree(), zorder=5)
            f.clabel(c, fontsize=8, fmt=fmt, zorder=6)
            
def draw_shades(f,var,linelevels,extend,colormaps,sigma,title,fcb,flag,L):
    VAR=ndimage.gaussian_filter(var,sigma=sigma)
        c=f.contourf(lon,lat,VAR,levels=linelevels,cmap=colormaps, extend=extend,transform=ccrs.PlateCarree())
    
    if flag:
        cb=fig.colorbar(c, cax=fcb,extendfrac='auto',shrink=1,orientation='horizontal',extend='both' )
        cb.ax.tick_params(labelsize=9)
        cb.set_label(title,labelpad=0, rotation=0,fontsize=9)   
        
def adjust_pos(f,x0,y0,w,h):
    f_pos=f.get_position()
    f.set_position([f_pos.x0+x0, f_pos.y0+y0,f_pos.width+w,f_pos.height+h])
    
def draw_rectangle(f, extent, color, lw, ls):
    rec = plt.Rectangle(  (extent[0], extent[2]), extent[1] - extent[0],  extent[3] - extent[2],
        edgecolor=color, linestyle=ls, fill=False,  linewidth=lw, zorder=30, transform=ccrs.PlateCarree()    )
    f.add_patch(rec)

if __name__ == "__main__":
    proj = ccrs.PlateCarree(central_longitude=0)
    fig=plt.figure(figsize=(7,8.5))   
    gs=fig.add_gridspec(6,1,width_ratios=[1,1,1],height_ratios=[40,1,40,1,40,1])
    f1=fig.add_subplot(gs[0,0],projection = proj)
    plt.title('(a) Land-Only',loc='left')
    f2=fig.add_subplot(gs[2,0],projection = proj)
    plt.title('(d) Land-Only',loc='left')
    f3=fig.add_subplot(gs[4,0],projection = proj)
    plt.title('(g) Land-Only',loc='left')
    fcb1=fig.add_subplot(gs[1,0])
    fcb2=fig.add_subplot(gs[3,0])
    fcb3=fig.add_subplot(gs[5,0])


