from query import domain_query

# 字符集
char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
# 主域名
domain = "cheyipai.com"
# 子域名长度
SUB_DM_LEN = 3


# 使用递归遍历子域名
# todo:使用装饰器遍历查询

def travel(length, prefix, wildcard):
    for string in char_set:
        if length > len(string):
            new_prefix = prefix + string
            travel(length - len(string), new_prefix, wildcard)
        sub_str = prefix + string
        if len(sub_str) == SUB_DM_LEN:
            # print(sub_str)
            domain_query(sub_str + '.' + domain, wildcard)


if __name__ == "__main__":
    wildcard_ip = "210.74.2.227"
    travel(SUB_DM_LEN, '', wildcard_ip)
