import json
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from utils import check_none, logger
from data_processor import RequestAndResponseData
from config import DEFAULT_HEADERS, REQUEST_TIMEOUT, MAX_WORKERS

class RequestError(Exception):
    pass

class Veri:
    def __init__(self, dns, uygulamaadi, endpoint, postOrnek, requestType, timeout=REQUEST_TIMEOUT):
        self.dns = check_none(dns)
        self.uygulamaadi = check_none(uygulamaadi)
        self.endpoint = check_none(endpoint)
        self.postOrnek = check_none(postOrnek)
        self.requestType = check_none(requestType)
        self.timeout = timeout
    
    def request(self):
        logger.info(f'{self.uygulamaadi} için istek gönderiliyor...')
        print(f'{self.uygulamaadi} için istek gönderiliyor...')
        
        try:
            data = self._prepare_data()
            requests_and_responses = self._send_requests(data)
            
            return [RequestAndResponseData(request, response, self.endpoint) 
                   for request, response in requests_and_responses]
                   
        except json.JSONDecodeError:
            logger.error(f'{self.uygulamaadi} için JSON ayrıştırma hatası: {self.postOrnek}')
            return None
        except requests.Timeout:
            logger.error(f'{self.uygulamaadi} için zaman aşımı hatası: {self.endpoint}')
            return None
        except requests.RequestException as e:
            logger.error(f'{self.uygulamaadi} için istek hatası: {str(e)}')
            return None
        except Exception as e:
            logger.error(f'{self.uygulamaadi} için beklenmeyen hata: {str(e)}')
            return None
    
    def _prepare_data(self):
        if not self.postOrnek:
            return None
        return json.loads('[' + self.postOrnek + ']')
    
    def _send_requests(self, data):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            if self.requestType == 'GET':
                return list(executor.map(
                    lambda item: (item, requests.get(
                        self.endpoint, 
                        headers=DEFAULT_HEADERS, 
                        timeout=self.timeout
                    )), 
                    [None]
                ))
            elif self.requestType == 'POST':
                return list(executor.map(
                    lambda item: (item, requests.post(
                        self.endpoint, 
                        headers=DEFAULT_HEADERS, 
                        json=item, 
                        timeout=self.timeout
                    )), 
                    data
                ))
            else:
                logger.warning(f'{self.uygulamaadi} için geçersiz request tipi: {self.requestType}')
                raise RequestError(f"Desteklenmeyen istek tipi: {self.requestType}")
                
def load_data_from_excel(excel_file):
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        veriler = [
            Veri(
                row['dns'], 
                row['uygulamaadi'], 
                row['endpoint'], 
                row['postOrnek'], 
                row['requestType']
            ) for index, row in df.iterrows()
        ]
        logger.info(f"{excel_file} dosyasından {len(veriler)} adet veri yüklendi.")
        return veriler
    except Exception as e:
        logger.error(f"Excel dosyası yükleme hatası: {str(e)}")
        return []