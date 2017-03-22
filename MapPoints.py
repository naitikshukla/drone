import pygmaps1 as pg
mymap = pg.pygmaps(41.979595,-87.90446417, 10,'ROADMAP')	#centerlatitude, ceneterlongitude, zoomlevel(higher value more zoom), Maptype (SATELLITE,ROADMAP,HYBRID,TERRAIN)
rslt = []
with open('C:\\Users\\naiti\\Desktop\\data.csv') as csvfile:
	next(csvfile)
	for reader in csvfile:
		ext = reader.split(",")
		lat1 = ext[3]
		long1 = ext[4]
		rslt.append((float(lat1),float(long1)))
		mymap.addpoint(float(lat1),float(long1),'#0000FF')
csvfile.close()
mymap.addpath(rslt,'#00FF00')
mymap.draw('./mymap.html')
