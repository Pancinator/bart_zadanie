import datetime
import os
import urllib
import shutil

from .serializers import GallerySerializerPostRead
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from PIL import Image as I


@api_view(['GET'])  # function based decorator -> allows only usage of GET method
def api_overview(request):
    api_urls = {
        'List of galleries': 'api/gallery/',
        'List of images gallery': 'api/gallery/<name>',
        'View the picture': 'api/images/<gallery>/<path>'
    }
    return Response(api_urls)


# get list of galleries or create new one
@api_view(['GET', 'POST'])
def galleries(request):
    fs = FileSystemStorage()

    # GET request
    if request.method == 'GET':
        response_data = {}
        galleries = []

        for g in fs.listdir('')[0]:
            # Check for title image
            if len(fs.listdir(g)[1]) > 0:
                i = fs.listdir(g)[1][0]
                gallery = {
                    "name": urllib.parse.unquote(g),
                    "path": g,
                     "image": {
                        "path": i,
                        "fullpath": g + '/' + i,
                        "name": i.split('.')[0],
                        "modified": str(datetime.datetime.now()),
                    }
                }
            else:
                 gallery = {
                    "name": urllib.parse.unquote(g),
                    "path": g
                 }
            galleries.append(gallery)

        response_data['galleries'] = galleries
        return Response(response_data, status=status.HTTP_200_OK)

    # POST request
    elif request.method == 'POST':
        serializer = GallerySerializerPostRead(data=request.data)
        if serializer.is_valid():
            if fs.exists(urllib.parse.quote(serializer.data['name'])):
                return Response('Galéria so zadaným názvom už existuje.', status=status.HTTP_409_CONFLICT)
            else:
                os.mkdir("media/" + urllib.parse.quote(serializer.data['name']))
                content = {
                    "name": serializer.data['name'],
                    "path": urllib.parse.quote(serializer.data['name'])
                }
                return Response(content, status=status.HTTP_201_CREATED)
        else:
            bad_validation_response = {
                "code": 400,
                "payload": {
                    "paths": ["name"],
                    "validator": "required",
                    "example": None,
                },
                "name": "INVALID_SCHEMA",
                "description": "Bad JSON object: u'name' is a required property"
            }
            return Response(bad_validation_response,
                            status=status.HTTP_400_BAD_REQUEST)

# Methods for working with galleries content
@api_view(['GET', 'POST', 'DELETE'])
def gallery_detail(request, gallery):
    fs = FileSystemStorage()
    quoted_gallery_name = urllib.parse.quote(gallery)
    unquoted_gallery_name = urllib.parse.unquote(gallery)

    # GET request
    if request.method == 'GET':
        try:
            if fs.exists(quoted_gallery_name):
                response_data = {}
                images = []
                g = {
                    "path": quoted_gallery_name,
                    "name": unquoted_gallery_name
                }
                # Loop through directory and create JSON response
                for file in fs.listdir(quoted_gallery_name)[1]:
                    image = {
                        "path": file,
                        "fullpath": quoted_gallery_name + '/' + file,
                        "name": file.split('.')[0],
                        "modified": str(datetime.datetime.now()),
                    }
                    images.append(image)
                response_data['gallery'] = g
                response_data['images'] = images
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response('Zvolená galéria neexistuje', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response('Nedefinovaná chyba ' + str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST request
    elif request.method == 'POST':
        try:
            myfile = request.FILES['image']
        except Exception as e:
            return Response('Chybný request - nenašiel sa súbor pre upload. ' + str(e),
                            status=status.HTTP_400_BAD_REQUEST)
        if fs.exists(quoted_gallery_name):
            if not fs.exists(quoted_gallery_name + '/' + myfile.name):
                filename = fs.save(quoted_gallery_name + '/' + myfile.name, myfile)
                response = {
                    "uploaded": [{
                        "path": myfile.name,
                        "fullpath": fs.url(filename),
                        "name": myfile.name.split('.')[0],
                        "modified": str(datetime.datetime.now()),
                    }]
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response('Obrázok už existuje', status=status.HTTP_409_CONFLICT)
        else:
            return Response('Galéria pre upload sa nenašla', status=status.HTTP_404_NOT_FOUND)

    # DELETE request
    elif request.method == 'DELETE':
        try:
            if fs.exists(quoted_gallery_name):
                shutil.rmtree('media/' + quoted_gallery_name)
                return Response('Galéria/obrázok bola úspešne vymazaná', status=status.HTTP_200_OK)
            else:
                return Response('Zvolená galéria/obrázok neexistuje', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response('Nedefinovaná chyba ' + str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Methods for handling DELETE request of the specific image in specific gallery
@api_view(['DELETE'])
def delete_image_from_galery(request, gallery, image):
    quoted_gallery_name = urllib.parse.quote(gallery)

    if request.method == 'DELETE':
        try:
            fs = FileSystemStorage()
            if fs.exists(quoted_gallery_name + '/' + image):
                fs.delete(quoted_gallery_name + '/' + image)
                return Response('Galéria/obrázok bola úspešne vymazaná', status=status.HTTP_200_OK)
            else:
                return Response('Zvolená galéria/obrázok neexistuje', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response('Nedefinovaná chyba ' + str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Method for calculating a size ratio from origin image
def calculate_dimensions(w, h, i):
    if w == 0:
        s = i.size
        ratio = s[0] / s[1]
        w = round(h * ratio)
        return w, h
    elif h == 0:
        s = i.size
        ratio = s[0] / s[1]
        h = round(w * ratio)
        return w, h


# Method for generating image with specific size
# Method returns HttpResponse of imgae/jpeg type and object itself.
@api_view(['GET'])
def generate_image_view(request, w, h, image):
    # GET request
    quoted_path = urllib.parse.quote(image)

    if request.method == 'GET':
        try:
            i = I.open('media/' + quoted_path)
        except Exception as e:
            return Response('Obrázok sa nenašiel ' + str(e), status=status.HTTP_404_NOT_FOUND)
        try:
            if w == 0 or h == 0:
                w, h = calculate_dimensions(w, h, i)
            i.thumbnail((w,h))

            return HttpResponse(i, content_type="image/jpeg", status=status.HTTP_200_OK)
        except Exception as e:
            return Response('Nepodarilo sa spracovať obrázok a vygenerovať náhľad. ' + str(e),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


