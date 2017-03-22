import pygmaps1 as pg	#import library used to convert python code to javascript used in google maps
mymap = pg.pygmaps(41.979595,-87.90446417, 10,'ROADMAP')	#centerlatitude, ceneterlongitude, zoomlevel(higher value more zoom), Maptype (SATELLITE,ROADMAP,HYBRID,TERRAIN)
rslt = []
with open('C:\\Users\\naiti\\Desktop\\data.csv') as csvfile:	#open any file which have raw data from sensors
	next(csvfile)		#for header file avoid
	for reader in csvfile:		#every record in csv file
		ext = reader.split(",")		#create a list from string separated by comma
		lat1 = ext[3]				#extract latitude from 3rd position
		long1 = ext[4]				#extract longitude from 4th position
		rslt.append((float(lat1),float(long1)))		#add longlat into tuple of list
		mymap.addpoint(float(lat1),float(long1),'#0000FF')		#to add point on map
csvfile.close()
mymap.addpath(rslt,'#00FF00')		#with all points in rslt[] create poly line between them
mymap.draw('./mymap.html')			#draw html with name and path given
