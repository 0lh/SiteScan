from lib.request import get_req
from lib.common import get_random_url, save_result
from lib.parse import parse_title
from conf.config import SAVE_FILE_01, SAVE_FILE_02, SAVE_FILE_03, SAVE_FILE_04, SAVE_FILE_05


async def judge_site_status(session, q):
    while not q.empty():
        root_url = q.get_nowait()
        random_url = get_random_url(root_url)
        random_url_response, root_url_response = await get_req(session, random_url), await get_req(session, root_url)
        if random_url_response and root_url_response:
            random_url_code, root_url_code = random_url_response.status_code, root_url_response.status_code
            title = parse_title(root_url_response)
            output_item = f'{root_url} | {str(root_url_code)} | {title}'
            if random_url_code == 400:
                if random_url.startswith('https'):
                    await save_result(SAVE_FILE_04, output_item)
                    # log(f'{root_url} 异常网站')
                else:
                    url_list = root_url.split('/')
                    https_url = "//".join(['https:', url_list[2]])
                    # log(f'[添加HTTPS] {https_url} 添加到queue')
                    q.put_nowait(https_url)
            elif random_url_code == 200:
                random_response_text = random_url_response.text
                if random_response_text:  # 页面内容有信息才继续执行
                    if "404.css" in random_response_text or "404.js" in random_response_text or "404.html" in random_response_text or "404" in random_response_text or "not found" in random_response_text:
                        await save_result(SAVE_FILE_03, output_item)
                        # log(f'{root_url} 小概率正常网站')
                    else:
                        '''判断 url_code 部分'''
                        if root_url_code == 200:  # random_url_code 和 url_code此时都为200，需要借助content-length判断
                            # todo rootdir_content_length:,若果没有则保存两个response_text,difflib库
                            random_content_length = random_url_response.headers.get('Content-Length', None)
                            root_content_length = root_url_response.headers.get('Content-Length', None)
                            if random_content_length or root_content_length:
                                if root_content_length == random_content_length:  # 相当则小概率网站正常
                                    await save_result(SAVE_FILE_03, output_item)
                                    # log(f'{root_url} 小概率正常网站')

                                else:  # conteng-length不想等说明网站有大概率正常，访问正常网站和随机url正常来说content-length就应该不一样
                                    await save_result(SAVE_FILE_02, output_item)
                                    # log(f'{root_url} 大概率正常网站')

                            else:
                                random_content_length = len(random_url_response.text)
                                root_content_length = len(root_url_response.text)
                                if root_content_length == random_content_length:  # 相当则小概率网站正常
                                    await save_result(SAVE_FILE_03, output_item)
                                    # log(f'{root_url} 小概率正常网站')
                                else:  # conteng-length不想等说明网站有大概率正常，访问正常网站和随机url正常来说content-length就应该不一样
                                    await save_result(SAVE_FILE_02, output_item)
                                    # log(f'{root_url} 大概率正常网站')
                        elif "30" in str(root_url_code):
                            await save_result(SAVE_FILE_01, output_item)
                            # log(f'{root_url} 正常网站')
                        elif root_url_code in [403, 404, 405]:
                            await save_result(SAVE_FILE_02, output_item)
                            # log(f'{root_url} 大概率正常网站')
                        elif root_url_code == 500:
                            await save_result(SAVE_FILE_03, output_item)
                            # log(f'{root_url} 小概率正常网站')
                        elif root_url_code in [501, 502, 503, 504]:
                            await save_result(SAVE_FILE_04, output_item)
                            # log(f'{root_url} 异常网站')
                        else:
                            await save_result(SAVE_FILE_05, output_item)
                            # log(f'{root_url} 少见响应码网站')
            elif random_url_code == 404:  # 判断 random_url_code 部分
                '''
                判断 url_code 部分
                '''
                if root_url_code == 200 or "30" in str(root_url_code):
                    await save_result(SAVE_FILE_01, output_item)
                    # log(f'{root_url} 正常网站')
                elif root_url_code in [403, 404, 415]:
                    await save_result(SAVE_FILE_02, output_item)
                    # log(f'{root_url} 大概率正常网站')
                elif root_url_code == 500:
                    await save_result(SAVE_FILE_03, output_item)
                    # log(f'{root_url} 小概率正常网站')
                elif root_url_code in [501, 502, 503, 504]:
                    await save_result(SAVE_FILE_04, output_item)
                    # log(f'{root_url} 异常网站')
                else:
                    await save_result(SAVE_FILE_05, output_item)
                    # log(f'{root_url} 少见响应码网站')
            elif random_url_code in [401, 415]:
                await save_result(SAVE_FILE_02, output_item)
                # log(f'{root_url} 401 网站')
            elif "30" in str(random_url_code):
                await save_result(SAVE_FILE_01, output_item)
                # log(f'{root_url} 正常网站')
            elif random_url_code in [403, 500]:
                await save_result(SAVE_FILE_03, output_item)
                # log(f'{root_url} 小概率正常网站')
            elif random_url_code in [501, 502, 503, 504]:
                await save_result(SAVE_FILE_04, output_item)
                # log(f'{root_url} 异常网站')
            else:
                await save_result(SAVE_FILE_05, output_item)
                # log(f'{root_url} 少见响应码网站')
