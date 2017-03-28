import pygmaps1 as pg	#import library used to convert python code to javascript used in google maps
import difflib, sys	, csv , time	# to find difference in file if any
mymap = pg.pygmaps(41.979595,-87.90446417, 10,'ROADMAP')	#centerlatitude, ceneterlongitude, zoomlevel(higher value more zoom), Maptype (SATELLITE,ROADMAP,HYBRID,TERRAIN)

masterfile = 'C:\\Users\\naiti\\Desktop\\data.csv'
targetfile = 'C:\\Users\\naiti\\Desktop\\data1.csv'
tempfile = 'C:\\Users\\naiti\\Desktop\\data-temp.csv'

### delete the content of fName passed
def deleteContent(fName):
    with open(fName, "w"):
        pass

### function will check the difference between master and target file
### if difference found then write into temp file for map point.
def checkfilediff():
	deleteContent(tempfile)
	with open(masterfile, "r") as f1, open(targetfile, "r") as f2 , open(tempfile, "w") as csvoutput:
		writer = csv.writer(csvoutput)
		diff = difflib.ndiff(f1.readlines(),f2.readlines())
		type(diff)
		tmpdata = []
		i=0
		for line in diff:
			if line.startswith('-'):
				#line.replace("\n",'')
				temp,hum,alt,lat,lon = line.split(',')
				lon=lon.replace("\n",'')
				tmpdata.append((temp[2:],hum,alt,lat,lon))
			elif line.startswith('+'):
				continue
		while i != len(tmpdata):
			writer.writerow(tmpdata[i])
			i=i+1
	print("File difference checked and temp file created")
	f1.close()
	f2.close()
	csvoutput.close()
	return 1

### when points plot then append temp file data into target file so as to next time compare with master it won't come
def appendDiffIntoFile():
	print("inside append file started\n")
	with open(targetfile, "a") as target, open(tempfile) as source:
		source = source.read().replace('\r\n', '\n')
		for reader in source:
			target.write(reader)
	target.close()
	#source.close()
	print("file append completed\n")

### to create map points and path
def createinmap(file):
	#files = 'C:\\Users\\naiti\\Desktop\\%s.csv' %file
	print("\nenter into map creation\n")
	rslt = []
	with open(file) as csvfile:	#open any file which have raw data from sensors
		#next(csvfile)		#for header file avoid
		for reader in csvfile:		#every record in csv file
			ext = reader.split(",")		#create a list from string separated by comma
			temp = ext[0]				#extract temperature data from 1st position
			hum = ext[1]				#extract humidity information from 2nd position
			alt = ext[2]				#extract altitude information from 3rd position
			lat1 = ext[3]				#extract latitude from 4th position
			long1 = ext[4]				#extract longitude from 5th position
			rslt.append((float(lat1),float(long1)))		#add longlat into tuple of list
		#	mymap.addpoint(float(lat1),float(long1),'#0000FF')		#to add point on map # original
			mymap.addpoint(float(lat1), float(long1), float(temp), float(hum), float(alt), '#0000FF')		#to add point on map
	csvfile.close()
	mymap.addpath(rslt,'#00FF00')		#with all points in rslt[] create poly line between them
	mymap.draw('./mymap.html')			#draw html with name and path given
	print("map has been created\n")

if __name__ == "__main__":
	try:
		while True:
			if checkfilediff():
				createinmap(tempfile)
				appendDiffIntoFile()
				time.sleep(5)
	except KeyboardInterrupt:
		pass
