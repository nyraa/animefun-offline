import requests, json, os, re, time, sys
import functions

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70', 'referer': 'https://ani.gamer.com.tw/animeVideo.php', 'origin': 'https://ani.gamer.com.tw'}
cookie = {}

#open cookie
'''
with open('cookie.txt') as cookie_file:
    cookie_text = cookie_file.read().split('\n')
    cookie = {}
    for kv in cookie_text:
        if kv == '':
            continue
        k, v = kv.split('=', 1)
        cookie.setdefault(k, v)
'''

        
if len(sys.argv) > 1:
    sn = sys.argv[1]
    print('sn: %s' % sn)
else:
    sn = input('sn: ')

#get device id
deviceid_res = requests.get('https://ani.gamer.com.tw/ajax/getdeviceid.php', cookies=cookie, headers=header)
deviceid_res.raise_for_status()
cookie.update(deviceid_res.cookies.get_dict())
deviceid = json.loads(deviceid_res.text)['deviceid']

#start ad
ad_data = functions.get_major_ad()
cookie.update(ad_data['cookie'])
print('start ad')
requests.get('https://ani.gamer.com.tw/ajax/videoCastcishu.php?s=%s&sn=%s' % (ad_data['adsid'], sn), cookies=cookie, headers=header)
time.sleep(25)

#end ad
requests.get('https://ani.gamer.com.tw/ajax/videoCastcishu.php?s=%s&sn=%s&ad=end' % (ad_data['adsid'], sn), cookies=cookie, headers=header)
print('end ad')

#get m3u8 url (m3u8.php)
m3u_url_res = requests.get('https://ani.gamer.com.tw/ajax/m3u8.php?sn=%s&device=%s' % (sn, deviceid), cookies=cookie, headers=header)
m3u_url_res.raise_for_status()
try:
    m3u_url = json.loads(m3u_url_res.text)['src']
except Exception as ex:
    print(m3u_url_res.text)
    print('failed to load m3u')
    exit()

#get master m3u
base = os.path.dirname(m3u_url) + '/'
m3u_res = requests.get(m3u_url, headers=header)
m3u_res.raise_for_status()
master_m3u = m3u_res.text.split('\n')

resolutions = []

#list all resolutions
for i in range(len(master_m3u)):
    line = master_m3u[i]
    if line.startswith('#EXT-X-STREAM-INF'):
        resolutions.append({'info': line[18:], 'url': master_m3u[i+1]})

#select a resolution if no argv
if len(sys.argv) > 2:
    select_resolution = int(sys.argv[2])
    print('selected resolution: %s' % resolutions[select_resolution]['info'])
else:
    for j in range(len(resolutions)):
        print('#%s: %s' % (j, resolutions[j]['info']))

    select_resolution = int(input('select a resolution: '))

#get resolution description
resolution = re.match('^.*RESOLUTION=(\d+x\d+).*$', resolutions[select_resolution]['info']).group(1)

#switch folder
folder_name = '%s_%s' % (sn, resolution)
if not os.path.exists(folder_name) or not os.path.isdir(folder_name):
    os.mkdir(folder_name)
os.chdir(folder_name)

#get chunklist m3u
chunklist_res = requests.get(base + resolutions[select_resolution]['url'], headers=header)
chunklist_res.raise_for_status()

m3u_file_name = '%s.m3u8' % folder_name
chunklist_file = open(m3u_file_name, 'w')

chunklist = chunklist_res.text.split('\n')

file_counter = 1
file_list = []
skip_flag = False

for k in range(len(chunklist)):
    if skip_flag:
        skip_flag = False
        continue
    line = chunklist[k]
    if line.startswith('#EXTINF'):
        url = chunklist[k+1]
        chunklist_file.write(line + '\n')
        chunklist_file.write(re.match('(.*\..*)\?', url).group(1) + '\n')
        skip_flag = True
        file_list.append(base + url)
        
    elif line.startswith('#EXT-X-KEY'):
        key_uri = re.match('.*URI="(.*)"$', line).group(1)
        key_res = requests.get(key_uri, headers=header)
        key_res.raise_for_status()
        with open(re.match('(.*\..*)\?', os.path.basename(key_uri)).group(1), 'wb') as key_file:
            for chunk in key_res.iter_content(1024):
                key_file.write(chunk)
        chunklist_file.write(re.sub('^(.*URI=").*/(.*)\.m3u8key.*"$', r'\1\2.m3u8key"\n', line))
    else:
        chunklist_file.write(line + '\n')

chunklist_file.close()
file_count = len(file_list)
for file in file_list:
    #break
    print('%s/%s...' % (file_counter, file_count), end='')
    file_counter += 1
    ts_res = requests.get(file, headers=header)
    ts_res.raise_for_status()
    ts_name = re.match('(.*\..*)\?', os.path.basename(file)).group(1)
    with open(ts_name, 'wb') as ts:
        for chunk in ts_res.iter_content(100000):
            ts.write(chunk)
    print('done')

os.system('ffmpeg -allowed_extensions ALL -i %s -c copy %s.mp4' % (m3u_file_name, folder_name))
