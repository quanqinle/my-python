#coding:utf-8

#===============================================================================
# 视频处理
#===============================================================================
# 

import os
import shutil
import time

#单集动画（1~10分钟）
src_dir = 'D:\\tmp\\video\\source\\'
des_dir = 'D:\\tmp\\video\\target\\'
log_file = r'D:/tmp/video/convert.csv'
commad_line = 'ffmpeg.exe -ss 00:00:02 -i "{0}" -vf subtitles="{1}" "{2}"'
commad_line2 = 'ffmpeg.exe -ss 00:00:02 -i "{0}" "{1}"'
#commad_line= commad_line.decode("utf-8").encode("gbk")

def convert_video(filename):
    # for filename in os.listdir(src_dir):
    
    froot, fext = os.path.splitext(filename)
    fext = fext.lower()
    
    fname_lower = filename.lower()
    
    # 跳过字幕文件
    if '.srt' == fext:
        if not fname_lower.endswith('.en.srt'):
            to_log("[非英字幕], " + filename)
        return
    
    # 跳过已存在文件
    des_file = des_dir + (froot + ".mp4")
    if os.path.exists(des_file):
        print("跳过已存在, " + des_file)
        return

    # 字幕文件
    subtitle_file = src_dir + (froot + ".en.srt")

    src_file = src_dir + filename

    print(des_file)
    print(commad_line.format(src_file, subtitle_file, des_file))
    if '.mp4' == fext:
        if os.path.exists(subtitle_file):
            os.system(commad_line.format(src_file, subtitle_file, des_file))
            to_log("[mp4有字幕], " + filename)
        else:
            shutil.copy(src_file, des_file)
            to_log("[mp4无字幕], " + filename)
    elif '.mkv' == fext:
        os.chdir(src_dir) # ffmpeg提取mkv内的字幕时，有bug！
        subtitle_file = froot + ".en.srt"
        if not os.path.exists(subtitle_file):
            subtitle_file = filename
        to_log("[mkv视频], " + filename)
        os.system(commad_line.format(src_file, subtitle_file, des_file))
    elif '.webm' == fext:
        if os.path.exists(subtitle_file):
            os.system(commad_line.format(src_file, subtitle_file, des_file))
            to_log("[webm有字幕], " + filename)
        else:
            os.system(commad_line2.format(src_file, des_file))
            to_log("[webm无字幕], " + filename)
    else:
        to_log('[未知文件], ' + filename)


def to_log(line):
    fname = log_file
    with open(fname, 'a+', encoding='utf-8') as fout:
        print(line)
        fout.write(line)
        fout.write('\n')


from multiprocessing import Process, Queue, Pool
def batch_tast(processes=10):
    """ 并发 """
    start_time = time.time()
    pool = Pool(processes)
    
    for filename in os.listdir(src_dir):
        pool.apply_async(convert_video, (filename, ))

    pool.close()
    pool.join()
    end_time = time.time()
    print('处理完毕，用时:%s 秒' % (end_time - start_time))

def main():
    batch_tast(processes=10)
#     for filename in os.listdir(src_dir):
#         convert_video(filename)

if __name__ == "__main__":
    main()

