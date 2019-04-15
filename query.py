# 导入域名查询类
import dns.resolver
import dns.exception
import functools


# 域名查询功能装饰器
def query(func):
    @functools.wraps(func)
    def wrapper(*args):
        try:
            answer = dns.resolver.query(args[0], rdtype='A')
            # print(answer)
        except dns.exception.Timeout:
            print("查询超时")
        except dns.resolver.NXDOMAIN:
            pass
            # print("没有对应A记录")
        except (dns.resolver.YXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            print("查询异常")
        if len(args)>1:
            return func(domain=args[0], answer=answer, wildcard_ip=args[1])
        else:
            return func(domain=args[0], answer=answer)

    return wrapper


@query
def domain_query(domain, answer, wildcard_ip):
    if not wildcard_ip:
        print(domain, end='')
        for record in answer.rrset.items:
            if record.address == wildcard_ip:
                continue
            print(',', end=' ')
            print(record.address, end='')


@query
def wildcard_dns_records(domain, answer):
    if answer:
        print(domain + "存在DNS泛解析")
        wildcard_ip = answer.rrset.items[0].address
        print(wildcard_ip)
        return wildcard_ip
    else:
        print("不存在DNS泛解析")


if __name__ == "__main__":
    ip = wildcard_dns_records("xubo.cheyipai.com")
    domain_query("123.cheyipai.com", ip)
