import requests
import bs4

class acgDetail:
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    def __init__(self, s: str=None, sn: str=None, parse_metadata: bool=False):
        self.sns = {}
        self.name = None
        if s is None and sn is None:
            raise Exception('s and sn cannot be both unspecified')
        if s is not None:
            self.s = s
            self.sn = self._parse_sn()
        else:
            self.sn = sn
        self._parse_eps()
        if self.name is None and parse_metadata:
            self._parse_sn()

    def _parse_sn(self):
        res = requests.get(f"https://acg.gamer.com.tw/acgDetail.php?s={self.s}", headers=self.HEADERS)
        res.raise_for_status()

        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        first_sn = bs.select('.seasonACG a')[0].attrs['href'].split('=')[1]

        self.name = bs.select('.ACG-mster_box1 h1')[0].text
        return first_sn
    
    def _parse_eps(self):
        res = requests.get(f"https://ani.gamer.com.tw/animeVideo.php?sn={self.sn}", headers=self.HEADERS)
        res.raise_for_status()


        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        self.sns = {x.text: x.attrs['href'].split('=')[1] for x in bs.select('.season a')}

        self.s = bs.select('a[href^="//acg.gamer.com.tw/acgDetail.php"]')[0].attrs['href'].split('=')[1]


if __name__ == '__main__':
    data = acgDetail(s='109289')
    print(data.sns)