import sys
from animefun import download_sn
from acgDetail import acgDetail

if __name__ == '__main__':
    # read sn from argv or stdin
    if len(sys.argv) > 1:
        sn = sys.argv[1]
        print('sn: %s' % sn)
    else:
        sn = input('sn: ')
    if len(sys.argv) > 2:
        resolution = int(sys.argv[2])
    else:
        resolution = None
    metadata = acgDetail(sn=sn, parse_metadata=True)
    download_sn(sn, resolution=resolution if resolution is not None else None, group_dir_name=metadata.name, method='mtd')