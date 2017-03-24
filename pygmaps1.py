import math
###########################################################
## Google map python wrapper V0.1
## Modified by Naitik Original Library pygmaps taken from https://pypi.python.org/pypi/pygmaps/0.1.1
############################################################

class pygmaps:

	def __init__(self, centerLat, centerLng, zoom , maptype):
		self.center = (float(centerLat),float(centerLng))
		self.zoom = int(zoom)
		self.maptype = str(maptype)
		self.grids = None
		self.paths = []
		self.points = []
		self.radpoints = []
		self.gridsetting = None
		self.coloricon = 'https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0'
		#self.coloricon = 'http://chart.apis.google.com/chart?cht=mm&chs=12x16&chco=FFFFFF,XXXXXX,000000&ext=.png'

	def addpoint(self, lat, lng, color = '#FF0000'):
		self.points.append((lat,lng,color[1:]))

	#def addpointcoord(self, coord):
	#	self.points.append((coord[0],coord[1]))

	def addpath(self,path,color = '#FF0000'):
		path.append(color)
		self.paths.append(path)
	
	#create the html file which inlcude one google map and all points and paths
	def draw(self, htmlfile):
		f = open(htmlfile,'w')
		f.write('<html>\n')
		f.write('<head>\n')
		f.write('<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
		f.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
		f.write('<title>Google Maps - pygmaps </title>\n')
		f.write('<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>\n')
		f.write('<script type="text/javascript">\n')
		f.write('\tfunction initialize() {\n')
		self.drawmap(f)
		#self.drawgrids(f)
		self.drawpoints(f)
		#self.drawradpoints(f)
		self.drawpaths(f,self.paths)
		f.write('\t}\n')
		f.write('</script>\n')
		f.write('</head>\n')
		f.write('<body style="margin:0px; padding:0px;" onload="initialize()">\n')
		f.write('\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
		f.write('</body>\n')
		f.write('</html>\n')		
		f.close()


	def drawpoints(self,f):
		for point in  self.points:
			self.drawpoint(f,point[0],point[1],point[2])


	def drawpaths(self, f, paths):
		for path in paths:
			#print path
			self.drawPolyline(f,path[:-1], strokeColor = path[-1])

	#############################################
	# # # # # # Low level Map Drawing # # # # # # 
	#############################################
	def drawmap(self, f):
		f.write('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' % (self.center[0],self.center[1]))
		f.write('\t\tvar myOptions = {\n')				
		f.write('\t\t\tzoom: %d,\n' % (self.zoom))
		f.write('\t\t\tcenter: centerlatlng,\n')
		f.write('\t\t\tmapTypeId: google.maps.MapTypeId.%s\n' % (self.maptype))
		f.write('\t\t};\n')		#change ; to ,	-- bad idea
		f.write('\t\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')	#change ; to ,
		# new code from here #				#added for right click event #
		f.write('\t\tvar marker = new google.maps.Marker({\n')
		f.write('\t\t\tmap: map,\n')
		f.write('\t\t});\n')
		f.write('\t\tvar infowindow = new google.maps.InfoWindow;\n')
		f.write('\t\tmap.addListener("rightclick", function(e){\n')		
		#f.write('\t\t\tmap.setCenter(e.latLng);\n')				#can be unmarked if you want to point the screen center to point right click
		f.write('\t\t\tmarker.setPosition(e.latLng);\n')
		f.write('\t\t\tinfowindow.setContent("Latitude: " + e.latLng.lat() + "<br>" + "Longitude: " + e.latLng.lng());\n')
		f.write('\t\t\tinfowindow.open(map, marker);\n')
		f.write('\t\t});\n')
		# till here #
		#f.write('\t\tmap.setTilt(45);\n')
		f.write('\n')



	def drawpoint(self,f,lat,lon,color):
		f.write('\t\tvar latlng = new google.maps.LatLng(%f, %f);\n'%(lat,lon))
		#f.write('\t\tvar img = new google.maps.MarkerImage(\'%s\');\n' % (self.coloricon.replace('XXXXXX',color)))
		f.write('\t\tvar img = new google.maps.MarkerImage(\'%s\');\n' % (self.coloricon))#(self.coloricon.replace('XXXXXX',color)))
		f.write('\t\tvar marker = new google.maps.Marker({\n')
		f.write('\t\ttitle: "no implimentation",\n')
		f.write('\t\ticon: img,\n')
		f.write('\t\tposition: latlng\n')
		f.write('\t\t});\n')
		f.write('\t\tmarker.setMap(map);\n')
		f.write('\n')
		
	def drawPolyline(self,f,path,\
			clickable = False, \
			geodesic = True,\
			strokeColor = "#FF0000",\
			strokeOpacity = 1.0,\
			strokeWeight = 2
			):
		f.write('var PolylineCoordinates = [\n')
		for coordinate in path:
			f.write('new google.maps.LatLng(%f, %f),\n' % (coordinate[0],coordinate[1]))
		f.write('];\n')
		f.write('\n')

		f.write('var Path = new google.maps.Polyline({\n')
		f.write('clickable: %s,\n' % (str(clickable).lower()))
		f.write('geodesic: %s,\n' % (str(geodesic).lower()))
		f.write('path: PolylineCoordinates,\n')
		f.write('strokeColor: "%s",\n' %(strokeColor))
		f.write('strokeOpacity: %f,\n' % (strokeOpacity))
		f.write('strokeWeight: %d\n' % (strokeWeight))
		f.write('});\n')
		f.write('\n')
		f.write('Path.setMap(map);\n')
		f.write('\n\n')


if __name__ == "__main__":
	mymap = pygmaps(37.428, -122.145, 16)
	mymap.addpoint(37.427, -122.145, "#0000FF")
	path = [(37.429, -122.145),(37.428, -122.145),(37.427, -122.145),(37.427, -122.146),(37.427, -122.146)]
	mymap.draw('./mymap.html')
