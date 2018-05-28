#coding:utf-8

# 遍历文件夹，将所有的txt文件处理后存储为md。txt处理逻辑：中文行尾加空格

import os
import re


def contain_chinese(text):
    '''
    判断传入字符串是否包含中文
    :param text: 字符串
    :return: True:包含中文  False:不包含中文
    '''
    # return all('\u4e00' <= char <= '\u9fff' for char in text) # wrong
    for uchar in text:
        if '\u4e00' <= uchar <= '\u9fff':
            return True
    return False


def convert_txt_2_md():
    '''
    遍历文件夹，将所有的txt文件处理后存储为md
    txt处理逻辑：中文行尾加空格
    '''
    for fname in os.listdir('.'):
        if fname.find('.txt') < 0:
            continue

        print(fname)

        with open('./' + fname.replace('.txt', '.md'), 'w', encoding='utf-8') as fout:
            with open('./' + fname, 'r', encoding='utf-16') as fin:
                for line in fin.readlines():
                    if line.find('-->') > 0:
                        continue
                    if re.match(r'^\d{1,8}$', line):
                        # 整行只有数字1-8位
                        continue
                    if contain_chinese(line):
                        # u = line.decode('utf-16')
                        # line = u.encode('utf-8')
                        fout.write(line.replace('\n', '  \n'))
                    else:
                        # u = line.decode('utf-16')
                        # line = u.encode('utf-8')
                        fout.write(line)


def main():
    convert_txt_2_md()


if __name__ == "__main__":
    main()