import os
import config
from data_processors import company_extractor, pdf2text, ocr

if __name__ == '__main__':
    # 企業名のリスト作成
    # company_extractor.save_company_list(config.train_company_list, config.valid_company_list)

    # pdfをjpgに変換
    # ocr.save_jpg(config.train_pdf_dir, config.train_img_dir)
    # ocr.save_jpg(config.valid_pdf_dir, config.valid_img_dir)

    # pdfをテキストに変換
    pdf2text.pdf2text(config.train_pdf_dir, config.train_text_dir)
    # pdf2text.pdf2text(config.valid_pdf_dir, config.valid_text_dir)