import os

top_dir = os.path.dirname(os.path.dirname(__file__))

src_dir = os.path.join(top_dir, 'src')
data_dir = os.path.join(top_dir, 'data')

test_dir = os.path.join(data_dir, 'test')
valid_dir = os.path.join(data_dir, 'valid')
test_company_list = os.path.join(test_dir, 'company_list.csv')
valid_company_list = os.path.join(valid_dir, 'company_list.csv')
test_pdf_dir = os.path.join(test_dir, 'docs_pdf')
valid_pdf_dir = os.path.join(valid_dir, 'docs_pdf')
test_img_dir = os.path.join(test_dir, 'docs_image')
valid_img_dir = os.path.join(valid_dir, 'docs_image')
test_ocr_dir = os.path.join(test_dir, 'docs_ocr')
valid_ocr_dir = os.path.join(valid_dir, 'docs_ocr')
test_text_dir = os.path.join(test_dir, 'docs_text')
valid_text_dir = os.path.join(valid_dir, 'docs_text')
test_db_dir = os.path.join(test_dir, 'embedding_db')
valid_db_dir = os.path.join(valid_dir, 'embedding_db')

test_query_path = os.path.join(test_dir, 'query.csv')

export_dir = os.path.join(top_dir, 'export')
