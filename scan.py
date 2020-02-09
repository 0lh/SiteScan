import httpx
import asyncio
import time
from lib.cmdline import parse_args
from lib.queue_put import queue_put, q
from conf.config import COROS_NUM
from core.core import judge_site_status


async def main():
    argv = parse_args()
    urls_file = argv.urls
    queue_put(urls_file)
    async with httpx.AsyncClient(verify=False) as client:  # 创建session
        tasks = []
        for _ in range(COROS_NUM):
            task = judge_site_status(client, q)
            tasks.append(task)
        await asyncio.wait(tasks)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(f'耗时: {time.time() - start_time}')
