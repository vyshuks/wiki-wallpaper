import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

URL = "https://commons.wikimedia.org/wiki/Main_Page"

def get_image():
    response = requests.get(URL)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    main_div = soup.find(id="mainpage-potd")
    attrs = main_div.find("img").attrs
    srcset = attrs['srcset']
    return srcset.split(' ')[0]


def download_image(image_url):
    user = os.getenv('USER')
    file_name = dt.now().strftime("%Y-%m-%d") + ".jpg"
    path='/home/'+user+'/Pictures/wiki-wallpapers'
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path, file_name)

    with open(full_path, 'wb') as handle:
        response = requests.get(image_url, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    
    return full_path

def set_wallpaper(image_path):
    os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:///"+image_path)


if __name__ == "__main__":
    image = get_image()
    image_path = download_image(image)
    set_wallpaper(image_path)

