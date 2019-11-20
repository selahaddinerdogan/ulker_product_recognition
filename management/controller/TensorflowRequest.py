from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import requests,  json, cv2, base64, os, time
from PIL import Image
import numpy as np

import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


class TensorflowRequest(APIView):

    @api_view(['GET', 'POST'])
    def model_request(self):
        produts = {
            2: {'name': 'Coco Star', 'short_name': 'cocostar', 'stock': False, 'image': '/product_image/cocostar.png'},
            3: {'name': 'Çikolatalı Gofret', 'short_name': 'ucg', 'stock': False, 'image': '/product_image/cikolatali_gofret.png'},
            5: {'name': 'Laviva', 'short_name': 'laviva', 'stock': False, 'image':'/product_image/laviva.png'},
            6: {'name': 'Metro Klasik', 'short_name': 'metro', 'stock': False, 'image':'/product_image/metro1.png'},
            14: {'name': 'Metro Büyük Boy', 'short_name': 'metro40', 'stock': False, 'image': '/product_image/metro40.png'},
            8: {'name': 'Albeni', 'short_name': 'albeni', 'stock': False, 'image':'/product_image/albeni.png'},
            15: {'name': 'Albeni Büyük Boy', 'short_name': 'albeni30', 'stock': False, 'image': '/product_image/albeni30.png'},
            4: {'name': 'Dido', 'short_name': 'dido', 'stock': False, 'image': '/product_image/dido.png'},
            1: {'name': 'Caramio Karamel Baton', 'short_name': 'caramio', 'stock': False, 'image': '/product_image/caramio.png'},
            7: {'name':  'Çokonat', 'short_name': 'cokonat', 'stock': False, 'image': '/product_image/cokonat.png'},
            10: {'name': 'Antep Fıstıklı Baton', 'short_name': 'fistik_baton', 'stock': False, 'image': '/product_image/butun_antep_fistikli.png'},
            11: {'name': 'Sütlü Baton', 'short_name': 'sutlu_baton', 'stock': False, 'image': '/product_image/sutlu_baton.png'},
            13: {'name': 'Antep Fıstıklı Kare', 'short_name': 'fistik_kare', 'stock': False, 'image': '/product_image/antep_fistikli_kare.png'},
            9: {'name': 'Antep Fıstıklı Bitter Kare', 'short_name': 'bitter_kare', 'stock': False, 'image': '/product_image/antep_fistikli_bitter_kare.png'},
            12: {'name': 'Sütlü Kare', 'short_name': 'sutlu_kare', 'stock': False, 'image': '/product_image/sutlu_kare.png'}

        }
        STANDARD_COLORS = [
            'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
            'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
            'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
            'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
            'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
            'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
            'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
            'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
            'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
            'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
            'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
            'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
            'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
            'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
            'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
            'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
            'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
            'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
            'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
            'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
            'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
            'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
            'WhiteSmoke', 'Yellow', 'YellowGreen'
        ]

        model_url = "http://localhost:8501/v1/models/ulker_model_base/versions/1:predict"

        file_name = str(time.time()).replace('.', '')
        imageb64 = self.data['image']
        images_dir = os.path.join(os.getcwd(), "management", "controller", "images")
        image_file_name = "{}.jpg".format(file_name)
        image_file_dir = os.path.join(images_dir, image_file_name)
        with open(os.path.join(image_file_dir), "wb") as fh:
            fh.write(base64.b64decode(imageb64))

        #image_encode = base64.b64encode(image).decode("utf-8")

        # resim uzerine cizdirme
        image = Image.open(image_file_dir)
        image_np_orj = TensorflowRequest.load_image_into_numpy_array(image)

        image_pil = Image.fromarray(np.uint8(image_np_orj)).convert('RGB')

        draw = ImageDraw.Draw(image_pil)  # s = requests.Session()

        body = {
            "signature_name": "serving_default",
            "instances": [{"inputs": {"b64": imageb64}}]
        }

        headers = {"content-type": "application/json"}
        r = requests.post(model_url, data=json.dumps(body), headers=headers, timeout=None)  # json.dumps(body)
        jsonData = r.json()

        threshold = 0.5

        produce = []

        #font = ImageFont.load_default()
        font_file_path = os.path.join(os.getcwd(), "management", "controller", "DoppioOne-Regular.ttf")
        font = ImageFont.truetype(font_file_path, 17)

        for score, category, bbox in zip(jsonData["predictions"][0]['detection_scores'],
                                         jsonData["predictions"][0]['detection_classes'],
                                         jsonData["predictions"][0]['detection_boxes']):

            if score >= threshold:
                json_data = produts[(int(category))]
                clas_name = json_data.get('short_name')
                produts[int(category)]['stock'] = True

                xmin = int(bbox[0] * image_np_orj.shape[0])
                ymin = int(bbox[1] * image_np_orj.shape[1])
                xmax = int(bbox[2] * image_np_orj.shape[0])
                ymax = int(bbox[3] * image_np_orj.shape[1])

                clas_name = clas_name + " %" + str(int(score * 100))
                (left, right, top, bottom) = (ymin, ymax, xmin, xmax)
                color = STANDARD_COLORS[int(category % len(STANDARD_COLORS))]
                draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=4,
                          fill=color)
                text_width, text_height = font.getsize(clas_name)
                margin = np.ceil(0.05 * text_height)
                # text_bottom =top #karenin ust kismina yazar
                text_bottom = bottom - 4  # karenin alt kismina yazar
                draw.rectangle([(ymin, text_bottom - text_height - 2 * margin), (left + text_width, text_bottom)],
                               fill='yellow')
                draw.text((left + margin, text_bottom - text_height - margin), clas_name, fill='black', font=font)
                # text_bottom -= text_height - 2 * margin
                #
                #

                produce.append({"id": category, "name": clas_name,
                                "bbox": [int(ymin), int(xmin), int(ymax), int(xmax)],
                                #                            "bbox":[bbox[0], bbox[1],bbox[2], bbox[3]],
                                "score": "{0:.2f}".format(score * 100)})

        np.copyto(image_np_orj, np.array(image_pil))
        image_np = cv2.cvtColor(image_np_orj, cv2.COLOR_BGR2RGB)
        cv2.imwrite(image_file_dir, image_np)

        return Response(
            {
            'image': image_file_name,
            'products': [produts[item] for item in produts]
            }
        )

    @staticmethod
    def load_image_into_numpy_array(image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

