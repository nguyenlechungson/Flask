import difflib
from pprint import pprint
import json

def so_sanh_string():
    a = 'ngày tốt, tháng tốt, năm tốt'
    b = 'bạn cho hỏi: ngày tốt nào trong tháng tốt nhất này ?.'
    print(a)
    print(b)
    result = difflib.SequenceMatcher(None,a,b).ratio()
    result_2 = difflib.SequenceMatcher(None,a,b)
    consquec = []
    dict_consquec = {}
    for tag, i1, i2, j1, j2 in result_2.get_opcodes():
        print('{:7}   a[{}:{}] --> b[{}:{}] {!r:>8} --> {!r}'.format(tag, i1, i2, j1, j2, a[i1:i2], b[j1:j2]))

        if tag =='equal':
            key = tag
            value = b[j1:j2]
            dict_consquec={key:value}
            consquec.append(dict_consquec)

    print(consquec)
        
so_sanh_string()