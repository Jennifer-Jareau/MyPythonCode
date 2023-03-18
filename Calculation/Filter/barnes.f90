subroutine bns(infile,c,outfilename)
parameter (nx=161,ny=121,nv=13,g1=0.3)
parameter (nx1=151,ny1=111)
real  infile(nx,ny,nv),twodim(nx,ny,nv)
real  pslab(nx,ny)
real  work(nx,ny)
real  lona(nx,ny),lata(nx,ny)
real  lonb(nx,ny),latb(nx,ny)
real  lon1,lat1
real  lat0,lon0
real  d(nx,ny),f0(nx,ny),f1(nx,ny)
real  barnes0(nx1,ny1,nv), barnes1(nx1,ny1,nv)
real c
character(len=16) outfilename
!     nx-----x方向格点数
!     ny-----y方向格点数
!     nv-----待滤波的变量数
!     c1,g1,c2,g2 滤波参数
!     twodim----原始资料
!     pslab,work 工作数组
!     lon0，lat0 区域左下角的经纬度
!     lona(nx),lata(ny) 计算点的经纬度
!     lonb(nx),latb(ny) 参与滤波点的经纬度


!!! 读数据开始
twodim(1:nx,1:ny,1:nv)=infile
!!! 读数据结束
!区域左下角的纬度
lat0=50.
!区域左下角的经度
lon0=90.
!!! 开始调用barnes 滤波程序
do iv=1,nv
do iy=1,ny
do ix=1,nx

work(ix,iy)=twodim(ix,iy,iv)
pslab(ix,iy)=twodim(ix,iy,iv)
d(ix,iy)=0.0
f0(ix,iy)=0.0
f1(ix,iy)=0.0
enddo
enddo

do ix=1+5,nx-5
do iy=1+5,ny-5

lona(ix,iy)=lon0+(ix-1)*0.25
lata(ix,iy)=lat0-(iy-1)*0.25
lon1=lona(ix,iy)
lat1=lata(ix,iy)

ixst=ix-5
ixed=ix+5
iyst=iy-5
iyed=iy+5
rr2=0.0
sumw=0.0
sumwfk=0.0

do  i=ixst,ixed
do  j=iyst,iyed
lonb(i,j)=lon0+(i-1)*0.25
latb(i,j)=lat0-(j-1)*0.25

rr2=(lon1-lonb(i,j))*(lon1-lonb(i,j))+(lat1-latb(i,j))*(lat1-latb(i,j)) 
rr2=rr2*111.0*110.0                ! 一个经经纬度计为111km
fk=work(i,j)
call calw(rr2,fk,1.0,c,w,wfk)
sumw=sumw+w
sumwfk=sumwfk+wfk

enddo
enddo

pslab(ix,iy)=sumwfk/sumw
D(ix,iy)=work(ix,iy)-pslab(ix,iy)
f0(ix,iy)=pslab(ix,iy)

enddo
enddo

do i=1,nx1
do j=1,ny1
barnes0(i,j,iv)=f0(i+5,j+5)
enddo
enddo

write(*,*)'over'
        
!滤波初值场计算结束 


!--------------------开始第一次滤波修正


do ix=1+5,nx-5
do iy=1+5,ny-5

lona(ix,iy)=lon0+(ix-1)*0.25
lata(ix,iy)=lat0-(iy-1)*0.25
lon1=lona(ix,iy)
lat1=lata(ix,iy)

ixst=ix-5
ixed=ix+5
iyst=iy-5
iyed=iy+5
rr2=0.0
sumw=0.0
sumwfk=0.0

do  i=ixst,ixed
do  j=iyst,iyed
lonb(i,j)=lon0+(i-1)*0.25
latb(i,j)=lat0-(j-1)*0.25
rr2=(lon1-lonb(i,j))*(lon1-lonb(i,j))+(lat1-latb(i,j))*(lat1-latb(i,j)) 
rr2=rr2*111.0*110.0                      ! 一个经经纬度计为111km
fk=d(i,j)
call calw(rr2,fk,g1,c,w,wfk)
sumw=sumw+w
sumwfk=sumwfk+wfk
enddo
enddo

pslab(ix,iy)=sumwfk/sumw
f1(ix,iy)=f0(ix,iy)+pslab(ix,iy)
enddo
enddo

do i=1,nx1
do j=1,ny1
barnes1(i,j,iv)=f1(i+5,j+5)
enddo
enddo


!第一次滤波修正结束 

enddo


!!!   写结果开始
open(3,file=outfilename)
do iv=1,nv
do iy=1,ny1
write(3,*) barnes1(:,iy,iv)
enddo
enddo
close(3)

end subroutine bns



subroutine calw(rk,fk,g,c,w,wfk)
real fk,w,wfk
real g,c
real rk
w=exp(-rk/(4.0*g*c))
wfk=w*fk
end subroutine calw


