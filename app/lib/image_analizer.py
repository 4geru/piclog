from app.lib.env import ENV
import http.client, urllib.request, urllib.parse, urllib.error, base64, json

class image_analizer:
    def __init__(img):
        self.search(img)
        
    def search(img):
        """ Azure Vision APIへリクエスト 
         >> img : string URL
         << english_words : list
        """    
        uri_base = 'westcentralus.api.cognitive.microsoft.com'
        
        headers = {
            # Request headers.
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': ENV('SUBSCRIPTION_KEY'),
        }
        
        params = urllib.parse.urlencode({
            'visualFeatures': 'Categories,Description,Color',
            'language': 'en',
        })
        
        body = "{'url':'" + img + "'}"
        try:
            conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
            conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
        
            parsed = json.loads(data)
            conn.close()
            return parsed['description']['tags']
        except Exception as e:
            print('Error:', end='')
            print(e)
            return []
        