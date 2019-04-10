from query import domain_query

# 字符集
char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
# 主域名
domain = "iqiyi.com"
# 子域名长度
SUB_DM_LEN = 3


# 使用递归遍历子域名
def travel(length, prefix):
    for string in char_set:
        if length > len(string):
            new_prefix = prefix + string
            travel(length - len(string), new_prefix)
        sub_str = prefix + string
        if len(sub_str) == SUB_DM_LEN:
            # print(sub_str)
            domain_query(sub_str + '.' + domain)


if __name__ == "__main__":
    travel(SUB_DM_LEN, '')
