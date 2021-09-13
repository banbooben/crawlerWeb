#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/1/21 18:22
# @Author  : shangyameng
# @Email   : shangyameng@aliyun.com
# @Site    : 
# @File    : pdf_tools.py
# @desc    :

import os


class PdfTools(object):

    @staticmethod
    def py_mu_pdf_fitz(file_path, pages=None, index_map=None):
        import fitz
        new_file_name = os.path.basename(file_path)
        images_ath = file_path.rsplit(".", 1)[0] + "/" + new_file_name.rsplit(".", 1)[0]
        _ = os.makedirs(images_ath) if not os.path.exists(images_ath) else None
        with fitz.open(file_path) as pdf_reader:
            pages = pages if pages or pages == 0 else [x for x in range(pdf_reader.pageCount)]

            if isinstance(pages, list):
                for page in pages:
                    new_name = images_ath + f"/{page}.png"
                    if page <= pdf_reader.pageCount - 1:
                        # trans = fitz.Matrix(2, 2).preRotate(0)
                        trans = fitz.Matrix(2, 2).preRotate(0)
                        pdf_reader[page].getPixmap(matrix=trans).writePNG(new_name)
            elif pages == 0 or (isinstance(pages, int) and pages <= pdf_reader.pageCount):
                new_name = images_ath + f"/{new_file_name.rsplit('.', 1)[0]}_{pages}.png"

                # if index_map:
                #     mat = fitz.Quad()
                #     m = fitz.Matrix()
                #     mat.rect((10, 100), (100, 100), (10, 200), (100, 200))
                #     pdf_reader[pages].getPixmap(matrix=mat).writePNG(new_name)

                trans = fitz.Matrix(2, 2).preRotate(0)
                pdf_reader[pages].getPixmap(matrix=trans).writePNG(new_name)
                images_ath = new_name
            else:
                return []
        return images_ath

    @staticmethod
    def pdf_split_one(filename, pages=None):
        from PyPDF2 import PdfFileReader, PdfFileWriter
        pages = pages or []
        if not pages:
            return []
        new_file_dir = os.path.dirname(filename)
        new_file_name = os.path.basename(filename)
        pdf_reader = PdfFileReader(filename, strict=False)
        # 创建一个新的写实例
        pdf_writer = PdfFileWriter()
        if isinstance(pages, list):
            for page in pages:
                pdf_writer.addPage(pdf_reader.getPage(page))
            new_name = new_file_dir + f"/{new_file_name.rsplit('.', 1)[0]}_{pages[0]}_{pages[-1]}.pdf"

        else:
            pdf_writer.addPage(pdf_reader.getPage(pages))
            new_name = new_file_dir + f"/{new_file_name.rsplit('.', 1)[0]}_{pages}.pdf"

        with open(new_name, "wb") as f:
            pdf_writer.write(f)
        return new_name

    @staticmethod
    def pdf_to_images(file_path: str, pages=None):
        import pdf2image
        import tempfile
        pages = pages or []
        if not pages:
            return []
        images_ath = file_path.rsplit(".", 1)[0]
        cmd = os.makedirs(images_ath) if not os.path.exists(images_ath) else None
        # images = pdf2image.convert_from_path(file_path)
        with tempfile.TemporaryDirectory() as path:
            images = pdf2image.convert_from_path(file_path, output_folder=path)
            if isinstance(pages, list):
                [image.save(images_ath + '/' + f'psReport_{image}s.jpg', 'JPEG') for image in
                 images[pages[0]:pages[-1] + 1]]
            elif isinstance(pages, int) and pages < len(images):
                images[pages].save(images_ath + '/' + f'psReport_{images[pages]}s.jpg', 'JPEG')
            else:
                return []
        return images_ath


if __name__ == '__main__':
    path = "/Users/sarmn/Downloads/00-国泰君安期货_[苯乙烯]_R3_晨报_20210126 (1).pdf"

    a = PdfTools()
    ss = a.py_mu_pdf_fitz(path)
    print(ss)



