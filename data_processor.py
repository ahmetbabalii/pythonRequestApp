"""
Veri işleme sınıfları ve fonksiyonları.
Bu modülde, istek ve yanıtların işlenmesi için gerekli sınıflar bulunur.
"""
import pandas as pd
from utils import logger

class RequestData:
    """
    HTTP isteği verilerini temsil eden sınıf.
    
    Attributes:
        Dinamik olarak eklenen nitelikler
    """
    def __init__(self, request):
        """
        RequestData sınıfı için yapılandırıcı.
        
        Args:
            request (dict): İstek verisi içeren sözlük
        """
        if request is None: 
            return
            
        try:
            request_items = request.items()
        except (ValueError, AttributeError):
            request_items = []
            
        for key, value in request_items:
            setattr(self, key, value)

class ResponseData:
    """
    HTTP yanıtı verilerini temsil eden sınıf.
    
    Attributes:
        status_code (int): HTTP durum kodu
        Dinamik olarak eklenen diğer nitelikler
    """
    def __init__(self, response):
        """
        ResponseData sınıfı için yapılandırıcı.
        
        Args:
            response (requests.Response): HTTP yanıtı nesnesi
        """
        self.status_code = response.status_code
        
        try:
            response_items = response.json().items()
        except (ValueError, AttributeError):
            response_items = []
            
        for key, value in response_items:
            setattr(self, key, value)

class RequestAndResponseData:
    """
    Bir HTTP isteği ve yanıtı çiftini temsil eden sınıf.
    
    Attributes:
        request (RequestData): İstek verileri
        response (ResponseData): Yanıt verileri
        endpoint (str): İsteğin yapıldığı endpoint
        statusCode (int): HTTP durum kodu
    """
    def __init__(self, request, response, endpoint):
        """
        RequestAndResponseData sınıfı için yapılandırıcı.
        
        Args:
            request (dict): İstek verisi
            response (requests.Response): HTTP yanıtı
            endpoint (str): İsteğin yapıldığı endpoint
        """
        self.request = RequestData(request)
        self.response = ResponseData(response)
        self.endpoint = endpoint
        self.statusCode = response.status_code

def export_data_to_excel(data_list, filename, app_name):
    """
    İstek ve yanıt verilerini Excel dosyasına aktarır.
    
    Args:
        data_list (list): RequestAndResponseData nesnelerini içeren liste
        filename (str): Kaydedilecek Excel dosyası adı
        app_name (str): İlgili uygulama adı
    
    Returns:
        bool: İşlem başarılı ise True, değilse False
    """
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