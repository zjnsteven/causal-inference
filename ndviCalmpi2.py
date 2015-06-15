from mpi4py import MPI
import os, os.path
import numpy as np
from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr
#import matplotlib.pylab as plt

#import subprocess as sp
#import sys
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

#ndviDir = "/sciclone/home00/zjn/wbproj/ndvimpi/ndvi"

<<<<<<< HEAD
ndviDir = "/sciclone/aiddata10/REU/data/ltdr.nascom.nasa.gov/allData/Ver4/ndvi"
=======
ndviDir = "/sciclone/data20/aiddata/REU/data/ltdr.nascom.nasa.gov/allData/Ver4/ndvi"
>>>>>>> origin/master
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
status = MPI.Status()
tags = enum('READY', 'DONE', 'EXIT', 'START')


<<<<<<< HEAD
ignore = ['1981']

#accept = ['1981']

qlist = [name for name in os.listdir(ndviDir) if os.path.isdir(os.path.join(ndviDir, name)) and not name in ignore]
=======

#accept = []

qlist = [name for name in os.listdir(ndviDir) if os.path.isdir(os.path.join(ndviDir, name))]
>>>>>>> origin/master
		

for i in range(len(qlist)): 
	yearDir = qlist[i]
	filelist = [ndviDir + "/" + yearDir + "/" + name for name in os.listdir(ndviDir + "/" + yearDir) if not os.path.isdir(os.path.join(ndviDir+"/" + yearDir ,name)) ]
	print yearDir
 	if rank ==0:
 		geotransform = None
 		tmp = gdal.Open(filelist[1])
		testarray = np.array(tmp.GetRasterBand(1).ReadAsArray())
		nrows,ncols = np.shape(testarray)
		geotransform = tmp.GetGeoTransform()

		result=[]
 		tasks = filelist
 		task_index = 0
 		num_workers = size - 1
 		closed_workers = 0
 		print("Master starting with %d workers" % num_workers)
 		while closed_workers < num_workers:
 			data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
 			source = status.Get_source()
 			tag = status.Get_tag()
 			if tag == tags.READY:
 				if task_index < len(tasks):
 					comm.send(tasks[task_index], dest=source, tag=tags.START)
 					print("Sending task %d to worker %d" % (task_index, source))
					task_index += 1

				else:
					comm.send(None, dest=source, tag=tags.EXIT)

			elif tag == tags.DONE:
				result.append(data)
				print("Got data from worker %d" % source)

			elif tag == tags.EXIT:
				print("Worker %d exited." % source)
				closed_workers +=1

		ndviarr= np.dstack(result)
		ndvivalue = []
		for row in range(0,len(ndviarr)):
			ndvivalue.append([])
			for cell in range(0,len(ndviarr[row])):
				ndvivalue[row].append(np.max(ndviarr[row][cell]))

		
		if geotransform != None:
			output_raster = gdal.GetDriverByName('GTiff').Create('/sciclone/home00/zjn/wbproj/ndvimpi/output/ndvi_max/'+ yearDir+'.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  
			output_raster.SetGeoTransform(geotransform)  
			srs = osr.SpatialReference()                 
			srs.ImportFromEPSG(4326)  
			output_raster.SetProjection(srs.ExportToWkt()) 
			output_raster.GetRasterBand(1).SetNoDataValue(-9999)
			output_raster.GetRasterBand(1).WriteArray(np.array(ndvivalue))

	else:
		name = MPI.Get_processor_name()
		print("I am a worker with rank %d on %s." % (rank, name))
		while True:
			comm.send(None,dest=0,tag=tags.READY)
			task = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
			tag = status.Get_tag()

			if tag == tags.START:
				ds = gdal.Open(task)
				myarray = np.array(ds.GetRasterBand(1).ReadAsArray())
				comm.send(myarray, dest=0, tag=tags.DONE)

			if tag == tags.EXIT:
				comm.send(None, dest=0, tag=tags.EXIT)
				break

		#comm.send(None, dest=0, tag=tags.EXIT)

			# if (flag == 0):
			# 	#DS = gdal.Open(subroot+"/"+file)
			# 	#array = np.array(DS.GetRasterBand(1).ReadAsArray())
			# 	nrows,ncols = np.shape(myarray)
			# 	geotransform = ds.GetGeoTransform()
			# 	flag = 1
		
	
		
			



