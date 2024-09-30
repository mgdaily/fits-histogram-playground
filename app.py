import os
import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from astropy.io import fits
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from fits2image.conversions import fits_to_img

app = Flask(__name__)
CORS(app)

IMAGE_PATHS = {'R': {'FITS': 'data/ogg2m001-ep02-20240813-0051-e91.fits.fz'},
               'G': {'FITS': 'data/ogg2m001-ep04-20240813-0050-e91.fits.fz'},
               'B': {'FITS': 'data/ogg2m001-ep03-20240813-0050-e91.fits.fz'}}

OUTPUT_PATH = './rgb_image.jpg'


@app.route('/raw_data', methods=['POST'])
def get_raw_data():
    filter_arg = request.json.get('filter')
    fits_path = IMAGE_PATHS[filter_arg]['FITS']

    image_data = fits.open(fits_path)['SCI'].data

    # resize the image to max. 500 pixels on an axis
    max_size = 800
    image = Image.fromarray(image_data)
    image.thumbnail((max_size, max_size), Image.LANCZOS)
    scaled_array = np.asarray(image).astype(np.float16)
    scaled_array_flipped = np.flip(scaled_array, axis=0)

    return jsonify({'data': scaled_array_flipped.flatten().tolist(),
                    'height': scaled_array.shape[0],
                    'width': scaled_array.shape[1]})

@app.route('/rgb', methods=['POST'])
def scale_data():
    limits_r = request.json.get('limits_r')
    limits_g = request.json.get('limits_g')
    limits_b = request.json.get('limits_b')

    print(limits_r, limits_g, limits_b)

    fits_paths = [IMAGE_PATHS[filter]['FITS'] for filter in IMAGE_PATHS.keys()]

    fits_to_img(fits_paths, OUTPUT_PATH, file_type='jpeg', color=True,
                zmin=[limits_r[0], limits_g[0], limits_b[0]],
                zmax=[limits_r[1], limits_g[1], limits_b[1]], width=1000, height=1000)
    return jsonify({'path': OUTPUT_PATH})



if __name__ == '__main__':
    app.run(debug=True)
