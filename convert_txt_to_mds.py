#coding:utf-8

# 读取一个包含Friends全部剧本的txt，格式处理后，按剧集分别保存到md文件

import re

def split_friends_txt_2_mds():
    '''
    读取一个包含Friends全部剧本的txt，格式处理后，按剧集分别保存到md文件
    '''
    fname = ''
    with open('./friends-all.txt', 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            line = line.strip()
            words = line.split()
            # print(words)
            if words:
                # 剧集标题前面是纯数字
                if re.match(r'^\d{1,8}$', words[0]):
                    print(line)
                    fname = line.replace('"', "'") + '.md'

            with open('./' + fname, 'a+', encoding='utf-8') as fout:
                fout.write(line)
                fout.write('\n\n')


def main():
    split_friends_txt_2_mds()


if __name__ == "__main__":
    main()
