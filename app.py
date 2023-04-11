import numpy as np
import gradio as gr
from PIL import Image
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import json


def sepia(input_img):
    answer = imageToText(input_img)
    return answer


def imageToText(input_img):
    returnTxt = ""
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '${{AZURE_COMPUTER_VISION_API_KEY}}',
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'language': 'zh-Hant',
        'detectOrientation': 'true',
        'model-version': 'latest',
    })
    image_data = open(input_img,"rb").read()
    conn = http.client.HTTPSConnection(
        '${{AZURE_COMPUTER_VISION_END_POINT}}')
    conn.request("POST", "/vision/v3.2/ocr?%s" % params, image_data , headers)
    response = conn.getresponse()
    data = response.read()
    ocr_result = json.loads(data)
    conn.close()

    aLine = ""
    for region in ocr_result['regions']:
        for line in region['lines']:
            aLine = ""
            for txt in line['words']:
                aLine += txt["text"]
            returnTxt += (aLine + "\r\n")
    return returnTxt


demo = gr.Interface(
    fn=sepia,
    inputs=gr.Image(shape=(400, 400), type="filepath"),
    outputs="text")
demo.launch()
