import sys
import subprocess
sys.path.append('scripts/')
import gdal_merge
import zipfile  
import os
import fnmatch
import time
import readline, glob
# from pyreadline import Readline
from pathlib import Path

# readline = Readline()

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def generate_geotiffs(inputProductPath, outputPath):

	basename =  os.path.basename(inputProductPath)
	if os.path.isdir(outputPath + basename[:-3] + "SAFE") :
		print('Already extracted')
	else:
		zip = zipfile.ZipFile(inputProductPath) 
		zip.extractall(outputPath) 
		print("Extracting Done") 

	
	directoryName = outputPath + basename[:-3] + "SAFE/GRANULE"

	productName = os.path.basename(inputProductPath)[:-4]
	outputPathSubdirectory = outputPath + productName + "_PROCESSED"

	if not os.path.exists(outputPathSubdirectory):
		os.makedirs(outputPathSubdirectory)

	subDirectorys = get_immediate_subdirectories(directoryName)

	results = []

	for granule in subDirectorys:
		unprocessedBandPath = outputPath + productName + ".SAFE/GRANULE/" + granule + "/" + "IMG_DATA/"
		results.append(generate_all_bands(unprocessedBandPath, granule, outputPathSubdirectory))
	
	#gdal_merge.py -n 0 -a_nodata 0 -of GTiff -o /home/daire/Desktop/merged.tif /home/daire/Desktop/aa.tif /home/daire/Desktop/rgbTiff-16Bit-AllBands.tif
	merged = outputPathSubdirectory + "/merged.tif"
	params = ['',"-of", "GTiff", "-o", merged]

	for granule in results:
		params.append(granule)

	gdal_merge.main(params)


def generate_all_bands(unprocessedBandPath, granule, outputPathSubdirectory):

	granuleBandTemplate =  granule[:-6]

	outputPathSubdirectory = outputPathSubdirectory 
	if not os.path.exists(outputPathSubdirectory+ "/IMAGE_DATA"):
		os.makedirs(outputPathSubdirectory+ "/IMAGE_DATA")
	
	outPutTiff = '/'+granule[:-6]+'16Bit-AllBands.tif'
	outPutVRT = '/'+granule[:-6]+'16Bit-AllBands.vrt'

	outPutFullPath = outputPathSubdirectory + "/IMAGE_DATA/" + outPutTiff
	outPutFullVrt = outputPathSubdirectory + "/IMAGE_DATA/" + outPutVRT
	
	

	for file_name in os.listdir(unprocessedBandPath):
		if fnmatch.fnmatch(file_name, '*.jp2'):
			numbers = file_name[16:22]
			break

	inputPath = unprocessedBandPath + granuleBandTemplate[4:11] + granuleBandTemplate[19:] + numbers

	bands = {
	"band_02" :  inputPath + "_B02.jp2",
	"band_03" :  inputPath + "_B03.jp2",
	"band_04" :  inputPath + "_B04.jp2",
	"band_08" :  inputPath + "_B08.jp2",
	"band_11" :  inputPath + "_B11.jp2",
	}


	cmd = ['gdalbuildvrt', '-resolution', 'user', '-tr' ,'20', '20', '-separate' ,outPutFullVrt]


	for band in sorted(bands.values()):
		cmd.append(band)
           
	my_file = Path(outPutFullVrt)
	if not my_file.is_file():
		# file exists
		subprocess.call(cmd)

	#, '-a_srs', 'EPSG:3857'
	cmd = ['gdal_translate', '-of' ,'GTiff', outPutFullVrt, outPutFullPath]

	my_file = Path(outPutTiff)
	if not my_file.is_file():
		# file exists
		subprocess.call(cmd)



	#params = ['', '-o', outPutFullPath, '-separate', band_01, band_02, band_03, band_04, band_05, band_06, band_07, band_08, band_8A, band_09, band_10, band_11, band_12]

	#gdal_merge.main(params)
	
	return(outPutFullPath)




outputPath = 'output/'
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)
inputPath = input("Input Path? ")
# inputPath = '/home/vinicius/projects/Sentinel-Scripts/Sentinel 2/inputs/'

start_time = time.time()

for file_name in os.listdir(inputPath):
	if fnmatch.fnmatch(file_name, '*.zip'):
		generate_geotiffs(inputPath + file_name, outputPath)

print("--- %s seconds ---" % (time.time() - start_time))
