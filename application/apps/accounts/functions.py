# coding=utf-8
import re
import hmac
import hashlib


class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


def has_active_business_profile(user):
    """ user test """
    if user.get_userprofile():
        return bool(user.get_userprofile().active_profile_id)

#### Old pw crypt functions


def str_split(string, split_length=1):
    return filter(None, re.split('(.{1,%d})' % split_length, string))


def strrev(string):
    return string[::-1]


def old_pw_crypt(pw, nonce):
    #          'dr@se*uyuQech&pup#*_bAfrecra#avus#udra_par*yucREta=as8mefru7afuq9e!!buchedaye!9dusaRaj-f_g$haswutrus=yerachechuj7stec?=veb?th+ca'
    site_key = 'dr@se*uyuQech&pup#*_bAfrecra#avus#udra_par*yucREta=as8mefru7afuq9e!!buchedaye!9dusaRaj-f_g$haswutrus=yerachechuj7stec?=veb?th+ca'
    salt = str_split(strrev(nonce), 2)
    salt = [salt[0], salt[4], salt[13], salt[12], salt[15], salt[8], salt[2], salt[7], salt[10], salt[14], salt[6], salt[11], salt[1], salt[9], salt[5], salt[3]]
    data = "".join(salt)
    data = pw + data
    return hmac.new(site_key, data, hashlib.sha512).hexdigest()


# function encrypt_pw($pw, $nonce)
# {
#     $ci =& get_instance();

#     $salt = str_split(strrev($nonce), 2);
#     $salt = array($salt[0], $salt[4], $salt[13], $salt[12], $salt[15], $salt[8], $salt[2], $salt[7], $salt[10], $salt[14], $salt[6], $salt[11], $salt[1], $salt[9], $salt[5], $salt[3]);

#     return hash_hmac('sha512', $pw . implode($salt), $ci->config->item('site_key'));
# }


#### End old pw crypt functions
