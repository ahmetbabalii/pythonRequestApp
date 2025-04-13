"""
HTTP İstek Uygulaması.
Bu, uygulamanın ana giriş noktasıdır.
"""
import argparse
from config import EXCEL_FILE
from utils import logger
from request_manager import load_data_from_excel
from data_processor import export_data_to_excel

def main():
    """
    Uygulamanın ana fonksiyonu
    """
    # Komut satırı argümanlarını işle
    parser = argparse.ArgumentParser(description='HTTP İstek Uygulaması')
    parser.add_argument('--excel', type=str, default=EXCEL_FILE,
                      help='Excel dosyasının konumu (varsayılan: datas.xlsx)')
    parser.add_argument('--filter', type=str, default=None,
                      help='Belirli bir uygulama adı ile filtreleme')
    args = parser.parse_args()
    
    # Excel'den verileri yükle
    excel_file = args.excel
    logger.info(f"'{excel_file}' dosyasından veriler yükleniyor...")
    veriler = load_data_from_excel(excel_file)
    
    # Filtreleme işlemi
    if args.filter:
        filtered_veriler = [veri for veri in veriler if veri.uygulamaadi == args.filter]
        logger.info(f"'{args.filter}' filtresine göre {len(filtered_veriler)} adet veri bulundu.")
        veriler = filtered_veriler
    
    # Her veri öğesi için istekleri gönder ve sonuçları işle
    logger.info(f"Toplam {len(veriler)} adet veri için istek gönderiliyor...")
    for veri in veriler:
        # İstekleri gönder
        results = veri.request()
        
        # Sonuçları kontrol et
        if results is None:
            logger.warning(f"{veri.uygulamaadi} için sonuç alınamadı, devam ediliyor...")
            continue
        
        # Sonuçları Excel'e aktar
        export_data_to_excel(results, f'{veri.uygulamaadi}.xlsx', veri.uygulamaadi)

if __name__ == "__main__":
    try:
        logger.info("Uygulama başlatılıyor...")
        main()
        logger.info("Uygulama başarıyla tamamlandı.")
    except KeyboardInterrupt:
        logger.info("Uygulama kullanıcı tarafından durduruldu.")
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {str(e)}")
        raise