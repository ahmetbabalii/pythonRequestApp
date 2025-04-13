"""
Uygulama için konfigürasyon ayarlarını içerir.
Bu dosya, uygulamanın temel parametrelerini ve seçeneklerini tanımlar.
"""

# HTTP istek yapılandırmaları
REQUEST_TIMEOUT = 30  # Saniye cinsinden istek zaman aşımı
CONTENT_TYPE = 'application/json'
DEFAULT_HEADERS = {'Content-Type': CONTENT_TYPE}

# Dosya yapılandırmaları
EXCEL_FILE = 'datas.xlsx'
LOG_FILE = 'request_app.log'

# Logging yapılandırmaları
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'  # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'

# Thread yapılandırmaları
MAX_WORKERS = 10  # ThreadPoolExecutor için maksimum iş parçacığı sayısı