# animefun offline
Make online service "animefun"(also called "animategamer") content work offline.
## Requirement
### Python Modules
* requests
### Others
* ffmpeg with path added

## Usage
### Interactive
1. run `animefun.py`
2. type in the number `sn` from animefun URL params
3. wait for ad finishing
4. select a resolution by typing the number prompted
5. wait for downloading

### Command Line
```
animefun.py sn resolution_index_number
```

## Config
### Multiple Thread
This program's downloading function is multiple-thread-able.
By default, max number of threads are 1, you can adjust it depending on your condition, **REMEMBER don't make over load to animefun**.

### Cookies
If you are normal user of animefun (normal account or haven't login), you need to wait the 30s advertisment (actually the time server counts are about 25 second) and the maximum resolution is 720p (no logined also can get 720p, you can just see 360p in webpage because the UI hide the option higher then 360p).
But if you are VIP, you can try to get your cookie `BAHARUNE` from logined browser and put it in to `cookie.txt` like:
```
BAHARUNE=xxxxxxxx(your BAHARUNE cookie value)
```
Then I suppose you can access as VIP role to get the high resolution video and ignore advertisement(remove the AD part in program first).
_I have no VIP account to test so I just can guess_