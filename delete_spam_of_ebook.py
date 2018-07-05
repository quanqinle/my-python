#coding:utf-8

# 删除电子书中的垃圾信息。
# 背景知识：网上下载的电子书大都每隔几章节就会有广告信息，故而需要删除，免得干扰

import os

spams = ['电子书', 'txt', '下载', '免费']

def is_spam_line(line, threshold=1):
    '''
    该行是否是垃圾行  
    :param line:  
    :param threshold: 存在的垃圾词数目超过这个阈值才认为是垃圾行  
    :return: boolean
    '''
    cnt = 0
    for word in spams:
        if line.count(word) > 0:
            cnt += 1
    
    if cnt >= threshold:
        return True
    else:
        return False


def delete_spam():
    '''
    删除文件中的特定字符串
    '''
    with open('橙红年代.txt', 'r', encoding='gbk') as fin:
        with open('橙红年代-new.txt', 'w', encoding='utf-8') as fout:
            for line in fin.readlines():
                line = line.strip()

                if (line.isspace() or line == ''):
                    # fout.write('\n') # 不删除空行
                    continue
                elif not is_spam_line(line, 2):
                    fout.write(line + '\n')


def main():
    os.chdir(r'C:\Users\quanql\Desktop')
    delete_spam()

if __name__ == "__main__":
    main()