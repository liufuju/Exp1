from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import os, json, pandas

class Alignment_info(Page):
    form_model = 'player'
    form_fields = ['name', 'student_id', 'exp_date']


class Instruction(Page):
    def before_next_page(self):
        pwd = os.getcwd()
        emo_order_file = 'order.xlsx'
        dscp_file = 'emo_dscp.js'

        folder = 'reference'
        dscp_path = os.path.join(pwd, folder, dscp_file)
        order_path = os.path.join(pwd, folder, emo_order_file)

        with open(dscp_path, 'r', encoding='utf-8') as file_object:
            dscp_data = json.load(file_object)

        unordered = ['amusement', 'desire', 'happy', 'relaxation', 'fear', 'anger', 'sadness', 'bored']
        order, order_code = order_retrieval(order_path)

        emotions = [unordered[i] for i in order]
        emo_dscp = [dscp_data[i] for i in emotions]

        self.participant.vars['emotions'] = emotions
        self.participant.vars['emo_dscp'] = emo_dscp

        self.player.emo_order = '_'.join(emotions)
        self.player.emo_order_code = order_code


page_sequence = [Instruction, Alignment_info]


def order_retrieval(order_path):
    emotions = ['amusement', 'desire', 'happy', 'relaxation', 'fear', 'anger', 'sadness', 'bored']
    order = []
    order_code = '0'
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
                        for emo in emotions:
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
    order_data.to_excel(order_path, sheet_name='sheet1', columns=['block', 'code', 'condition'] + emotions)

    return order, order_code