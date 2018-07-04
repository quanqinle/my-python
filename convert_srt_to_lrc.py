#coding:utf-8

# 将字幕srt文件内容另存为歌词lrc文件格式

import os
import re


def get_timeline(t, ahead=0):
    '''
    将srt格式的时间转化成lrc格式，并[]包裹  
    :param t: 字符串，形如00:00:13,246  
    :param ahead: s，3位浮点型，正数字幕时间戳提前，负数字幕延后  
    :return: [分钟:秒.毫秒]
    '''
    t = t.replace(',', '.')
    if t.count(':') >= 2:
        tt = t.split(':')
        sec = max(0, float(tt[len(tt)  - 1]) - ahead)
        return ('[%s:%.3f]' % (tt[len(tt) - 2], sec) )
    else:
        print('处理时间轴失败，原始信息：' + t)
        return '[' + t + ']'


def convert_srt_to_lrc():
    '''
    将字幕srt文件内容另存为歌词lrc文件格式
    '''
    for fname in os.listdir('./pappe pig-s01'):
        if not fname.endswith('.srt'):
            continue

        with open('./pappe pig-s01/' + fname, 'r', encoding='utf-8') as fin:
            with open('./LRC/' + fname.replace('.srt', '.lrc'), 'w', encoding='utf-8') as fout:

                print(fname)
                starttime = ''
                endtime = ''
            
                for line in fin.readlines():
                    line = line.strip()

                    if (line.isspace() or line.isnumeric()):
                        continue
                    if line.find('-->') > 0:
                        fout.write(' ' + endtime) # 应用上次存储的结束时间戳

                        words = line.split('-->')
                        starttime = get_timeline(words[0].strip(), 0.030)
                        endtime = get_timeline(words[1].strip(), 0.030)
                        fout.write('\n' + starttime + ' ')
                        continue
                    else:
                        # u = line.decode('utf-16')
                        # line = u.encode('utf-8')
                        fout.write(line)


def main():
    os.chdir("D:\\data\\tmp\\字幕")
    convert_srt_to_lrc()


if __name__ == "__main__":
    main()