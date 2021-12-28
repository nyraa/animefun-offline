import random

def tocode62(n):
    return '01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'[n]

def generate_ck_gamer_ad_string(cookie_pos, ad_index):
    AD_LENGTH = 16
    ckstr = '-' * AD_LENGTH
    ckstr = ckstr[:cookie_pos] + tocode62(ad_index) + ckstr[cookie_pos + 1:]
    return ckstr

def get_major_ad():
    adlist = [['96969', 'https:\/\/www.gamer.com.tw\/adcounter.php?id=218556', '218556', 'video'], ['96969', 'https:\/\/www.gamer.com.tw\/adcounter.php?id=218793', '218793', 'video'], ['80900', '', '218413', 'facebook'], ['80900', '', '218412', 'facebook'], ['80900', '', '218411', 'facebook'], ['80900', '', '218410', 'facebook'], ['80900', '', '218409', 'facebook'], ['80900', '', '218408', 'facebook'], ['80900', '', '218407', 'facebook'], ['80900', '', '218406', 'facebook'], ['80900', '', '218402', 'facebook'], ['80900', '', '218403', 'facebook'], ['80900', '', '218404', 'facebook'], ['80900', '', '218405', 'facebook'], ['80900', '', '218414', 'facebook'], ['80900', '', '218415', 'facebook'], ['80900', '', '218416', 'facebook'], ['80900', '', '218417', 'facebook'], ['80900', '', '218418', 'facebook'], ['80900', '', '218419', 'facebook'], ['80900', '', '218420', 'facebook'], ['80900', '', '218421', 'facebook'], ['80900', '', '218509', 'facebook'], ['80900', '', '218510', 'facebook'], ['80900', '', '218511', 'facebook'], ['80900', '', '218512', 'facebook'], ['80900', '', '219093', 'facebook'], ['80900', '', '219092', 'facebook'], ['80900', '', '219091', 'facebook'], ['80900', '', '219085', 'facebook'], ['80900', '', '219086', 'facebook'], ['80900', '', '219087', 'facebook'], ['80900', '', '219088', 'facebook'], ['80900', '', '219089', 'facebook'], ['80900', '', '219090', 'facebook'], ['80900', '', '219193', 'facebook'], ['80900', '', '219194', 'facebook'], ['80900', '', '219195', 'facebook'], ['80900', '', '219269', 'facebook'], ['80900', '', '219270', 'facebook'], ['80900', '', '219271', 'facebook'], ['80900', '', '219272', 'facebook'], ['80900', '', '219273', 'facebook'], ['80900', '', '219274', 'facebook'], ['80900', '', '219286', 'facebook'], ['80900', '', '219287', 'facebook'], ['80900', '', '219288', 'facebook'], ['80900', '', '219291', 'facebook'], ['80900', '', '219275', 'facebook'], ['80900', '', '219276', 'facebook'], ['80900', '', '219277', 'facebook'], ['80900', '', '219278', 'facebook'], ['80900', '', '219279', 'facebook'], ['80900', '', '219280', 'facebook']]
    ad_index = random.randint(0, len(adlist) - 1)
    ckstr = generate_ck_gamer_ad_string(6, ad_index)
    return {'adsid': adlist[ad_index][2], 'cookie': {'ckBahaAd': ckstr}}