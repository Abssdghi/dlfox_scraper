from dlfox_scraper import get_latest_posts, get_game_info

MAX_GB = 10
print(f"Games larger than {MAX_GB}GB:")

response = get_latest_posts(pagecount=5)

if response['success']:
    for url in response['data']:
        game_info = get_game_info(url)
        
        if game_info['success']:
            game_data = game_info['data']
            size_str = game_data.get('size', '')
            
            try:
                parts = size_str.split()
                value = float(parts[0])
                unit = parts[1]
                
                size_in_gb = 0
                if unit == 'گیگابایت':
                    size_in_gb = value
                elif unit == 'مگابایت':
                    size_in_gb = value / 1024
                
                if size_in_gb > MAX_GB:
                    print(f"Found {game_data['title']} ({size_str})")

            except:
                print('error')
                continue