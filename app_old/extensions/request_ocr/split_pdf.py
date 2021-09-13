# coding=utf-8

import json
import os
import subprocess


#
# def split_pdf(ori_pdf, page_num, n):
#     """
#     使用pdfseparate分割成每N页的文件
#     """
#     file_name = ori_pdf.rsplit('.', 1)[0]
#     split_pdf_file_list = []
#     if page_num > n:
#         all_pages = list(range(1, page_num + 1))
#         split_pages_with_n = [all_pages[i:i + n] for i in range(0, len(all_pages), n)]
#         for split_pages in split_pages_with_n:
#             begin_page = split_pages[0]
#             end_page = split_pages[-1]
#             shell_command = "pdfseparate -f {} -l {} {} {}-%d.pdf".format(begin_page, end_page, ori_pdf, file_name)
#             os.system(shell_command)
#             pdf_path_list = [file_name + '-' + str(page) + '.pdf' for page in range(begin_page, end_page + 1)]
#             res_pdf_path = file_name + '-' + str(begin_page) + '-' + str(end_page) + '.pdf'
#             unite_pdf(pdf_path_list, res_pdf_path)
#     else:
#         split_pdf_file_list = [ori_pdf]
#     return split_pdf_file_list
def split_pdf(ori_pdf, page_num, n):
    """
    使用pdfseparate分割成每N页的文件
    """
    file_name = ori_pdf.rsplit('.', 1)[0]
    split_pdf_file_list = []
    all_pages = get_file_page(ori_pdf)
    if page_num > n:
        begin_page = page_num
        end_page = page_num + n
        shell_command = "pdfseparate -f {} -l {} {} {}-%d.pdf".format(begin_page, end_page, ori_pdf, file_name)
        os.system(shell_command)
        if end_page <= all_pages:
            end_page += 1
        pdf_path_list = [file_name + '-' + str(page) + '.pdf' for page in range(begin_page, end_page)]
        res_pdf_path = file_name + '-' + str(begin_page) + '-' + str(end_page) + '.pdf'
        split_pdf_file_list.append(res_pdf_path)
        unite_pdf(pdf_path_list, res_pdf_path)
    else:
        split_pdf_file_list = [ori_pdf]
    return split_pdf_file_list



def get_file_page(ori_pdf):
    cmd = "pdfinfo {}".format(ori_pdf)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output_lines = []
    pages = 0
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.strip()
        if line:
            output_lines.append(line)
    for i in range(0, len(output_lines)):
        if b'Pages' in output_lines[i]:
            pages = output_lines[i].split(b' ')[-1]
    return int(pages)


def unite_pdf(pdf_path_list, res_pdf_path):
    """
    根据列表，合并成一个pdf文件，pdf路径不要有空格和中文
    """
    pdf_path_str = " ".join(pdf_path_list)
    shell_command = "pdfunite {} {}".format(pdf_path_str, res_pdf_path)
    os.system(shell_command)
    for pdf_path in pdf_path_list:
        os.remove(pdf_path)
    assert os.path.exists(res_pdf_path), 'combine all files into one pdf file error'


# def unit_candidate_json(json_path_list, res_json_path):
#     """
#     根据列表，合并成一个候选集json文件
#     """
#     res_json = []
#     for each_file in json_path_list:
#         print(each_file)
#         content = json.loads(open(each_file, 'r').read())
#         img_data_list = content['img_data_list']
#         print(img_data_list)
#         for i in img_data_list:
#             res_json.extend(i['text_info'])
#     with open(res_json_path, 'w', encoding='utf-8') as fs:
#         fs.write(json.dumps(res_json, ensure_ascii=False))
#     for json_path in json_path_list:
#         os.remove(json_path)
#     assert os.path.exists(res_json_path), 'combine all files into one json file error'
#
#
# def delete_split_file(split_file_list):
#     """
#     删除分割出来的pdf文件
#     """
#     if len(split_file_list) > 1:
#         for spit_file in split_file_list:
#             os.remove(spit_file)


if __name__ == '__main__':
    test_file_path = "/Users/sarmn/DG/project/suyan/suyan/suyan_server/flaskr/upload/苏研分类/4.pdf"
    res = split_pdf(test_file_path, 12, 1)
    print(res)
