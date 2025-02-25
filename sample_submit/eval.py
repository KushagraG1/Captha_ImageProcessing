import predict
import time as tm
import numpy as np
import re
import os
import glob
import cv2 as cv
import numpy as np
from PIL import Image
import os
from os import listdir
import imutils
from matplotlib import pyplot as plt
# If there are 100 test points and predict.py returns 110 predictions
# then we only consider the first 100 and discard the last 10 predictions.
# On the other hand, if predict.py returns only 90 predictions, then we
# assume that these were predictions on the first 90 test points and
# assume that the predictions on the last 10 points was wrong by default.

def getCodeMatchScore( pred_labels, gold_labels ):
	totScore = 0
	for i in range( min( len( pred_labels ), len( gold_labels ) ) ):
		# Convert to upper case as a helpful gesture to avoid trivial mismatches
		pred = process( pred_labels[ i ].upper() )
		gold = process( gold_labels[ i ] )

		print( f"Predicted label was processed to contain names {pred}" )

		subScore = 0

		for l in range( min( len( pred ), len( gold ) ) ):
			print( f"Comparing {pred[l]} with {gold[l]} ... ", end = '' )
			if pred[l] == gold[l]:
				subScore += 1
				print( "match" )
			else:
				print( "no match" )

		print( f"subScore is {subScore}" )
		totScore += subScore

	return totScore / ( 3 * len( gold_labels ) )

def process( label ):
	# Remove all characters that are not upper-case Latin alphabets or commas
	# Please take care to only output Greek letter names in upper case letters
	# Please also take care not to make spelling mistakes in the names
	# Please refer to the reference folder for correct names of all letters
	label = re.sub( r"[^A-Z,]+", '', label )

	# Split the names using comma as a separator
	names = label.split( ',' )

	# Keep only the first 3 names
	return names[:3]

numTest = 2
filepaths = [ f"test/{i}.png" for i in range( numTest ) ]

# Get labels from predict.py and time the thing
tic = tm.perf_counter()
pred_labels = predict.decaptcha( filepaths )
toc = tm.perf_counter()

with open( "test/codes.txt", 'r' ) as file:
	gold_labels = file.read().splitlines()

print( "Total time taken is %.6f seconds " % ( toc - tic ) )
print( "Code match score is %.6f" % ( getCodeMatchScore( pred_labels, gold_labels ) ) )
