a ={'123123':{'name': '에스케이바이오사이언스(유가)', 'type': 'kospi', 'day': '20210318', 'now_p': '136000', 'gongmo_p': '65000', 'sicho_p':'130000', 'first_p': '169000', 'code':'302440', 'jangwe_jonga': '170500', 'jabon': '38200000000', 'jusicsu':'76500000', 'akmyen': '500', 'sigachong': 4972500000000, 'd_1': '169000', 'd_2': '166500', 'd_3':'144000', 'd_4': '140500', 'd_5': '136500', 'd_30': '136000'}}

def dict_to_file(dic, filename ):
    with open(f'data/{filename}.csv', 'w') as f:
        list = []
        for i in [*dic[[*dic][0]]]:
            list.append(str(i))
            list.append(',')
        list[-1] = '\n'
        f.writelines(list)

        for i in [*dic]:
            list = []
            for ii in [*dic[i]]:
                list.append(str(dic[i][ii]))
                list.append(',')
            list[-1] = '\n'
            f.writelines(list)

dict_to_file(a,'shit')