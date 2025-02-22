import os
from dotenv import load_dotenv

load_dotenv()

import config
from data_processors import company_extractor, pdf2text, pdf2jpg, ocr_gcv, markdownize, database

if __name__ == '__main__':
    # 企業名のリスト作成
    # company_extractor.save_company_list(config.test_company_list, config.valid_company_list)

    # pdfをjpgに変換
    # pdf2jpg.save_jpg(config.test_pdf_dir, config.test_img_dir)
    # pdf2jpg.save_jpg(config.valid_pdf_dir, config.valid_img_dir)

    # vision apiでocr
    # ocr_gcv.save_ocr(config.test_img_dir, config.test_ocr_dir)
    # ocr_gcv.save_ocr(config.valid_img_dir, config.valid_ocr_dir)

    # markdownに変換
    # markdownize.markdownize(config.test_img_dir, config.test_ocr_dir, config.test_md_dir)
    # markdownize.markdownize(config.valid_img_dir, config.valid_ocr_dir, config.valid_md_dir)

    # pdfをテキストに変換
    pdf2text.pdf2text(config.test_pdf_dir, config.test_text_dir)
    pdf2text.pdf2text(config.valid_pdf_dir, config.valid_text_dir)

    # embeddingとdatabaseへの保存
    # database.text2db(config.test_text_dir, config.test_db_dir)
    # database.text2db(config.valid_text_dir, config.valid_db_dir)
