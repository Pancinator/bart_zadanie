import datetime
import os
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
            gallery = {
                "path": g,
                "name": g.replace("%", " ")
            }
            galleries.append(gallery)
        response_data['galleries'] = galleries
        return Response(response_data, status=status.HTTP_200_OK)

    # POST request
    elif request.method == 'POST':
        try:
            gallery_name = request.data['name']
            if '/' in gallery_name:
                return Response('Chybne zadaný request - nevhodný obsah podľa schémy.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response('Chybne zadaný request - nevhodný obsah podľa schémy. ' + str(e),
                            status=status.HTTP_400_BAD_REQUEST)
        p = gallery_name.replace(" ", "%")
        if fs.exists(gallery_name):
            return Response('Galéria so zadaným názvom už existuje.', status=status.HTTP_409_CONFLICT)
        else:
            os.mkdir("media/" + p)
            content = {
                "name": gallery_name,
                "path": p
            }
            return Response(content, status=status.HTTP_201_CREATED)


# Methods for working with galleries content
@api_view(['GET', 'POST', 'DELETE'])
def gallery_detail(request, gallery):
    fs = FileSystemStorage()
    # GET request
    if request.method == 'GET':
        try:
            if fs.exists(gallery):
                response_data = {}
                images = []
                g = {
                    "path": gallery,
                    "name": gallery
                }
                # Loop through directory and create JSON response
                for file in fs.listdir(gallery)[1]:
                    image = {
                        "path": file,
                        "fullpath": gallery + '/' + file,
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
            myfile = request.FILES['myfile']
        except Exception as e:
            return Response('Chybný request - nenašiel sa súbor pre upload. ' + str(e),
                            status=status.HTTP_400_BAD_REQUEST)
        if fs.exists(gallery):
            filename = fs.save(gallery + '/' + myfile.name, myfile)
            response = {
                "uploaded": [{
                    "path": myfile.name,
                    "fullpath": fs.url(filename),
                    "name": myfile.name.split('.')[0],
                    "modified": str(datetime.datetime.now()),
                }]
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response('Galéria pre upload sa nenašla', status=status.HTTP_404_NOT_FOUND)

    # DELETE request
    elif request.method == 'DELETE':
        try:
            g = gallery.replace(" ", "%")
            if fs.exists(g):
                fs.delete(g)
                return Response('Galéria/obrázok bola úspešne vymazaná', status=status.HTTP_200_OK)
            else:
                return Response('Zvolená galéria/obrázok neexistuje', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response('Nedefinovaná chyba ' + str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Methods for handling DELETE request of the specific image in specific gallery
@api_view(['DELETE'])
def delete_image_from_galery(request, gallery, image):
    if request.method == 'DELETE':
        try:
            fs = FileSystemStorage()
            if fs.exists(gallery + '/' + image):
                fs.delete(gallery + '/' + image)
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
    if request.method == 'GET':
        try:
            i = I.open(image)
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


