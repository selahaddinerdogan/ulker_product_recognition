from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from django.http import HttpResponse

image_file_path = os.path.join(os.getcwd(), "management", "controller", "images")
image_product_file_path = os.path.join(os.getcwd(), "management", "controller", "images", "products")


class Image(APIView):

    @api_view(['GET'])
    def image(self,  file_name):
        request = self
        try:
            file_rename = os.path.join(image_file_path, file_name)
            if os.path.isfile(file_rename):
                image_data = open(file_rename, "rb").read()
                return HttpResponse(image_data, content_type="image/jpg")

        except IOError as ex:
            print("Hata :", ex)
            return HttpResponse(image_data, content_type="image/jpg")

    @api_view(['GET'])
    def product_image(self,  file_name):
        request = self
        try:
            file_rename = os.path.join(image_product_file_path, file_name)
            if os.path.isfile(file_rename):
                image_data = open(file_rename, "rb").read()
                return HttpResponse(image_data, content_type="image/jpg")

        except IOError as ex:
            print("Hata :", ex)
            return HttpResponse(image_data, content_type="image/jpg")
