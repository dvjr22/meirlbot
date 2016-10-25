############################################################
#                       Meme Creator                       #
# Creator: Tyler Moon                                      #
# Contributors:                                            #
# Purpose: This script takes in an image, a string for the #
# top text, and a string for the bottom text. Out of these #
# three things a simple meme is generate and saved to the  #
# createdMemes directory                                   #
############################################################

# These PIL libraries are the Python Image Library which allows for the
# image manipulation
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# MongoDb database
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['meirlbot_mongodb']
rposts = db.redditposts

import sys

# This method creates the meme :)
def make_meme(topString, bottomString, filename):
	# Open the image and get its size
	img = Image.open(filename)
	imageSize = img.size

	# find biggest font size that works
	fontSize = int(imageSize[1]/4)
	# Use the Impact font because its the best font
	font = ImageFont.truetype("/Library/Fonts/Impact.ttf", fontSize)
	topTextSize = font.getsize(topString)
	bottomTextSize = font.getsize(bottomString)
	while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
		fontSize = fontSize - 1
		font = ImageFont.truetype("/Library/Fonts/Impact.ttf", fontSize)
		topTextSize = font.getsize(topString)
		bottomTextSize = font.getsize(bottomString)

	# find top centered position for top text
	topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
	topTextPositionY = 0
	topTextPosition = (topTextPositionX, topTextPositionY)

	# find bottom centered position for bottom text
	bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
	bottomTextPositionY = imageSize[1] - bottomTextSize[1]
	bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)

	# Draw the image with the text on it
	draw = ImageDraw.Draw(img)

	# draw outlines
	# there may be a better way
	outlineRange = int(fontSize/15)
	for x in range(-outlineRange, outlineRange+1):
		for y in range(-outlineRange, outlineRange+1):
			draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=font)
			draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=font)

	draw.text(topTextPosition, topString, (255,255,255), font=font)
	draw.text(bottomTextPosition, bottomString, (255,255,255), font=font)

	# Save the image
	img.save(str("createdMemes/" + "meme_" + filename.replace('createdMemes/','')))

def get_upper(somedata):

	# Handle Python 2/3 differences in argv encoding
	result = ''
	try:
		result = somedata.decode("utf-8").upper()
	except:
		result = somedata.upper()
	return result

def get_lower(somedata):

	# Handle Python 2/3 differences in argv encoding
	result = ''
	try:
		result = somedata.decode("utf-8").lower()
	except:
		result = somedata.lower()

	return result



if __name__ == '__main__':
	for current in rposts.find():
		if current['updateFlag'] and current['createdMemeFlag']:
			print 'creating a meme'
			text = current['captionText']
			filename = current['createdMemeFile']
			topString, bottomString = text[:len(text)/2], text[len(text)/2:]
			make_meme(topString, bottomString, filename)
