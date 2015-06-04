import os, os.path
import numpy as np
from osgeo import gdal
from osgeo import gdal_array
from osgeo import osr
import matplotlib.pylab as plt
from mpi4py import MPI
import subprocess as sp
import sys


ndviDir = "/home/vinay/Desktop/wbproj/ndvi"

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


qlist = [name for name in os.listdir(ndviDir) if os.path.isdir(os.path.join(ndviDir, name)) ]
		
c = rank
while c < len(qlist):

	yearDir = qlist[c]
	flag = 0
	geotransform = None
	#myarray = None
	arr = []
	for subroot,subdirs,subfiles in os.walk(yearDir):
		for file in subfiles:
			if file.endswith(".tif"):
				ds = gdal.Open(subroot+"/"+file)
				myarray = np.array(ds.GetRasterBand(1).ReadAsArray())
				arr.append(myarray)

				if (flag == 0):
					#DS = gdal.Open(subroot+"/"+file)
					#array = np.array(DS.GetRasterBand(1).ReadAsArray())
					nrows,ncols = np.shape(myarray)
					geotransform = ds.GetGeoTransform()
					flag = 1
		
		ndviarr= np.dstack(arr)
		ndvivalue = []
		for row in range(0,len(ndviarr)):
			ndvivalue.append([])
			for cell in range(0,len(ndviarr[row])):
				ndvivalue[row].append(np.max(ndviarr[row][cell]))

		#print len(myarray[0])
		#print len(ndvivalue[0])
		if geotransform != None:
			output_raster = gdal.GetDriverByName('GTiff').Create('/home/vinay/Desktop/wbproj/output_'+ dirs +'.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  
			output_raster.SetGeoTransform(geotransform)  
			srs = osr.SpatialReference()                 
			srs.ImportFromEPSG(4326)  
			output_raster.SetProjection(srs.ExportToWkt()) 
			output_raster.GetRasterBand(1).WriteArray(np.array(np.array(ndvivalue))

	c += size
comm.Barrier()
