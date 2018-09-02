# getImageData.py
# Author: Stefan Heincke
# Created: August 25, 2018
# Reads an image of any type, resizes to 100x100, outputs as a BMP
# and as an array of RGB values (0-255), for output to an LED strip.
# Code adapted from https://stackoverflow.com/questions/46385999/transform-an-image-to-a-bitmap
#
# VERSION HISTORY
# Ver 1.0: [Aug 25, 2018]
# Basic functionality, hardcoded input filename
# 
# Ver 1.1: [Aug 26, 2018]
# Added a CLI progress bar (code from StackOverflow, https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console)
#
# Ver 1.2: [Sep 2, 2018]
# Added user input for image name/type


#from __future__ import print_function
import os, sys
from PIL import Image
import numpy as np

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

# 
# Sample Usage
# 

#from time import sleep

# A List of Items
#items = list(range(0, 57))
#l = len(items)

# Initial call to print 0% progress
#printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
#for i, item in enumerate(items):
    # Do stuff...
#    sleep(0.1)
    # Update Progress Bar
#    printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)

# Get User Input
print("Time to get some image data!")
FN = input("\nWhat is the image filename? ")
extInput = input("\nWhat type of image is it? (J)PG, (P)NG, (B)MP? ")

if (extInput == "J") or (extInput == "j"):
	ext = '.jpg'
elif (extInput == "P") or (extInput == "p"):
	ext = '.png'
elif (extInput == "B") or (extInput == "b"):
	ext = '.bmp'
else:
	print("Sorry, that is invalid")

# Open up image, get bits
#FN  = 'RandM' # Filename
img = Image.open(FN + ext) # Open image #Originally Image.open(FN + '.jpg')
size = (100, 100) # Choose size
res = img.resize(size) # Resizes to 100x100
pixels = list(res.getdata()) # create a list of pixels (for Bitmap creation)
ary = np.array(res) # Convert to array of pixel data (for raw data)

# create a image and put data into it
newImg = Image.new(res.mode, res.size) # mode=RGB, size=100x100 (defined above)
newImg.putdata(pixels) # dump pixel data into newImg)
newImg.save(FN + '.bmp') # write BMP file

# split channels
r,g,b = np.split(ary,3,axis=2) # Split array into separate RGB values
r=r.reshape(-1) # Reshape to 1D array
g=g.reshape(-1)
b=b.reshape(-1)
#print(ary[0,0])
#print(r[0])
#print("Red is " + str(len(r)) + " long")
#print(g[0])
#print("Grn is " + str(len(g)) + " long")
#print(b[0])
#print("Blu is " + str(len(b)) + " long")

# Write raw data to file

f = open(FN + "_Array.txt",'w') # open file in write mode
f.write("{") # Initial curly brace, since this goes into a C file later
#for yy in range(0,100):
#	for xx in range(0,100):
#		#pixOut = [str(r[xx,yy]), str(g[xx,yy]), str(b[xx,yy])]
#		#print(str(pixOut))
#		#f.write(str(pixOut) + ' , ')
#		f.write("(" + str(red) + ", " + str(grn) + ", " + str(blu) + ")" + " , ")
#	f.write(";\n")
xx = 0; # X pixel counter
yy = 0; # Y pixel counter

for ii in range(0,len(r)):
	red = str(r[ii]) # Get current Red value
	grn = str(g[ii]) # Get current Green value
	blu = str(b[ii]) # Get current Blue value
	f.write("{" + red + ", " + grn + ", " + blu + "}") # Write current RGB value in braces
	xx += 1 # Increment X counter
	#print("X = " + str(xx))
	if xx == 100: # once we hit the end of the 100 px line...
		yy += 1 # Increment y counter
		printProgressBar(yy + 1, 101, prefix = 'Getting Bits:', suffix = 'Complete', length = 100)
		if yy == 100: # Check the end of the array
			f.write("};") # At the very end of the image
		else:
			f.write("},{") # At 100 X pixels, create a new line for readability
		xx = 0
		#print("Y = " + str(yy))
	else:
		f.write(", ") # Else, if in the middle of the array, just add a comma
#	if (yy < 100) and (yy >= 0): # Print the progress bar
#		printProgressBar(yy + 1, 100, prefix = 'Getting Bits:', suffix = 'Complete', length = 100)
	
		
#	if (yy % 100 == 0) and (yy != 0):
#		f.write("}")
#		f.write("\n")
	#elif yy % 100 != 0:
		
#	if (ii % 100 == 0) and (ii != 0):
#		f.write("}\n{")
	
f.close() # Close file.

print("All Done! Now grab that list of RGB data and make an image.")
