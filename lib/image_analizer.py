import http.client, urllib.request, urllib.parse, urllib.error, base64, json
def analyze(img):
    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '964ad916f8fa43a6a46d10fa7d6aec28'
    
    uri_base = 'westcentralus.api.cognitive.microsoft.com'
    
    headers = {
        # Request headers.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
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
        print('Error:')
        print(e)
        return []
    