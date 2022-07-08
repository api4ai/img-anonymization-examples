#!/usr/bin/env python3

"""Example of using API4AI image anonymization API."""

import base64
import json
import os
import sys

import requests


# Use 'demo' mode just to try api4ai for free. Free demo is rate limited.
# For more details visit:
#   https://api4.ai
#
# Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
# For more details visit:
#   https://rapidapi.com/api4ai-api4ai-default/api/image-anonymization/details
MODE = 'demo'


# Your RapidAPI key. Fill this variable with the proper value if you want
# to try api4ai via RapidAPI marketplace.
RAPIDAPI_KEY = ''


OPTIONS = {
    'demo': {
        'url': 'https://demo.api4ai.cloud/img-anonymization/v1/results',
        'headers': {'A4A-CLIENT-APP-ID': 'sample'}
    },
    'rapidapi': {
        'url': f'https://image-anonymization.p.rapidapi.com/v1/results',
        'headers': {'X-RapidAPI-Key': RAPIDAPI_KEY}
    }
}


if __name__ == '__main__':
    # Parse args.
    image = sys.argv[1] if len(sys.argv) > 1 else 'https://storage.googleapis.com/api4ai-static/samples/img-anonymization-0.jpg'

    if '://' in image:
        # POST image via URL.
        response = requests.post(
            OPTIONS[MODE]['url'],
            headers=OPTIONS[MODE]['headers'],
            data={'url': image})
    else:
        # POST image as file.
        with open(image, 'rb') as image_file:
            response = requests.post(
                OPTIONS[MODE]['url'],
                headers=OPTIONS[MODE]['headers'],
                files={'image': (os.path.basename(image), image_file)}
            )

    response_entities = response.json()['results'][0]['entities']
    image_format = response_entities[0]['format'].lower()
    img_b64 = response_entities[0]['image'].encode('utf8')

    path_to_image = os.path.join(f'result.{image_format}')
    with open(path_to_image, 'wb') as img:
        img.write(base64.decodebytes(img_b64))

    objects_pretty = json.dumps(response_entities[1]["objects"], indent=2)
    print(f'💬 Hidden objects:\n{objects_pretty}\n')

    print(f'💬 The "result.{image_format}" image is saved to the current directory.')
