import random
import aiofiles


def gen_random_url(root_url: str) -> str:
    '''
    生成随机url
    '''
    random_string = '/' + \
                    "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 9))
    random_url = root_url + random_string
    return random_url


async def save_result(output_file, output_item: str):
    async with aiofiles.open(output_file, mode='a+', encoding='utf-8') as f:
        await f.write(f'{output_item}\n')
