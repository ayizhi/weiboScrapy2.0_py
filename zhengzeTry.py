import re
ustr = '"page_desc":"\u4e00\u4f4d\u7236\u4eb2\u544a\u8bc9\u513f\u5b50\u4ec0\u4e48\u624d\u662f\u771f\u6b63\u7684\u563b\u54c8\uff08\u5408\u96c6\uff09"}'
# r = re.compile(r'\\u\w{4}')
final = re.findall(r'\\u\w{4}',ustr)
print final