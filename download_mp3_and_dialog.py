# 网页抓取英文对话，保存成md和mp3
#coding:utf-8

import os
import time
import requests
import traceback
from lxml import html
from lxml import etree

SAVE_FILE_TO_DIR = 'sef'

def get_audio_info():
    md = []
    mp3 = {}

    url='https://www.rong-chang.com/speak/'
    rsp = requests.get(url)
    tree = html.fromstring(rsp.text)
    category_urls = tree.xpath('//table//p[@class="MsoNormal"]//a')

    # for category_url in category_urls:
    for category_no, category_url in enumerate(category_urls):
        category_name = category_url.text
        # print('# %s\n' % category_name)
        md.append('# %s\n' % category_name)
        rsp = requests.get(url + category_url.get('href'))
        tree = html.fromstring(rsp.text)
        dialog_urls = tree.xpath('//table//p[@class="MsoNormal"]//a')

        for dialog_no, dialog_url in enumerate(dialog_urls):
            href = dialog_url.get('href')
            if ('youtube.com' in href):
                continue
            
            dialog_name = dialog_url.text
            # print('## %s\n' % (dialog_name))
            md.append('## %s\n' % (dialog_name))

            rsp = requests.get(url + href)
            tree = html.fromstring(rsp.text)
            dialog = tree.xpath('//blockquote')
            # print('%s\n' % dialog[0].text_content().strip())
            md.append('%s\n' % dialog[0].text_content().strip())

            audio = tree.xpath('//audio')
            audio_url = url + audio[0].get('src').strip()[3:] # 去掉前面的../再拼接
            save_2_path = os.path.join(SAVE_FILE_TO_DIR, '%02d-%02d.mp3' % (category_no, dialog_no))
            # print('%s-->%s\n' % (save_2_path, audio_url) )
            mp3[save_2_path] = audio_url
        
    print("get_audio_info end")
    return md, mp3

from multiprocessing import Process, Queue, Pool
def batch_download(mp3_dict, processes=10):
    """ 并发下载所有图片 """
    start_time = time.time()
    pool = Pool(processes)
    for file_path, url in mp3_dict.items():
        pool.apply_async(download_one, (file_path, url))

    pool.close()
    pool.join()
    end_time = time.time()
    print('下载完毕,用时:%s秒' % (end_time - start_time))

def download_one(file_path, url):
    """ 下载一个文件 """
    # 如果文件已经存在，放弃下载
    if os.path.exists(file_path):
        print('exists:', file_path)
        return

    rsp = requests.get(url)
    print('start download', url)
    try:
        with open(file_path, 'wb') as f:
            f.write(rsp.content)
            print('end download', url)
    except Exception as err:
        print("type error: " + str(err))
        # print(traceback.format_exc())

def main():
    print('main start...')
    
    md_content, mp3_dict = get_audio_info()
    os.mkdir(SAVE_FILE_TO_DIR)
    with open("Speak English Fast.md", "w", encoding='utf-8') as f:
        f.write(''.join(md_content))
    batch_download(mp3_dict, processes=10)

    print('main end...')


if __name__ == '__main__':
    main()
