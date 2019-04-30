# 导入域名查询类
import dns.resolver
import dns.exception
import functools

# 字符集
char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
# 主域名
DOMAIN = "cheyipai.com"
# 子域名长度
SUB_DM_LEN = 3


# 域名查询功能装饰器
def query(func):
    @functools.wraps(func)
    def wrapper(*args):
        try:
            answer = dns.resolver.query(args[0], rdtype='A')
            # print(answer)
            if len(args) > 1:
                return func(domain=args[0], answer=answer, wildcard_ip=args[1])
            else:
                return func(domain=args[0], answer=answer)
        except dns.exception.Timeout:
            print("查询超时")
        except dns.resolver.NXDOMAIN:
            pass
            # print("没有对应A记录")
        except (dns.resolver.YXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            print("查询异常")
        # if len(args) > 1:
        #     return func(domain=args[0], answer=answer, wildcard_ip=args[1])
        # else:
        #     return func(domain=args[0], answer=answer)

    return wrapper


# 遍历输出一个子域名的A记录查询结果
@query
def domain_query(domain, answer, wildcard_ip):
    if not wildcard_ip:
        print(domain, end='')
        for record in answer.rrset.items:
            if record.address == wildcard_ip:
                continue
            print(',', end=' ')
            print(record.address, end='')


# 判断域名通配符解析wildcard records是否存在
@query
def wildcard_dns_records(domain, answer):
    if answer:
        print(domain + "存在DNS泛解析")
        wildcard_ip = answer.rrset.items[0].address
        print(wildcard_ip)
        return wildcard_ip
    else:
        print("不存在DNS泛解析")


# 使用递归遍历子域名
def travel(length, prefix, wildcard):
    for string in char_set:
        if length > len(string):
            new_prefix = prefix + string
            travel(length - len(string), new_prefix, wildcard)
        sub_str = prefix + string
        if len(sub_str) == SUB_DM_LEN:
            # print(sub_str)
            domain_query(sub_str + '.' + DOMAIN, wildcard)


if __name__ == "__main__":
    ip = wildcard_dns_records("xubo.cheyipai.com")
    domain_query("123.cheyipai.com", ip)
    # wildcard_ip = "210.74.2.227"
    travel(SUB_DM_LEN, '', ip)
