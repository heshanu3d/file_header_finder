# -*- coding: utf-8 -*-

import os
import re

def find_files(path, files, pattern):
    sub = os.listdir(path)
    for s in sub:
        sub_path = path + "/" + s
        if (os.path.isdir(sub_path)):
            find_files(sub_path, files, pattern)
        else:
            if re.match(pattern, s):
                files.add(sub_path)

def find_header_file(path, header_files):
    if not path:
        return
    with open(path, 'r', encoding="utf-8") as f:
        f.seek(0, 2)  # 指针移动到文件末尾
        size = f.tell()  # 此时指针的位置即文件末尾的位置
        f.seek(0, 0)  # 把指针移回文件开头
        while f.tell() < size:  # 如果指针在size之前
            line = f.readline()  # 用readline()读一行
            res = re.findall(r'#include ["|<](.+\.h)["|>]', line.strip())
            if res:
                header_files.add(res[0])

def find_header_file_path(name, root_path):
    files = set()
    find_files(root_path, files, r'.+\.(h|hpp)')
    for file in files:
        if re.match(r'.*/'+ name, file):
            return file

if __name__ == "__main__":
    root_path = "C:/Users/hs-s1/Downloads/Compressed/handy-master/handy"
    files = set()
    header_file_names = set()
    find_files(root_path, files, r'.+\.(cc|cpp|h|hpp)')
    header_files = set()
    find_files(root_path, header_files, r'.+\.(h|hpp)')
    for file in files:
        find_header_file(file, header_file_names)


    new_header_file_names = set()
    for header_file_name in header_file_names:
        header_file_path = find_header_file_path(header_file_name, root_path)
        if header_file_path:
            find_header_file(header_file_path, new_header_file_names)

    while(True):
        erase_set = set()
        for new_header_file_name in new_header_file_names:
            if new_header_file_name in header_file_names:
                erase_set.add(new_header_file_name)
            else:
                header_file_names.add(new_header_file_name)
        for name in erase_set:
            new_header_file_names.remove(name)
        if (len(new_header_file_names) == 0):
            break;
        tmp = new_header_file_names
        new_header_file_names.clear()
        for name in tmp:
            path = find_header_file_path(name, root_path)
            if path:
                find_header_file(path, new_header_file_names)
    for header_file_name in header_file_names:
        path = find_header_file_path(header_file_name, root_path)
        if path:
            header_files.add(path)
    for header_file in header_files:
        print(header_file)
    print("---------------------------")
    for header_file in header_files:
        header_file = re.sub(root_path, '', header_file)
        print(header_file)

