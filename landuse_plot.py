#!/usr/bin/python
# -*- coding: utf8 -*-

from fonction import *
from jules_download import *
from Split_times_Marine import *

from mpl_toolkits.basemap import Basemap
from osgeo import gdal

from rotate_landuse import *


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

save_plot='yes'
save_directory='/storage/shared/research/met/micromet/JULES/Marine/FIGURE/Landuse/'



name_var_clim='stratiform_rainfall_flux'
name_var_clim='UM_m01s03i217_vn1006'
name_var_clim='air_temperature'

year=[2006,2007,2008,2009,2010]


if(name_var_clim=='surface_downwelling_shortwave_flux_in_air') : 
	legend_axes_var='surface K down $W.m^{-2}$'
	climat_folder='/storage/shared/research/met/micromet/JULES/ClimateRuns/data2/'
	climat_file='u-aj981.ape.london.2006.nc'
elif(name_var_clim=='stratiform_rainfall_flux') :
	legend_axes_var='RR $KG.M^{-2}.S^{-1}$'
	climat_folder='/storage/shared/research/met/micromet/JULES/ClimateRuns/data2/'
	climat_file='u-aj981.apa.london.2006.nc'
else :
	if(name_var_clim=='air_temperature'):
		legend_axes_var='$T_{air}$ at 1.5m ($K$)'
	elif(name_var_clim=='surface_air_pressure'):
		legend_axes_var='$P$  $Pa$'
	else : 	legend_axes_var=name_var_clim+' (?)'
	climat_folder='/storage/shared/research/met/micromet/JULES/ClimateRuns/data2/'
	climat_file='u-aj981.ap9.london.2007.nc'

moruses_folder='/storage/shared/research/met/micromet/JULES/u-av612_MORUSES_London_KSSW/'
version_plot='' #OBS and AnthroOff
#var=['SW_up','QH','Q_star','K_star','K_down','L_up','L_down']
var=['QH']

for var_i in var :
	if (var_i=='QH') :
		legende_variable='$Q_{H}$  $W.m^{-2}$'
		name_variable_JULES='ftl_gb'
		name_variable_OBS='qh'
		name_file_plot='QH'
		name_variable_SUEWS='QH'
	if(version_plot==''):
		moruses_version=76930# Anthropogenic Flux OFF
	Start= datetime.datetime(2011, 01, 01,00,00,00)
	Var_moruses=jules_download(moruses_folder+str(moruses_version)+'/jules.all.nc',name_variable_JULES,Start)[0]
	Time_moruses=jules_download(moruses_folder+str(moruses_version)+'/jules.all.nc',name_variable_JULES,Start)[1]
	lon_JULES=jules_download(moruses_folder+str(moruses_version)+'/jules.all.nc','longitude',Start)[0]
	lat_JULES=jules_download(moruses_folder+str(moruses_version)+'/jules.all.nc','latitude',Start)[0]


f = Dataset(climat_folder+climat_file, 'r')
#for v in f.variables : print '****', v, f.variables[v] 



Time_CLIM= np.squeeze(f.variables['time'][:])
Var_CLIM= np.squeeze(f.variables[name_var_clim][:])

lon_CLIM=np.squeeze(f.variables['longitude'][:])
lat_CLIM=np.squeeze(f.variables['latitude'][:])


lon_GRID= np.append(np.squeeze(f.variables['longitude_bounds'][:])[:,0].tolist(),np.squeeze(f.variables['longitude_bounds'][:])[(lon_CLIM.shape[0]-1),1])
delta_lon_GRID=lon_GRID[1]-lon_GRID[0]

print lon_CLIM
print lon_CLIM.shape[0]
print lon_GRID
print lon_GRID.shape[0]

lat_GRID= np.append(np.squeeze(f.variables['latitude_bounds'][:])[:,0].tolist(),np.squeeze(f.variables['latitude_bounds'][:])[(lat_CLIM.shape[0]-1),1])
delta_lat_GRID=lat_GRID[1]-lat_GRID[0]
print type(lon_CLIM)
print lon_CLIM.shape[0]
print np.squeeze(f.variables['longitude_bounds'][:])[(lon_CLIM.shape[0]-1),1]
print lon_CLIM

lon_min=lon_GRID.min()
lon_max=lon_GRID.max()
lat_min=lat_GRID.min()
lat_max=lat_GRID.max()

index_lat=[]
for j in range(0,len(lat_GRID)) :
	if((lat_GRID[j]>lat_JULES-2*delta_lat_GRID and lat_GRID[j]<lat_JULES+2*delta_lat_GRID)) : index_lat.append(j)

index_lon=[]
for j in range(0,len(lon_GRID)) :
	if((lon_GRID[j]>lon_JULES-2*delta_lon_GRID and lon_GRID[j]<lon_JULES+2*delta_lon_GRID)) : index_lon.append(j)

index_lon_ruralwest=[]
for j in range(0,len(lon_GRID)) :
	if((lon_GRID[j]>-1.6 and lon_GRID[j]<-1.0)) : index_lon_ruralwest.append(j)

index_lon_north=[]
for j in range(0,len(lon_GRID)) :
	if((lon_GRID[j]>0.5 and lon_GRID[j]<1.0)) : index_lon_north.append(j)

index_lat_north=[]
for j in range(0,len(lat_GRID)) :
	if((lat_GRID[j]>51.8 and lat_GRID[j]<52.2)) : index_lat_north.append(j)

lat_CITY=np.array(lat_CLIM)[index_lat[0]:(index_lat[-1])]
lon_CITY=np.array(lon_CLIM)[index_lon[0]:(index_lon[-1])]
Var_CITY=Var_CLIM[:,index_lat[0]:(index_lat[-1]),index_lon[0]:(index_lon[-1])]
lon_RURALWEST=np.array(lon_CLIM)[index_lon_ruralwest[0]:(index_lon_ruralwest[-1])]
Var_RURALWEST=Var_CLIM[:,index_lat,index_lon_ruralwest]
Var_RURALWEST=Var_CLIM[:,index_lat[0]:(index_lat[-1]),index_lon_ruralwest[0]:(index_lon_ruralwest[-1])]
lon_NORTH=np.array(lon_CLIM)[index_lon_north[0]:(index_lon_north[-1])]
lat_NORTH=np.array(lat_CLIM)[index_lat_north[0]:(index_lat_north[-1])]
Var_NORTH=Var_CLIM[:,index_lat_north,index_lon_north]
Var_NORTH=Var_CLIM[:,index_lat_north[0]:(index_lat_north[-1]),index_lon_north[0]:(index_lon_north[-1])]



#######################################################
##### Plot

for i in range(0,9):
	landuse_frac=get_landuse_fraction('London','all',51.609375,-0.073125,show_plot='no')
	
landuse_list = ['b. leaf', 'n. leaf', 'C3', 'C4', 'shrubs', 'urban', 'lake', 'soil', 'ice']

f, case = plt.subplots(3,3, sharex='col', sharey='row',figsize=(10,5))
plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=0.00, hspace=0.00)
couleur=['red','orange','yellow','greenyellow','black','darkgreen','darkblue','cyan','magenta']
for i in range(0,9):
	landuse_frac_NORTH=get_landuse_fraction('London','all',lat_NORTH[i%3],lon_NORTH[i/3],show_plot='no')
	landuse_frac_WEST=get_landuse_fraction('London','all',lat_CITY[i%3],lon_RURALWEST[i/3],show_plot='no')
	landuse_frac_CITY=get_landuse_fraction('London','all',lat_CITY[i%3],lon_CITY[i/3],show_plot='no')
	print len(landuse_frac)
	case[2-i%3,i/3].bar(np.array(range(0,9)),landuse_frac_CITY,0.2,color='red',label='London')
	case[2-i%3,i/3].bar(np.array(range(0,9))+ 0.2,landuse_frac_NORTH,0.2,color='blue',label='North')
	case[2-i%3,i/3].bar(np.array(range(0,9))-0.2,landuse_frac_WEST,0.2,color='green',label='West')
	case[2-i%3,i/3].set_xticks(np.arange(9) + 0.2 / 3)
	case[2-i%3,i/3].set_xticklabels(landuse_list,rotation='vertical')
	case[2-i%3,i/3].set_ylim([0, 1])
	case[0,2].legend(loc='upper right',fontsize='small' )

if (save_plot=='yes') :plt.savefig(save_directory+'histogram_landuse_urban_rural.png',dpi=300)

landuse_frac_CITY=get_landuse_fraction('London','urban',lat_CITY[i%3],lon_CITY[i/3],show_plot='yes')







# Fixing random state for reproducibility
np.random.seed(19680801)


#ax = plt.subplot(111, projection='polar')

landuse_list = ['broadleaf', 'needleleaf', 'C3', 'C4', 'shrubs', 'urban', 'lake', 'soil', 'ice']
#couleur_landuse=['yellowgreen','darkgreen','yellow','greenyellow','lightgreen','red','blue','saddlebrown','w']
N = 8
theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
width = np.array([2*np.pi / N]*N)


#couleur_landuse = ['springgreen', 'darkgreen', 'lawngreen', 'coral', 'olive', 'dimgrey', 'deepskyblue', 'sienna', 'lightsteelblue']


def landuse_frac_circle(vect_lat,vect_lon,landuse_list,titre='',save_plot=save_plot,site='LONDON'):
	fig, ax = plt.subplots(figsize=(16,8))
	ax = plt.subplot(111, projection='polar')
	couleur_landuse = ['springgreen', 'darkgreen', 'lawngreen', 'coral', 'olive', 'dimgrey', 'deepskyblue', 'sienna', 'lightsteelblue']
	N = 8
	theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
	width = np.array([2*np.pi / (N)]*(N))
	landuse_add=[]
	landuse_add.append(np.array([0]*8))
	for j in range(0,len(landuse_list)):
		landuse_1_CITY=[]
		for i in [7,8,5,2,1,0,3,6]:
			landuse_1_CITY.append(get_landuse_fraction('London',landuse_list[j],vect_lat[i%3],vect_lon[i/3],show_plot='no'))
		landuse_add.append(landuse_add[j]+np.array(landuse_1_CITY))
	print 'len',len(landuse_add), len(landuse_list)
	for j in range(0,(len(landuse_add)-1)):
		print j, j+1
		bars = ax.bar(theta, landuse_add[j+1]-landuse_add[j], width=width, bottom=landuse_add[j],color=couleur_landuse[j],tick_label=['12','22','21','20','10','00','01','02'],label=landuse_list[j],edgecolor='k',alpha=0.4,linewidth=0.5)
	r = [0]+get_landuse_fraction('London','all',vect_lat[1],vect_lon[1],show_plot='no')
	theta_line = np.linspace(0.0, 2 * np.pi, 100, endpoint=False)
	for j in (range(0,len(landuse_list)-1)):
		if (j%2==0): lines='--'
		else : lines=':'
		bars = ax.plot(theta_line.tolist()+[theta_line[0]], [sum(r[0:(j+1)])]*(len(theta_line)+1),color=couleur_landuse[j],linewidth=2.0,linestyle=lines,label=landuse_list[j])
	if (save_plot=='yes') :plt.savefig(save_directory+'circle_'+site+'_all.png',dpi=300)
	ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.6))
	ax.set_title(titre)
	fig, ax = plt.subplots(figsize=(16,8))
	ax = plt.subplot(111, projection='polar')
	print 'r',r
	for i in range(0,len(r)-1):
		bars=ax.bar(theta[2], r[i+1], width=width[2], bottom=sum(r[0:i+1]),color=couleur_landuse[i+1],tick_label=['11'],label=landuse_list[i+1],edgecolor='k',alpha=0.4,linewidth=0.5)
	ax.set_title(titre)
	if (save_plot=='yes') :plt.savefig(save_directory+'circle_'+site+'_central.png',dpi=300)




landuse_frac_circle(lat_CITY,lon_CITY,landuse_list,titre='London')
#landuse_frac_circle(lat_CITY,lon_RURALWEST,landuse_list,titre='WEST',site='WEST')
#landuse_frac_circle(lat_NORTH,lon_NORTH,landuse_list,titre='NORTH',site='NORTH')






def landuse_frac_box(vect_lat,vect_lon,landuse_list,titre=''):
	f, case = plt.subplots(len(vect_lat),len(vect_lon), sharex='col', sharey='row',figsize=(14,7))
	plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=0.00, hspace=0.00)
	couleur_landuse = ['springgreen', 'darkgreen', 'lawngreen', 'coral', 'olive', 'dimgrey', 'deepskyblue', 'sienna', 'lightsteelblue']
	for i in range(0,len(vect_lat)*len(vect_lon)): # we will browse each latitute and each longitude
#		print '***'
#		print len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)
#		print len(vect_lat),i%len(vect_lat), len(vect_lon),i/len(vect_lat)
#		print i/len(vect_lon),len(vect_lat)-i%len(vect_lon)
#		print vect_lat[i/len(vect_lon)], vect_lon[i%len(vect_lon)]
		landuse_frac_CITY=[0]+get_landuse_fraction('London','all',vect_lat[i/len(vect_lon)],vect_lon[i%len(vect_lon)],show_plot='no') # extraction od the land fraction for each type of land for 1 lat and 1 lon
		for j in range(0,len(landuse_list)-1):
			#plot the landuse fraction
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].bar([1],[landuse_frac_CITY[j+1]], bottom=[sum(landuse_frac_CITY[0:j+1])],color=couleur_landuse[j+1],alpha=0.4)
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].set_xticks([])
			if(len(vect_lat)*len(vect_lon)<20) : case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].annotate(str(i/len(vect_lon))+str(i%len(vect_lon)),xy=(0.005,    0.8), xycoords = 'axes fraction')
		print sum(landuse_frac_CITY)
	plt.suptitle(titre)

#landuse_frac_box(lat_CLIM[1:len(lat_CLIM)-1],lon_CLIM[1:len(lon_CLIM)-1],landuse_list,titre='London')
#landuse_frac_box(lat_CLIM,lon_CLIM,landuse_list,titre='London')
landuse_frac_box(lat_CITY,lon_CITY,landuse_list,titre='London')
#landuse_frac_box(lat_CITY,lon_RURALWEST,landuse_list,titre='WEST')
#landuse_frac_box(lat_NORTH,lon_NORTH,landuse_list,titre='NORTH')

print '################'
print '11',get_landuse_fraction('London','all',lat_CITY[1],lon_CITY[1],show_plot='no')
print '22',get_landuse_fraction('London','all',lat_CITY[2],lon_CITY[2],show_plot='no')
print '12',get_landuse_fraction('London','all',lat_CITY[1],lon_CITY[2],show_plot='no')
print '02',get_landuse_fraction('London','all',lat_CITY[0],lon_CITY[2],show_plot='no')

#plt.show()



## with box LONDON WEST and NORTH in red, green and blue
def landuse_frac_box(vect_lat,vect_lon,landuse_list,titre='',lat_city=lat_CITY,lon_city=lon_CITY,lat_north=lat_NORTH,lon_north=lon_NORTH,lon_west=lon_RURALWEST):
	f, case = plt.subplots(len(vect_lat),len(vect_lon), sharex='col', sharey='row',figsize=(14,7))
	plt.subplots_adjust(left=None, bottom=None, right=None, top=None,wspace=0.00, hspace=0.00)
	couleur_landuse = ['springgreen', 'darkgreen', 'lawngreen', 'coral', 'olive', 'dimgrey', 'deepskyblue', 'sienna', 'lightsteelblue']
	for i in range(0,len(vect_lat)*len(vect_lon)):
	#for i in range(0,40):
		#landuse_frac_NORTH=[0]+get_landuse_fraction('London','all',lat_NORTH[i%3],lon_NORTH[i/3],show_plot='no')
		#landuse_frac_WEST=[0]+get_landuse_fraction('London','all',lat_CITY[i%3],lon_RURALWEST[i/3],show_plot='no')
		print '***'
		#print str(i/len(vect_lon)), str(i%len(vect_lon))
		print len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)
		print len(vect_lat),i%len(vect_lat), len(vect_lon),i/len(vect_lat)
		print i/len(vect_lon),len(vect_lat)-i%len(vect_lon)
		print vect_lat[i/len(vect_lon)], vect_lon[i%len(vect_lon)]
		landuse_frac_CITY=[0]+get_landuse_fraction('London','all',vect_lat[i/len(vect_lon)],vect_lon[i%len(vect_lon)],show_plot='no')
		print landuse_frac_CITY	
		print '***'
		for j in range(0,len(landuse_list)-1):
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].bar([1],[landuse_frac_CITY[j+1]], bottom=[sum(landuse_frac_CITY[0:j+1])],color=couleur_landuse[j+1],alpha=0.4)
		case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].set_xticks([])
		case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].set_yticks([])
		#if(len(vect_lat)*len(vect_lon)<20) : case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].annotate(str(i/len(vect_lon))+str(i%len(vect_lon)),xy=(0.005,    0.8), xycoords = 'axes fraction')
	for i in range(0,len(vect_lat)*len(vect_lon)):
		if(vect_lat[i/len(vect_lon)] in lat_city and vect_lon[i%len(vect_lon)] in lon_city) :
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['bottom'].set_color('red')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['top'].set_color('red')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['left'].set_color('red')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['right'].set_color('red')
		if(vect_lat[i/len(vect_lon)] in lat_city and vect_lon[i%len(vect_lon)] in lon_west) :
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['bottom'].set_color('green')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['top'].set_color('green')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['left'].set_color('green')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['right'].set_color('green')
		if(vect_lat[i/len(vect_lon)] in lat_north and vect_lon[i%len(vect_lon)] in lon_north) :
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['bottom'].set_color('blue')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['top'].set_color('blue')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['left'].set_color('blue')
			case[len(vect_lat)-1-i/len(vect_lon),i%len(vect_lon)].spines['right'].set_color('blue')
		print sum(landuse_frac_CITY)
	plt.suptitle(titre)

landuse_frac_box(lat_CLIM[1:len(lat_CLIM)-1],lon_CLIM[1:len(lon_CLIM)-1],landuse_list,titre='London')
if (save_plot=='yes') :plt.savefig(save_directory+'landuse_all.png',dpi=300)
#landuse_frac_box(lat_CLIM,lon_CLIM,landuse_list,titre='London')
landuse_frac_box(lat_CITY,lon_CITY,landuse_list,titre='')
if (save_plot=='yes') :plt.savefig(save_directory+'landuse_london.png',dpi=300)
landuse_frac_box(lat_CITY,lon_RURALWEST,landuse_list,titre='')
if (save_plot=='yes') :plt.savefig(save_directory+'landuse_west.png',dpi=300)
landuse_frac_box(lat_NORTH,lon_NORTH,landuse_list,titre='')
if (save_plot=='yes') :plt.savefig(save_directory+'landuse_north.png',dpi=300)



#landuse_frac_box(lat_CITY,lon_CITY,landuse_list,titre='London')
#print len(lat_CITY), len(lon_CITY)

plt.show()
