import requests
import os, sys, time
import json, re

import functions
import multiple_thread_downloading
from acgDetail import acgDetail

# header const
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70', 'referer': 'https://ani.gamer.com.tw/animeVideo.php', 'origin': 'https://ani.gamer.com.tw'}
session = requests.session()
session.headers.update(header)
deviceid = None

# read cookie from file
# paste your BAHARUNE cookie in cookie.txt if you want to download high resolution video
# BAHARUNE=YOUR_BAHARUNE_COOKIE
try:
    # cookies in k=v format
    with open('cookie.txt', 'r') as f:
        cookies = f.read().strip()
        cookies = {i.split('=')[0]: i.split('=')[1] for i in cookies.split('\n')}
        session.cookies.update(cookies)
except:
    print('cookies.txt not found')

# read sn from argv or stdin
if len(sys.argv) > 1:
    sn = sys.argv[1]
    print('sn: %s' % sn)
else:
    sn = input('sn: ')

def download_sn(sn: str, resolution: int=-1, method: str='mtd', download_dir_name: str='Downloads', ch_dir_name: str='.', ep_dir_name: str=sn, keep_tmp: bool=False):
    if not method in ['mtd', 'ffmpeg', 'aes128']:
        raise Exception('method must be one of mtd, ffmpeg, aes128')
    pass
    # get device id
    global deviceid
    deviceid_res = session.get(f"https://ani.gamer.com.tw/ajax/getdeviceid.php{'?id=' + deviceid if deviceid is not None else ''}")
    deviceid_res.raise_for_status()
    deviceid = deviceid_res.json()['deviceid']

    # get token
    res = session.get(f"https://ani.gamer.com.tw/ajax/token.php?sn={sn}&device={deviceid}")
    res.raise_for_status()
    token = res.json()

    if token['time'] == 0:
        # start ad
        ad_data = functions.get_major_ad()
        session.cookies.update(ad_data['cookie'])
        print('start ad')
        # session.get('https://ani.gamer.com.tw/ajax/videoCastcishu.php?s=%s&sn=%s' % (ad_data['adsid'], sn))
        session.get(f"https://ani.gamer.com.tw/ajax/videoCastcishu.php?s={ad_data['adsid']}&sn={sn}")
        ad_countdown = 25
        for countdown in range(ad_countdown):
            print(f'ad {ad_countdown - countdown}s remaining', end='\r')
            time.sleep(1)

        #end ad
        # session.get('https://ani.gamer.com.tw/ajax/videoCastcishu.php?s=%s&sn=%s&ad=end' % (ad_data['adsid'], sn))
        session.get(f"https://ani.gamer.com.tw/ajax/videoCastcishu.php?s={ad_data['adsid']}&sn={sn}&ad=end")
        print('end ad')

    # get m3u8 url form m3u8.php
    # m3u8_php_res = session.get('https://ani.gamer.com.tw/ajax/m3u8.php?sn=%s&device=%s' % (sn, deviceid))
    m3u8_php_res = session.get(f"https://ani.gamer.com.tw/ajax/m3u8.php?sn={sn}&device={deviceid}")
    m3u8_php_res.raise_for_status()
    try:
        playlist_basic_url = m3u8_php_res.json()['src']
    except Exception as ex:
        print(m3u8_php_res.text)
        print('failed to load m3u')
        exit()

    # get playlist_basic.m38u
    meta_base = os.path.dirname(playlist_basic_url) + '/'
    playlist_basic_res = requests.get(playlist_basic_url, headers=header)
    playlist_basic_res.raise_for_status()

    playlist_basic = playlist_basic_res.text.split('\n')

    # list all resolutions' metadata in list
    resolutions_metadata = []
    for i, line in enumerate(playlist_basic):
        if line.startswith('#EXT-X-STREAM-INF'):
            resolutions_metadata.append({'info': line[18:], 'url': playlist_basic[i+1]})

    # select a resolution from argv or stdin
    if resolution is not None and resolution < len(resolutions_metadata):
        print('selected resolution: %s' % resolutions_metadata[resolution]['info'])
    else:
        for j in range(len(resolutions_metadata)):
            print(f"#{j}: {resolutions_metadata[j]['info']}")
        # read selection from console
        resolution = int(input('select a resolution: '))

    # get resolution number for folder name(format ex: 1080x1920)
    resolution_number = resolutions_metadata[resolution]['info'].rsplit('=', 1)[1]

    # prepare work directory
    ep_basedir = os.path.join(download_dir_name, ch_dir_name, ep_dir_name)
    os.makedirs(ep_basedir, exist_ok=True)

    filename_base = f'{sn}_{resolution_number}'

    if method == 'mtd':
        tmp_dir = os.path.join(ep_basedir, 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)

        # get chunklist m3u8
        chunklist_res = requests.get(meta_base + resolutions_metadata[resolution]['url'], headers=header)

        # save chunklist to disk
        chunklist_filename = filename_base + '.m3u8'
        with open(os.path.join(tmp_dir, chunklist_filename), 'wb') as chunklist_file:
            for chunk in chunklist_res:
                chunklist_file.write(chunk)

        # base for the chunks
        # chunks_base = meta_base + resolutions_metadata[resolution]['url'].rsplit('/', 1)[0] + '/'
        chunks_base = f"{meta_base}{os.path.dirname(resolutions_metadata[resolution]['url'])}/"

        # parse chunklist.m3u8
        chunklist = chunklist_res.text.split('\n')
        mtd_worker = multiple_thread_downloading.mtd(header, chunks_base, chunklist_res.text.count('.ts'), tmp_dir)

        for k in range(len(chunklist)):
            line = chunklist[k]
            if line.startswith('#EXTINF'):
                ts_name = chunklist[k+1]
                # push
                mtd_worker.push(ts_name)
            elif line.startswith('#EXT-X-KEY'):
                key_name = re.match('.*URI="(.*)".*$', line).group(1)
                # push
                mtd_worker.push(key_name)
        # wait for all download thread finished
        mtd_worker.join()

        # call ffmpeg to combine all ts
        # os.system('ffmpeg -allowed_extensions ALL -i %s -c copy %s.mp4' % (chunklist_filename, folder_name))
        os.system(f'ffmpeg -allowed_extensions ALL -i {os.path.join(tmp_dir, chunklist_filename)} -c copy {os.path.join(ep_basedir, filename_base)}.mp4')


if __name__ == '__main__':
    metadata = acgDetail(sn=sn, parse_metadata=True)
    download_sn(sn, resolution=None, download_dir_name=metadata.name)