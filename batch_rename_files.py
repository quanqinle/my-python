#coding:utf-8

# 批量重命名文件

import os

def rename_files():
    # windows系统，则c:\\mydir
    # Linux系统，'/home/quanql/old'
    for filename in os.listdir('.'):
        if filename[-2: ] == 'py':
            #过滤掉改名的.py文件
            continue
        # 文件名替换规则：去掉空格
        name = filename.replace(' ', '')
        # 选择名字中需要保留的部分
        new_name = name[20: 30] + name[-4:]
        os.rename(filename, new_name)

def main():
    rename_files()


if __name__ == "__main__":
    main()