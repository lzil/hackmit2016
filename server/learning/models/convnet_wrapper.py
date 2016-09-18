import os

import texture_class

def getScore(adjective, image):
	base_path = '../../cache/models/'
	if not os.path.isfile(base_path+adjective+'.pkl'):
		# PULL A FOLDER OF IMAGES that have been downloaded. maybe we could make do with the URL.
		# But they need to be turned into thumbnails too
		res = texture_class.train_images(folder, adjective)
	# INSERT PROCESSING HERE to turn image into a thumbnail
	return texture_class.predict_image(base_path+adjective+'.pkl', image)