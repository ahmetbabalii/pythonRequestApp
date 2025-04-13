"""
Yardımcı fonksiyonlar ve yardımcı sınıfları içerir.
Bu modülde, uygulamanın çeşitli yerlerinde kullanılan genel amaçlı fonksiyonlar bulunur.
"""
import logging
from config import LOG_FORMAT, LOG_FILE, LOG_LEVEL

def check_none(value):
    """
    None değerlerini boş string'e dönüştürür, diğer değerleri string'e çevirir.
    
    Args:
        value: Kontrol edilecek değer
        
    Returns:
        str: None ise boş string, değilse değerin string hali
    """
    return '' if value is None else str(value)

def setup_logging():
    """
    Log sistemini yapılandırır.
    
    Returns:
        logging.Logger: Yapılandırılmış logger nesnesi
    """
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    # Logger yapılandırma
    logger = logging.getLogger('request_app')
    logger.setLevel(log_level)
    
    # Dosya handler'ı
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(log_level)
    
    # Konsol handler'ı
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Formatter
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Handler'ları ekle
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger nesnesini oluştur
logger = setup_logging()