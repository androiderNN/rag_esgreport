import os

data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
train_dir = os.path.join(data_dir, 'train')
valid_dir = os.path.join(data_dir, 'valid')
train_pdf_dir = os.path.join(train_dir, 'docs_pdf')
valid_pdf_dir = os.path.join(valid_dir, 'docs_pdf')
train_text_dir = os.path.join(train_dir, 'docs_text')
valid_text_dir = os.path.join(valid_dir, 'docs_text')
