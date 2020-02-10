from bs4 import BeautifulSoup


def parse_title(response):
    '''
    解析 html title 或者 json文本
    '''
    if response.text:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        # print('soup', soup)
        if soup.title:
            title = soup.title.string
            return title
        elif response.headers.get('Content-Type', None):
            if 'json' in response.headers.get('Content-Type', None):
                return response.text
            else:
                return None
        else:
            return None
    else:
        return None
