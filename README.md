# animefun offline
Make online service "animefun"(also called "animegamer") content work offline.
## Requirement
### Python Modules
* requests
### Others
* ffmpeg and added to path

## Usage
### Interactive - single episode
1. run `single.py`
2. type in the number `sn` from animefun URL params
3. wait for ad finishing(if no vip cookie provided)
4. select a resolution by typing the number prompted
5. wait for downloading

### Interactive - whole season(not recommended)
1. run `season.py`
2. type in the number `s` from acgDetail URL params
3. select a resolution by typing the index number(-1 for highest resolution)
4. wait for ad finishing(if no vip cookie provided)
5. wait for downloading
6. repeat 4~5 until all episodes are downloaded

### Command Line - single episode
```
single.py sn resolution_index_number
```

### Command Line - whole season
```
animefun.py sn resolution_index_number
```
`resolution_index_number`: 0 for 360p, 1 for 640p, 2 for 720p, 3 for 1080p, -1 for highest resolution

## Config
### Multiple Thread
This program's downloading function is multiple-thread-able.  
By default, max number of threads are 10, you can adjust it depending on your condition, **REMEMBER don't make over load to animefun**.

### Cookies
If you are normal user of animefun (normal account or haven't login), you need to wait the 30s advertisment (actually the time server counts about 25 second) and the maximum resolution is 720p (after an update, no login user can only get 360p video).
If you want to get 720p video, you need to put your `BAHARUNE` cookie in cookie.txt like following:
```
BAHARUNE=xxxxxxxx(your BAHARUNE cookie value)
```
If you have VIP, 1080p video is available when you provide `BAHARUNE` cookie.