# coding: utf-8
# author: xiwu
# description: 多进程+协程，基于字典爆破子域名

import asyncio
import aiodns
from aiomultiprocess import Pool
from multiprocessing import cpu_count
import time


class Brute(object):
    def __init__(self, domain):
        # 获取cpu核心数
        self.processes = cpu_count()
        # 目标域名
        self.domain = domain

    # 子域名DNS解析
    async def dns_query(self, sub_domain):
        resolver = aiodns.DNSResolver(
            nameservers=["114.114.114.114", "223.5.5.5"], timeout=3)
        try:
            query_result = await resolver.query(sub_domain, 'A')
            return sub_domain, query_result[0].host
        except Exception as e:
            return None, None

    # 加载子域名文件
    async def load_sub_file(self):
        sub_file = "dict/subnames.txt"
        with open(sub_file, 'r') as f:
            sub_domain = list(
                set([sub.strip() + '.' + self.domain for sub in f]))

        # 创建多进程
        async with Pool(processes=self.processes, childconcurrency=20) as pool:
            results = await pool.map(self.dns_query, sub_domain)
        for result in results:
            print(result)
            with open('res.txt', 'w') as f:
                f.write(result)
                f.write('\n')

    def main(self):
        start_time = time.time()
        asyncio.run(self.load_sub_file())
        end_time = time.time()
        print("totoal: %f" % (end_time - start_time))


if __name__ == "__main__":
    b = Brute("youdao.com")
    b.main()
