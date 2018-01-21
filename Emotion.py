from __future__ import print_function
from flask import Flask
import time
import requests
import flask
import glob
import cv2


_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_key = "c5a4f8648bb54c01ab66735c934a9b2b"
_maxNumRetries = 10


def processRequest(json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result


def read_images_in_folder():
    image_stack = []
    for img in glob.glob('Images\*.jpg'): # All jpeg images
        with open(img,'rb') as f:
            data=f.read()
            image_stack.append(data)
    return image_stack


if __name__=="__main__":

    # Load raw image file into memory
    image_stack=[]
    '''pathToFileInDisk = r'C:\FindMissingPerson\Expressions\Angry1.jpg'
    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()'''
    read_images_in_folder()
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'
    resultLog={}
    scores={}
    json = None
    params = None
    i=0

    image_stack=read_images_in_folder()
    for data in image_stack:
        result = processRequest( json, data, headers, params )
        print(result)
        if result is not None:
                resultlog=result[0]
                scores=resultlog['scores']
                key_max = max(scores.keys(), key=(lambda k: scores[k]))
                print(scores[key_max],key_max)



