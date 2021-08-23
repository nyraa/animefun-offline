# animefun-offline
make online animefun content work offline  
(you know it)

## requirement
### python
* requests
### others
* ffmpeg that be added in path

## usage
### interactive
1. run `animefun.py`
2. input the number `sn` from animefun URL param
3. wait for ad finishing
4. select a resolution  
5. download will starts, finally it will be a `sn.mp4`

### command line
```
animefun.py sn resolution_index
```

## limits
need to wait for 25sec AD timer  
I have no vip account to test 1080p, so now there highest resolution is 720p
