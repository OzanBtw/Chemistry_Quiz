import json

def renew():
    with open('source.json', 'r') as f:
        dic = json.load(f)


    all_formula = []
    all_names = []

    for i in [_ for _ in list(dic.keys()) if _ != 'All']:
        all_formula.extend(dic[i]['formula'])
        all_names.extend(dic[i]['names'])

    if len(all_formula) != len(all_names):
        print("bruh")
        for i in [_ for _ in list(dic.keys()) if _ != 'All']:
            print(len(dic[i]['formula']))
            print(len(dic[i]['names']))

            if len(dic[i]['formula']) == len(dic[i]['names']):
                continue
            print(f"There is a problem in '{i}'. Please check the 'source.json'")
            print(f"Number of 'formula': {len(dic[i]['formula'])}")
            print(f"Number of 'names': {len(dic[i]['names'])}")
            return False
        print("Can't identify the problem.")
        return False

    all_main = {'formula': all_formula, 'names': all_names}
    dic['All'] = all_main

    with open('source.json', 'w') as f:
        json.dump(dic, f, indent=2)
    return True


renew()