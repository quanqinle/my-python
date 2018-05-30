#coding:utf-8

# 将字幕srt文件内容另存为歌词lrc文件格式

import os
import re


def get_timeline(t):
    '''
    将srt格式的时间转化成lrc格式，并[]报告
    :param t: 字符串，形如00:00:13,246
    :return: [分钟:秒.毫秒]
    '''
    if t.count(',') > 0:
        return '[' + t.replace(',', '.') + ']'
    else:
        print('处理时间轴失败，原始信息：' + t)
        return '[' + t + ']'


def convert_srt_to_lrc():
    '''
    将字幕srt文件内容另存为歌词lrc文件格式
    '''
    for fname in os.listdir('./pappe pig'):
        if not fname.endswith('.srt'):
            continue

        with open('./pappe pig/' + fname, 'r', encoding='utf-8') as fin:
            with open('./LRC/' + fname.replace('.srt', '.lrc'), 'w', encoding='utf-8') as fout:

                print(fname)
            
                for line in fin.readlines():
                    line = line.strip()

                    if (line.isspace() or line.isnumeric()):
                        continue
                    if line.find('-->') > 0:
                        words = line.split('-->')
                        timeline = get_timeline(words[0].strip())
                        fout.write('\n' + timeline)
                        continue
                    else:
                        # u = line.decode('utf-16')
                        # line = u.encode('utf-8')
                        fout.write(' ' + line)


def main():
    convert_srt_to_lrc()


if __name__ == "__main__":
    main()