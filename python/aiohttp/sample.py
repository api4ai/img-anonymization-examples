#!/usr/bin/env python3

"""Example of using API4AI image anonymization API."""

import asyncio
import base64
import json
import os
import sys

import aiohttp


# Use 'demo' mode just to try api4ai for free. ⚠️ Free demo is rate limited and must not be used in real projects.
#
# Use 'normal' mode if you have an API Key from the API4AI Developer Portal. This is the method that users should normally prefer.
#
# Use 'rapidapi' if you want to try api4ai via RapidAPI marketplace.
# For more details visit:
#   https://rapidapi.com/api4ai-api4ai-default/api/image-anonymization/details
MODE = 'demo'

# Your API4AI key. Fill this variable with the proper value if you have one.
API4AI_KEY = ''

# Your RapidAPI key. Fill this variable with the proper value if you want
# to try api4ai via RapidAPI marketplace.
RAPIDAPI_KEY = ''


OPTIONS = {
    'demo': {
        'url': 'https://demo.api4ai.cloud/img-anonymization/v1/results'
    },
    'normal': {
        'url': 'https://api4ai.cloud/img-anonymization/v1/results',
        'headers': {'X-API-KEY': API4AI_KEY}
    },
    'rapidapi': {
        'url': 'https://image-anonymization.p.rapidapi.com/v1/results',
        'headers': {'X-RapidAPI-Key': RAPIDAPI_KEY}
    }
}


async def main():
    """Entry point."""
    image = sys.argv[1] if len(sys.argv) > 1 else 'https://static.api4.ai/samples/img-anonymization-0.jpg'

    async with aiohttp.ClientSession() as session:
        if '://' in image:
            # Data from image URL.
            data = {'url': image}
        else:
            # Data from local image file.
            data = {'image': open(image, 'rb')}
        # Make request.
        async with session.post(OPTIONS[MODE]['url'],
                                data=data,
                                headers=OPTIONS[MODE].get('headers')) as response:
            resp_json = await response.json()

        image_format = resp_json['results'][0]['entities'][0]['format'].lower()
        img_b64 = resp_json['results'][0]['entities'][0]['image'].encode('utf8')

        path_to_image = os.path.join(f'result.{image_format}')
        with open(path_to_image, 'wb') as img:
            img.write(base64.decodebytes(img_b64))

        objects_pretty = json.dumps(resp_json['results'][0]['entities'][1]['objects'], indent=2)
        print(f'💬 Hidden objects:\n{objects_pretty}\n')

        print(f'💬 The "result.{image_format}" image is saved to the current directory.')


if __name__ == '__main__':
    # Run async function in asyncio loop.
    asyncio.run(main())
