import requests
import os, sys, time
import json, re

import functions
import multiple_thread_downloading

# header const
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70', 'referer': 'https://ani.gamer.com.tw/animeVideo.php', 'origin': 'https://ani.gamer.com.tw'}
cookie = {}

# read cookie from file
# use it if you are VIP or some situation you need
# remove the comment mark '''
'''
with open('cookie.txt') as cookie_file:
    cookie_text = cookie_file.read().split('\n')
    for kv in cookie_text:
        if kv == '':
            continue
        k, v = kv.split('=', 1)
        cookie.setdefault(k, v)
'''

# read sn from argv or stdin
if len(sys.argv) > 1:
    sn = sys.argv[1]
    print('sn: %s' % sn)
else:
    sn = input('sn: ')

# get device id
deviceid_res = requests.get('https://ani.gamer.com.tw/ajax/getdeviceid.php', cookies=cookie, headers=header)
deviceid_res.raise_for_status()
cookie.update(deviceid_res.cookies.get_dict())
deviceid = json.loads(deviceid_res.text)['deviceid']

# start ad
ad_data = functions.get_major_ad()
cookie.update(ad_data['cookie'])
print('start ad')
requests.get('https://ani.gamer.com.tw/ajax/videoCastcishu.php?s=%s&sn=%s' % (ad_data['adsid'], sn), cookies=cookie, headers=header)
ad_countdown = 25
for countdown in range(ad_countdown):
    print(f'ad {ad_countdown - countdown}s remaining', end='\r')
    time.sleep(1)

#end ad
requests.get('https://ani.gamer.com.tw/ajax/videoCastcishu.php?s=%s&sn=%s&ad=end' % (ad_data['adsid'], sn), cookies=cookie, headers=header)
print('end ad')

# get m3u8 url form m3u8.php
m3u8_php_res = requests.get('https://ani.gamer.com.tw/ajax/m3u8.php?sn=%s&device=%s' % (sn, deviceid), cookies=cookie, headers=header)
m3u8_php_res.raise_for_status()
try:
    playlist_basic_url = json.loads(m3u8_php_res.text)['src']
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
for i in range(len(playlist_basic)):
    line = playlist_basic[i]
    if line.startswith('#EXT-X-STREAM-INF'):
        resolutions_metadata.append({'info': line[18:], 'url': playlist_basic[i+1]})

# select a resolution from argv or stdin
if len(sys.argv) > 2:
    selected_resolution = int(sys.argv[2])
    print('selected resolution: %s' % resolutions_metadata[selected_resolution]['info'])
else:
    for j in range(len(resolutions_metadata)):
        print('#%s: %s' % (j, resolutions_metadata[j]['info']))
    # read selection from console
    selected_resolution = int(input('select a resolution: '))

# get resolution number for folder name
resolution_number = resolutions_metadata[selected_resolution]['info'].rsplit('=', 1)[1]

# change working path
folder_name = f'{sn}_{resolution_number}'
os.makedirs(os.path.join('Download', folder_name), exist_ok=True)
os.chdir(os.path.join('Download', folder_name))

# get chunklist m3u8
chunklist_res = requests.get(meta_base + resolutions_metadata[selected_resolution]['url'], headers=header)

# save chunklist to disk
chunklist_filename = folder_name + '.m3u8'
with open(chunklist_filename, 'wb') as chunklist_file:
    for chunk in chunklist_res:
        chunklist_file.write(chunk)

# base for the chunks
chunks_base = meta_base + resolutions_metadata[selected_resolution]['url'].rsplit('/', 1)[0] + '/'

# parse chunklist.m3u8
chunklist = chunklist_res.text.split('\n')
mtd_worker = multiple_thread_downloading.mtd(header, chunks_base, chunklist_res.text.count('.ts'))

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
os.system('ffmpeg -allowed_extensions ALL -i %s -c copy %s.mp4' % (chunklist_filename, folder_name))
