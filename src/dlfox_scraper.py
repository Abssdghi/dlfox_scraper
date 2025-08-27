import requests, json
from bs4 import BeautifulSoup


def get_posts(count=1, url="https://dlfox.com/wp-admin/admin-ajax.php"):
    '''
    increase the count to get more posts
    '''
    result = []
    
    for j in range(1,count+1):

        headers = {
            "User-Agent": "Mozilla/5.0",
        }

        data = {
            "action": "load_post_index",
            "count": str(j)
        }

        response = requests.post(url, headers=headers, data=data)
        page = response.text
        soup = BeautifulSoup(page, 'html.parser')
        posts = soup.find_all('div', {'class':'col-md-3 col-sm-3 col-xs-3 product_image'})

        for i in posts:
            result.append(i.find('a').get('href'))
        
    return result


def get_info(url="https://dlfox.com/fortnite/"):
    result = {
        'url':'',
        'title':'',
        'size':'',
        'version':'',
        'category':'',
        'desc':'',
        'system':'',
        'images':'',
        'download_links':'',
        'parts':'',
        'comments':''
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url=url, headers=headers).text

    soup = BeautifulSoup(page, 'html.parser')
    game = soup.find('div', {'class':'col-md-9 col-sm-9 col-xs-12 right_column'})
    content = game.find('div', {'class':'single_content'})

    # url
    result['url'] = url

    # title
    result['title'] = content.find('a',{'class':'mod_articles_category_title'}).text

    # size and version and category
    info = content.find('div', {'class':'widget_header'}).find_all('td')
    info_text = []
    for i in info:
        info_text.append(i.text)
    result['size'] = info_text[3]
    result['version'] = info_text[-1]
    result['category'] = info_text[5]

    # desc
    result['desc'] = content.find_all('p')[2].text

    # system
    try:
        result['system'] = content.find('div', {'class':'system_text'}).text
    except Exception as e:
        result['system'] = str(e)

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
    result['images'] = images

    # download_links
    links = []
    try:
        downloadbox = game.find('div', {'class':'bhoechie-tab-content active download1'})
        a_tags = downloadbox.find_all('a')
        for i in a_tags:
            links.append(i.get('href'))
    except Exception as e:
        links.append(str(e))
    result['download_links'] = links
    result['parts'] = len(links)

    # comments
    # comments = []
    # try:
    #     commentlist = game.find('ol', {'class':'comment-list'})
    #     commentbodies = commentlist.find_all('div', {'class':'comment-body'})
    #     for i in commentbodies:
    #         comments.append(i.get_text()[:len(i)-8])
    # except Exception as e:
    #     comments.append(str(e))  
    # result['comments'] = comments

    return result


def search(keyword="game", count=1):
    return dlfox_get_posts(count, f"https://dlfox.com/?s={keyword}")
