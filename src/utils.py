import requests, json
from bs4 import BeautifulSoup

def get_dlfox_posts(count=1, url="https://dlfox.com/wp-admin/admin-ajax.php"):  
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