import requests, json
from bs4 import BeautifulSoup
from utils import *


def get_latest_posts(pagecount=1):
    '''
    increase the count to get more posts
    '''
    return get_dlfox_posts(count, "https://dlfox.com/wp-admin/admin-ajax.php")


def get_game_info(url="https://dlfox.com/fortnite/"):
    """
    Get a dlfox game info.

    Args:
        url (str): game page url.

    Returns:
        dict: Response in format:
        {
            "success": bool,
            "message": str,
            "data": {
                "url": str,
                "title": str,
                "size": str,
                "version": str,
                "category": str,
                "desc": str,
                "system": str,
                "images": [str],
                "download_links": [str],
                "parts": int
            }
        }
    """
    result = {
        "success": True,
        "message": "Operation successful",
        "data": {}
    }
    
    data = {
        "url": "",
        "title": "",
        "size": "",
        "version": "",
        "category": "",
        "desc": "",
        "system": "",
        "images": [""],
        "download_links": [""],
        "parts": 0
    }

    try:
        
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url=url, headers=headers).text

        soup = BeautifulSoup(page, 'html.parser')
        game = soup.find('div', {'class':'col-md-9 col-sm-9 col-xs-12 right_column'})
        content = game.find('div', {'class':'single_content'})
        
    except Exception as e:
        result["success"] = False
        result["message"] = e
        return result

    # url
    data['url'] = url

    # title
    data['title'] = content.find('a',{'class':'mod_articles_category_title'}).text

    # size and version and category
    info = content.find('div', {'class':'widget_header'}).find_all('td')
    info_text = []
    for i in info:
        info_text.append(i.text)
    data['size'] = info_text[3]
    data['version'] = info_text[-1]
    data['category'] = info_text[5]

    # desc
    data['desc'] = content.find_all('p')[2].text

    # system
    try:
        data['system'] = content.find('div', {'class':'system_text'}).text
    except Exception as e:
        data['system'] = str(e)

    # images
    images = []
    try:
        cover = content.find('img', {'decoding':'async'})
        images.append(cover.get('src'))
        game_images = content.find('div', {'class':'carousel-inner', 'role':'listbox'}).find_all('img')
        for i in game_images:
            images.append(i.get('src'))
    except Exception as e:
        images.append(str(e))
    data['images'] = images

    # download_links
    links = []
    try:
        downloadbox = game.find('div', {'class':'bhoechie-tab-content active download1'})
        a_tags = downloadbox.find_all('a')
        for i in a_tags:
            links.append(i.get('href'))
    except Exception as e:
        links.append(str(e))
    data['download_links'] = links
    data['parts'] = len(links)

    # comments
    # comments = []
    # try:
    #     commentlist = game.find('ol', {'class':'comment-list'})
    #     commentbodies = commentlist.find_all('div', {'class':'comment-body'})
    #     for i in commentbodies:
    #         comments.append(i.get_text()[:len(i)-8])
    # except Exception as e:
    #     comments.append(str(e))  
    # data['comments'] = comments

    result["data"] = data
    return result


def search(keyword="game", pagecount=1):
    return get_dlfox_posts(pagecount, f"https://dlfox.com/?s={keyword}")
