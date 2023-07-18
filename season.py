import sys
from animefun import download_sn
from acgDetail import acgDetail

if __name__ == '__main__':
    # read sn from argv or stdin
    if len(sys.argv) > 1:
        s = sys.argv[1]
        print('s: %s' % s)
    else:
        s = input('sn: ')
    if len(sys.argv) > 2:
        resolution = int(sys.argv[2])
    else:
        resolution = input('resolution index (-1=highest): ')
    metadata = acgDetail(s=s, parse_metadata=True)
    for ep, sn in metadata.sns.items():
        download_sn(sn, resolution=resolution if resolution is not None else None, group_dir_name=metadata.name, ep_dir_name=f"{ep}_{{sn}}_{{resolution}}", method='mtd')