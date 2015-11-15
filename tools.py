
import os
import subprocess
import pycurl
from io import BytesIO
import json
from urllib.parse import urlencode


def get_screen_resolution(location=None):
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4', shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    resolution = {'width': int(resolution[0]), 'height': int(resolution[1])}
    if location in resolution:
        return resolution[location]
    return resolution


def get_resource_path(rel_path):
    dir_of_py_file = os.path.dirname(__file__)
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource


def get_selected_text():
    sel = subprocess.Popen('xsel', shell=True, stdout=subprocess.PIPE).communicate()[0]
    return str(sel, encoding='UTF-8')


def curl(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(pycurl.HTTPHEADER, ['Referer: http://127.0.0.1/',
                                 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                                 'Chrome/44.0.2403.125 Safari/537.36'])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    return body.decode('utf-8')


def get_translate(q, sl, tl):
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&' + urlencode({'sl': sl}) + '&' + \
          urlencode({'tl': tl}) + '&' + urlencode({'hl': 'en-US'}) + '&' + urlencode({'dt': 't'}) + '&' + \
          urlencode({'dt': 'bd'}) + '&' + urlencode({'dj': '1'}) + '&' + urlencode({'source': 'icon'}) + '&' + \
          urlencode({'q': q})
    data = json.loads(curl(url))
    return data
