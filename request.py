import pandas as pd
import requests
import json
from concurrent.futures import ThreadPoolExecutor

def check_none(value):
    return '' if value is None else str(value)

class Veri:
    def __init__(self, dns, uygulamaadi, endpoint, postOrnek, requestType):
        self.dns = check_none(dns)
        self.uygulamaadi = check_none(uygulamaadi)
        self.endpoint = check_none(endpoint)
        self.postOrnek = check_none(postOrnek)
        self.requestType = check_none(requestType)
        
    def request(self):    
        print (f'{self.uygulamaadi} için istek gönderiliyor...')   
                   
        headers = {'Content-Type': 'application/json'}       
        data = json.loads('[' + self.postOrnek + ']') if self.postOrnek else None
        with ThreadPoolExecutor() as executor:
            if self.requestType == 'GET':
                requests_and_responses = list(executor.map(lambda item: (item, requests.get(self.endpoint, headers=headers)), [None]))
            elif self.requestType == 'POST':
                requests_and_responses = list(executor.map(lambda item: (item, requests.post(self.endpoint, headers=headers, json=item)), data))
            else :
                return None               

        return [RequestAndResponseData(request, response, self.endpoint) for request, response in requests_and_responses]
    
class ResponseData:
    def __init__(self, response):       
        self.status_code = response.status_code   
        
        try:
            response_items = response.json().items()
        except ValueError:
            response_items = []
            
        for key, value in response_items:           
            setattr(self, key, value)  
        
class RequestData:
    def __init__(self, request):    
        if request is None: return          
        try:
            request_items = request.items()
        except ValueError:
            request_items = []
            
        for key, value in request_items:           
            setattr(self, key, value)       
        
class RequestAndResponseData:
    def __init__(self, request, response, endpoint):  
        self.request = RequestData(request)            
        self.response = ResponseData(response)     
        self.endpoint = endpoint      
        self.statusCode = response.status_code               
                            
                            
df = pd.read_excel('datas.xlsx', engine='openpyxl')
veriler = [Veri(row['dns'], row['uygulamaadi'], row['endpoint'], row['postOrnek'] , row['requestType']) for index, row in df.iterrows()]

filtered_veriler = [veri for veri in veriler if veri.uygulamaadi ==  'uygulamaadı test'  ]

for veri in veriler:    
    results = veri.request()
    if results is None: continue
    
    data = []
    for item in results:
        
        request_dict = vars(item.request)
        response_dict = vars(item.response)    
        endPoint = item.endpoint
        
        requestParametersList = ' || '.join([f"{key}: {value}" for key, value in request_dict.items() if key != ''])
        responseParametersList = ' || '.join([f"{key}: {value}" for key, value in response_dict.items() if key != 'status_code'])  
        
        data.append([item.statusCode, requestParametersList, responseParametersList, endPoint])

    df = pd.DataFrame(data, columns=['StatusCode', 'RequestParameters', 'ResponseParameters', 'EndPoint'])
    df.to_excel(f'{veri.uygulamaadi}.xlsx', index=False)
    
    # with open(f'{veri.uygulamaadi}.txt', 'w') as f:  
    #     for item in results:
    #         request_dict = vars(item.request)
    #         reponse_dict = vars(item.response)    
    #         endPoint = item.endpoint
            
    #         reuqestParametersList = ' || '.join([f"{key}: {value}" for key, value in request_dict.items() if key != ''])
    #         responseParametersList = ' || '.join([f"{key}: {value}" for key, value in reponse_dict.items() if key != ''])  
            
    #         requestAndResponseSum = f'Request: {reuqestParametersList} >>> Response: {responseParametersList} >>> EndPoint: {endPoint}'
            
    #         f.write(requestAndResponseSum + '\n')
        
        
