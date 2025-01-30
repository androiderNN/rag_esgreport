import os

top_dir = os.path.dirname(os.path.dirname(__file__))

src_dir = os.path.join(top_dir, 'src')
data_dir = os.path.join(top_dir, 'data')

train_dir = os.path.join(data_dir, 'train')
valid_dir = os.path.join(data_dir, 'valid')
train_company_list = os.path.join(train_dir, 'company_list.csv')
valid_company_list = os.path.join(valid_dir, 'company_list.csv')
train_pdf_dir = os.path.join(train_dir, 'docs_pdf')
valid_pdf_dir = os.path.join(valid_dir, 'docs_pdf')
train_img_dir = os.path.join(train_dir, 'docs_image')
valid_img_dir = os.path.join(valid_dir, 'docs_image')
train_ocr_dir = os.path.join(train_dir, 'docs_ocr')
valid_ocr_dir = os.path.join(valid_dir, 'docs_ocr')
train_text_dir = os.path.join(train_dir, 'docs_text')
valid_text_dir = os.path.join(valid_dir, 'docs_text')
train_db_dir = os.path.join(train_dir, 'embedding_db')
valid_db_dir = os.path.join(valid_dir, 'embedding_db')
