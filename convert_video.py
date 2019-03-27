#coding:utf-8

#===============================================================================
# 视频处理
# 视频转换成mp4格式，并将字幕烧制到视频中
#===============================================================================
# 

import os
import shutil
import time

#单集动画（1~10分钟）
src_dir = 'D:\\tmp\\video-source\\'
des_dir = 'D:\\tmp\\video-target\\'
subtitle_dir = 'D:\\tmp\\video-subtitle\\'
log_file = r'D:/log.csv'
commad_line = 'ffmpeg.exe -i "{0}" -vf subtitles=\"{1}\" "{2}"'
commad_line2 = 'ffmpeg.exe -i "{0}" "{1}"'

#commad_line= commad_line.decode("utf-8").encode("gbk")

def convert_video(filename):
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
        to_log("跳过已存在, " + des_file)
        return

    # 字幕文件
    subtitle_file = (froot + ".en.srt")

    src_file = src_dir + filename

    """
    Note:
    I think ffmpeg has some problems when it uses the parameter '-vf subtitles ='.
    File directory, single quote, comma, etc. are not allowed in this parameter.
    """ 
    os.chdir(subtitle_dir) # ffmpeg提取mkv内的字幕时，有bug！
    
    if '.mp4' == fext:
        if os.path.exists(subtitle_file):
            run_cmd(src_file, subtitle_file, des_file)
            to_log("[mp4有字幕], " + filename)
        else:
            shutil.copy(src_file, des_file)
            to_log("[mp4无字幕], " + filename)
    elif '.mkv' == fext:
        if not os.path.exists(subtitle_file):
            # todo
            subtitle_file = filename
        run_cmd(src_file, subtitle_file, des_file)
        to_log("[mkv视频], " + filename)
    elif '.webm' == fext:
        if os.path.exists(subtitle_file):
            run_cmd(src_file, subtitle_file, des_file)
            to_log("[webm有字幕], " + filename)
        else:
            os.system(commad_line2.format(src_file, des_file))
            to_log("[webm无字幕], " + filename)
    else:
        to_log('[未知文件], ' + filename)

#===============================================
# 执行系统指令
# Note: 为了规避ffmpeg缺陷，重命名字幕文件。最后再改回文件名
#===============================================
def run_cmd(srcpath, subtitlefile, despath):
    new_name = time.time()
    os.rename(subtitlefile, new_name)
    os.system(commad_line.format(srcpath, new_name, despath))
    os.rename(new_name, subtitlefile)

#===============================================
# mkv视频是否含有字幕
#===============================================
def mkv_has_subtitle(mkv_file):
    cmd = "ffmpeg -i \"{0}\" -c copy -map 0:s -f null - -v 0 -hide_banner && echo $? || echo $?"
    code = os.system(cmd.format(mkv_file))
    # TODO 为调通
    if code == 0:
        return True
    return False

def to_log(line):
    fname = log_file
    with open(fname, 'a+', encoding='utf-8') as fout:
        print(line)
        fout.write(line)
        fout.write('\n')

#===============================================
# 并发任务
#===============================================
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

