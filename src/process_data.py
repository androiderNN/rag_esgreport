import config
from data_processors import company_extractor, pdf2text

if __name__ == '__main__':
    # 企業名のリスト作成
    # company_extractor.save_company_list(config.train_company_list, config.valid_company_list)

    # pdfの変換
    pdf2text.pdf2text(config.train_pdf_dir, config.train_text_dir)
    # pdf2text.pdf2text(config.valid_pdf_dir, config.valid_text_dir)