import http.client, urllib.request, urllib.parse, urllib.error, base64 , json

# call azure ocr service
# pass image url to azure.

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '',
}

params = urllib.parse.urlencode({
    # Request parameters
    'language': 'zh-Hant',
    'detectOrientation': 'true',
    'model-version': 'latest',
})

body = {"url":"https://rachel-nutrition.com/wp-content/uploads/2019/11/infographic_nutritionlabel.jpg"}
json_data = json.dumps(body)

try:
    conn = http.client.HTTPSConnection('')
    conn.request("POST", "/vision/v3.2/ocr?%s" % params, json_data , headers)
    response = conn.getresponse()
    data = response.read()
    ocr_result = json.loads(data)
    print(ocr_result["language"])
    conn.close()

    aLine = ""
    for region in ocr_result['regions']:
        for line in region['lines']:
            aLine = ""
            for txt in line['words']:
                aLine += txt["text"]
            print(aLine)


except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))



