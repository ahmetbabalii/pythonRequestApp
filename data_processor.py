import pandas as pd
from utils import logger

class RequestData:
    def __init__(self, request):
        if request is None: 
            return
            
        try:
            request_items = request.items()
        except (ValueError, AttributeError):
            request_items = []
            
        for key, value in request_items:
            setattr(self, key, value)

class ResponseData:
    def __init__(self, response):
        self.status_code = response.status_code
        
        try:
            response_items = response.json().items()
        except (ValueError, AttributeError):
            response_items = []
            
        for key, value in response_items:
            setattr(self, key, value)

class RequestAndResponseData:
    def __init__(self, request, response, endpoint):
        self.request = RequestData(request)
        self.response = ResponseData(response)
        self.endpoint = endpoint
        self.statusCode = response.status_code

def export_data_to_excel(data_list, filename, app_name):
    try:
        if not data_list:
            logger.warning(f"{app_name} için veri bulunamadı, Excel dosyası oluşturulmadı.")
            return False
            
        data = []
        for item in data_list:
            request_dict = vars(item.request)
            response_dict = vars(item.response)
            endpoint = item.endpoint
            
            request_params = ' || '.join([f"{key}: {value}" for key, value in request_dict.items() if key != ''])
            response_params = ' || '.join([f"{key}: {value}" for key, value in response_dict.items() if key != 'status_code'])
            
            data.append([item.statusCode, request_params, response_params, endpoint])
        
        df = pd.DataFrame(data, columns=['StatusCode', 'RequestParameters', 'ResponseParameters', 'EndPoint'])
        df.to_excel(f'{app_name}.xlsx', index=False)
        
        logger.info(f"{app_name} için veriler başarıyla Excel dosyasına kaydedildi.")
        return True
        
    except Exception as e:
        logger.error(f"Excel'e veri aktarma hatası: {str(e)}")
        return False