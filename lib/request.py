from httpx.exceptions import HTTPError
from lib.common import save_result
from conf.config import ERROR_LOG_PATH


async def get_req(client, url, redirect=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    try:
        response = await client.get(url, allow_redirects=redirect, headers=headers, timeout=15)
        if "30" in str(response.status_code):
            try:
                r = await get_req(client, url, redirect=True)
                if r:
                    if r.status_code in [200, 401, 403, 404, 415]:
                        return r
                    else:
                        return None
                else:
                    return None
            except HTTPError as e:
                output_item = f'{url} | {e}'
                await save_result(ERROR_LOG_PATH, output_item)
                return None
        return response
    except HTTPError as e:
        output_item = f'{url} | {e}'
        await save_result(ERROR_LOG_PATH, output_item)
        return None
