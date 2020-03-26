# coding: utf-8
# author: xiwu
# description: 多进程+协程，基于字典爆破子域名

import asyncio
import aiodns
from aiomultiprocess import Pool
from multiprocessing import cpu_count
import time

# 获取cpu核心数
processes = cpu_count()


# 子域名DNS解析
async def dns_query(sub_domain):
    resolver = aiodns.DNSResolver(timeout=3)
    try:
        query_result = resolver.query(sub_domain, 'A')
        return sub_domain, query_result[0].host
    except Exception as e:
        return None, None


# 加载子域名文件
async def load_sub_file():
    domain = 'youdao.com'
    sub_file = "subnames.txt"
    with open(sub_file, 'r') as f:
        sub_domain = list(set([sub.strip() + '.' + domain for sub in f]))
        sub_domain_counts = len(sub_domain)

    # 创建多进程
    async with Pool(processes=processes, childconcurrency=20) as pool:
        results = await pool.map(dns_query, sub_domain)
    for result in results:
        print(result)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(load_sub_file())
    end_time = time.time()
    print("totoal: %f" % (end_time - start_time))
