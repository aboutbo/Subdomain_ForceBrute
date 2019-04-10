# 导入域名查询类
import dns.resolver
import dns.exception


def domain_query(domain):
    try:
        answer = dns.resolver.query(domain, rdtype='A')
        # for ip in answer:
        #     print(domain)
        print(domain, end='')
        for record in answer.rrset.items:
            print(',', end=' ')
            print(record.address, end='')

    except dns.exception.Timeout:
        print("查询超时")
    except dns.resolver.NXDOMAIN:
        pass
        # print("没有对应A记录")
    except (dns.resolver.YXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        print("查询异常")


if __name__ == "__main__":
    domain_query("www.qiniu.com")
