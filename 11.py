import os, json, itertools, random, pandas


def emo_dscp():
    pwd = os.getcwd()
    folder = 'reference'
    file = 'emo_dscp.js'

    file_path = os.path.join(pwd, folder, file)

    dict = {
        'amusement': '你碰到了很有意思、很搞笑的事情，或听到他人很幽默的话语，让你觉得很有乐趣',
        'desire': '你预期到未来会有很好的事情发生，你非常期待这件很好的事发生，并且强烈地觉得它将很快变成现实',
        'happy': '你身上发生了很好的事情在，你感到身心舒畅，非常高兴、愉悦、快乐',
        'relaxation': '你得到了此前很想要的东西，实现了很重要的目标，你觉得非常放松，惬意',
        'fear': '你遇到了危险，感受到了威胁，但是不知道该怎么应对，或者无法应对',
        'anger': '你很想做的事情、想要获得的东西被一些人或事物阻碍了，它们给你带来了很不好的影响',
        'sadness': '你永远地失去了对你而言很重要的物品，或一个对你而言很重要的人，且无力挽回',
        'bored': '你对正在进行的事情感到厌烦乏味，没有兴趣参与、不想继续'
    }

    with open(file_path, 'w', encoding='utf-8') as file_object:
        json.dump(dict, file_object)


def order_txt():
    pwd = os.getcwd()
    folder = 'reference'
    file = 'order.txt'
    file_path = os.path.join(pwd, folder, file)

    order = ['amusement', 'desire', 'happy', 'relaxation', 'fear', 'anger', 'sadness', 'bored']

    latin = []

    for i in range(8):
        latin.append(order)
        head = order.pop(0)
        order += [head]

    with open(file_path, 'w') as file_object:
        randomize = [str(i) for i in list(range(1, 9))]
        random.shuffle(randomize)
        file_object.write('\t'.join(randomize) + '\n')
        for i in range(8):
            file_object.write('\t'.join(order) + '\n')
            head = order.pop(0)
            order += [head]


def alphabet():
    dict = {
        '1': '你碰到了很有意思、很搞笑的事情，或听到他人很幽默的话语，让你觉得很有乐趣',
        '2': '你预期到未来会有很好的事情发生，你非常期待这件很好的事发生，并且强烈地觉得它将很快变成现实',
        'happy': '你身上发生了很好的事情在，你感到身心舒畅，非常高兴、愉悦、快乐',
        'relaxation': '你得到了此前很想要的东西，实现了很重要的目标，你觉得非常放松，惬意',
        'fear': '你遇到了危险，感受到了威胁，但是不知道该怎么应对，或者无法应对',
        'anger': '你很想做的事情、想要获得的东西被一些人或事物阻碍了，它们给你带来了很不好的影响',
        'sadness': '你永远地失去了对你而言很重要的物品，或一个对你而言很重要的人，且无力挽回',
        'bored': '你对正在进行的事情感到厌烦乏味，没有兴趣参与、不想继续'
    }

def order_retrieval():
    pwd = os.getcwd()
    emo_order_file = 'order.xlsx'
    folder = 'reference'
    order_path = os.path.join(pwd, folder, emo_order_file)

    order = []
    flag = 0
    order_data = pandas.read_excel(order_path, sheet_name=0)
    for i in range(4):
        if not flag:
            target = order_data[order_data['block'] == i]
            for j in range(8):
                if not flag:
                    row = target[target['code'] == j]
                    condition = int(row['condition'].iloc[0])
                    if condition == 0:
                        for emo in ['amusement', 'desire', 'happy', 'relaxation', 'fear', 'anger', 'sadness', 'bored']:
                            order.append(row[emo].iloc[0])
                        order_code = str(i) + str(j)
                        flag = 1
                        order_data['condition'].iloc[i * 8 + j] = 1
                    else:
                        continue
                else:
                    break
        else:
            break
    order_data.to_excel(order_path, sheet_name='sheet1')

    return order, order_code


order = order_retrieval()