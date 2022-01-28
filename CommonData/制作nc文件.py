
dataset=xr.Dataset({'d':climate_t_08,            #要保证这些变量都还是dataarray格式，且大小相同
                  'z':climate_z_08,
                  'q':climate_q_08,
                  't':climate_t_08,
                  'u':climate_u_08,
                  'v':climate_v_08,
                  'w':climate_w_08,
                  'vo':climate_vo_08,
                 })
dataset_08.to_netcdf('climate_08.nc')

#这样就制作好了一个气候态文件，以下是ta的样子
   #<xarray.Dataset>
   #Dimensions:    (latitude: 261, level: 11, longitude: 481)
   #Coordinates:
   #  * longitude  (longitude) float32 20.0 20.25 20.5 20.75 ... 139.5 139.8 140.0
   #  * latitude   (latitude) float32 75.0 74.75 74.5 74.25 ... 10.5 10.25 10.0
   #  * level      (level) int32 100 150 200 250 300 400 500 600 700 850 950
   #Data variables:
   #    d          (level, latitude, longitude) float32 228.3 228.3 ... 295.8 295.8
   #    z          (level, latitude, longitude) float32 1.613e+05 ... 5.293e+03
   #    q          (level, latitude, longitude) float32 2.534e-06 ... 0.01679
   #    t          (level, latitude, longitude) float32 228.3 228.3 ... 295.8 295.8
   #    u          (level, latitude, longitude) float32 2.815 2.823 ... -0.4531
   #    v          (level, latitude, longitude) float32 1.805 1.794 ... 0.9429
   #    w          (level, latitude, longitude) float32 0.0008659 ... -0.009231
   #    vo         (level, latitude, longitude) float32 -2.598e-07 ... 4.198e-06
