import sys
import re
import os

ESCAPE_MAP = {
    "'": "\'",
    "+": "\+",
}

def get_change(line):
    amount = float(line.split(',')[1].strip('"'))
    return amount, amount > 0

def get_category(line, regex_patterns):
    description = line.split(',')[2].lower()
    
    for regex, cat in regex_patterns.items():
        if re.search(regex, description): return cat
    print(description)
    return 'uncategorized'

def get_category_patterns():
    regex_patterns = {}
    for category_file in os.listdir('categories'):
        category = category_file.split('.')[0]
        with open(f'categories/{category_file}', 'rt') as cat_file:
            entries = [fr'\b{vendor.strip().translate(ESCAPE_MAP)}\b' for vendor in cat_file]
            regex = '|'.join(entries)
            regex_patterns[regex] = category
    return regex_patterns

if __name__ == "__main__":
    values = {}
    regex = get_category_patterns()
    net_calc = {
        'income': [],
        'expense': [],
    }
    with open(sys.argv[1], 'rt') as csv:
        for line in csv:
            category = get_category(line, regex)
            amount, is_income = get_change(line)
            if is_income: net_calc['income'].append(amount)
            else: net_calc['expense'].append(-amount)
            if category not in values: values[category] = []
            values[category].append(amount)
    for category in values:
        print(f'{category:<40} {len(values[category]):<5} ${round(sum(values[category]), 2):>8}')
    income = round(sum(net_calc['income']), 2)
    expense = round(sum(net_calc['expense']), 2)
    print('TOTAL INCOME: $', income)
    print('TOTAL EXPENSE: $(', expense, ')')
    print('NET INCOME: $', round(income - expense, 2))