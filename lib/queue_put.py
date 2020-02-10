import asyncio

q = asyncio.Queue()


def get_urls(urls_file):
    with open(urls_file, 'r', encoding='utf-8') as f:
        for url in f:
            yield url.rstrip('\n').strip()


def queue_put(urls_file):
    urls = get_urls(urls_file)
    for url in urls:
        if url.endswith(':443'):
            q.put_nowait(f'https://{url}')
            print(f"https://{url} 正在导入")
        else:
            q.put_nowait(f'http://{url}')
            print(f"http://{url} 正在导入")
