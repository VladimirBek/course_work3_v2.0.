import json
from datetime import datetime

from src.operation_class import Operation


def get_last_operations(path, count):
    counter = 0
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        data = list(data)
    data = sorted(data,
                  key=lambda x: datetime.strptime(x.get("date", '2019-05-19T12:51:49.023880'), '%Y-%m-%dT%H:%M:%S.%f'))
    result = []
    while counter < count:
        counter += 1
        if data[-counter]['state'] == 'EXECUTED':
            try:
                result.append(Operation(data[-counter]['id'],
                                        state=data[-counter]['state'],
                                        date=data[-counter]['date'],
                                        amount=data[-counter]['operationAmount'],
                                        description=data[-counter]['description'],
                                        sender_acc=data[-counter]['from'],
                                        recipient_acc=data[-counter]['to']))

            except:
                result.append(Operation(data[-counter]['id'],
                                        state=data[-counter]['state'],
                                        date=data[-counter]['date'],
                                        amount=data[-counter]['operationAmount'],
                                        description=data[-counter]['description'],
                                        recipient_acc=data[-counter]['to']))

        else:
            count += 1
    return result


def show_operations(operations):
    res = []
    for op in operations:
        str_date, str_time = op.date.split('T')
        date = str_date.split('-')
        date = '.'.join(date[::-1])
        description = op.description
        sender_acc_num = op.sender_acc.split()[-1]
        sender_acc_card = op.sender_acc.split()[:-1]
        recipient_acc_num = op.recipient_acc.split()[-1]
        recipient_acc_card = op.recipient_acc.split()[:-1]
        amount = op.amount['amount']
        currency = op.amount['currency']['name']
        if sender_acc_card != []:
            res.append((f'{date} {description}\n'
                        f'{"".join(sender_acc_card)} {sender_acc_num[:4]} '
                        f'{sender_acc_num[4:6]}** **** {sender_acc_num[len(sender_acc_num) - 4:]} -> '
                        f'{"".join(recipient_acc_card)} **{recipient_acc_num[len(recipient_acc_num) - 4:]}\n'
                        f'{amount} {currency}\n'))
        else:
            res.append((f'{date} {description}\n'
                        f'{"".join(sender_acc_num[:6])}-> '
                        f'{"".join(recipient_acc_card)} **{recipient_acc_num[len(recipient_acc_num) - 4:]}\n'
                        f'{amount} {currency}\n'))

    return '\n'.join(res)
