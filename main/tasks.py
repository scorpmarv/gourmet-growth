from datetime import datetime
import json
import os


def json_to_dict():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, '../transactions.json')
    with open(file_path, 'r') as f:
        transactions_dict = json.load(f)
        return transactions_dict


def try_strptime(s, fmts=['%m/%d/%Y']):
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except:
            continue
    return None


def similar(w1, w2):
    w1 = w1 + ' ' * (len(w2) - len(w1))
    w2 = w2 + ' ' * (len(w1) - len(w2))
    return sum(1 if i == j else 0 for i, j in zip(w1, w2)) / float(len(w1))


def compare_date(current_list, transactions):
    days_list = []
    difference_list = []
    total_sets = []
    for item in current_list:
        days_list.append([item, transactions.get(id=item).date])
    for i in range(len(days_list)):
        if i + 1 < len(days_list):
            difference_list.append([[days_list[i][0], days_list[i + 1][0]],
                                    (days_list[i + 1][1] - days_list[i][1]).days])
    if len(difference_list) > 2:
        current_set = [[]]
        index = 0
        original_gap = 0
        for i in range(len(difference_list)):
            if i + 1 < len(difference_list):
                if original_gap == 0:
                    original_gap = difference_list[i][1]
                days_gap = abs(original_gap - difference_list[i+1][1])
                if days_gap < 4:
                    current_set[index] = current_set[index] + difference_list[i][0] + difference_list[i + 1][0]
                else:
                    index += 1
                    original_gap = 0
                    current_set.append([])
        for id_set in current_set:
            id_list = list(set(id_set))
            if len(id_list) > 3:
                total_sets.append(id_list)
    return total_sets


def compare(transactions):
    checked = []
    final_sets = []
    for i in range(len(transactions)):
        if transactions[i].id in checked:
            continue
        checked.append(transactions[i].id)
        j = i + 1
        w1 = transactions[i].description
        current_list = [transactions[i].id]
        while j < len(transactions):
            if transactions[j].id in checked:
                j += 1
                continue
            w2 = transactions[j].description
            similarity = similar(w1, w2)
            if similarity >= 0.5:
                checked.append(transactions[j].id)
                current_list.append(transactions[j].id)
            j += 1
        sets = compare_date(current_list, transactions)
        for current_set in sets:
            if len(current_set) > 3:
                final_sets.append(current_set)
    return final_sets
