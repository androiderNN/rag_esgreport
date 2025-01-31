import os
from dotenv import load_dotenv

import config
from data_processors import company_extractor, pdf2text, pdf2jpg, ocr_gcv, database

load_dotenv()

if __name__ == '__main__':
    # 企業名のリスト作成
    # company_extractor.save_company_list(config.train_company_list, config.valid_company_list)

    # pdfをjpgに変換
    # pdf2jpg.save_jpg(config.train_pdf_dir, config.train_img_dir)
    # pdf2jpg.save_jpg(config.valid_pdf_dir, config.valid_img_dir)

    # vision apiでocr
    # ocr_gcv.save_response(config.train_img_dir, config.train_ocr_dir)
    # ocr_gcv.save_response(config.valid_img_dir, config.valid_ocr_dir)

    # pdfをテキストに変換
    pdf2text.pdf2text(config.train_pdf_dir, config.train_text_dir)
    pdf2text.pdf2text(config.valid_pdf_dir, config.valid_text_dir)

    # embeddingとdatabaseへの保存
    # database.text2db(config.train_text_dir, config.train_db_dir)
    # database.text2db(config.valid_text_dir, config.valid_db_dir)
