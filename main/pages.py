from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import os, pandas, random

class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class Background(Page):
    def before_next_page(self):
        self.participant.vars['age_year_later'] = self.player.age_year_later
        self.participant.vars['city_later'] = self.player.city_later

    def is_displayed(self):
        criterion = self.round_number == 1
        return criterion

    form_model = 'player'
    form_fields = ['age_year_later', 'city_later']


class Composition(Page):
    def vars_for_template(self):
        pwd = os.getcwd()
        folder = 'reference'
        file_path = os.path.join(pwd, folder, 'composition.xlsx')
        cmp_data = pandas.read_excel(file_path)

        population = list(range(36))
        selection = random.sample(population, 3)
        information = []

        for i in selection:
            information += [[cmp_data['file'].iloc[i], cmp_data['ans'].iloc[i]]]

        self.player.cmp_file1, self.player.cmp_ans1 = information[0][0], information[0][1]
        self.player.cmp_file2, self.player.cmp_ans2 = information[1][0], information[1][1]
        self.player.cmp_file3, self.player.cmp_ans3 = information[2][0], information[2][1]

        return dict(
            cmp_pic1='compositions/' + self.player.cmp_file1,
            cmp_pic2='compositions/' + self.player.cmp_file2,
            cmp_pic3='compositions/' + self.player.cmp_file3
        )

    form_model = 'player'
    form_fields = ['cmp_response1', 'cmp_response2', 'cmp_response3']


class Emo_evoketion(Page):
    def vars_for_template(self):
        emotion = self.participant.vars['emotions'][self.round_number - 1]
        emo_dscp = self.participant.vars['emo_dscp'][self.round_number - 1]
        age = self.participant.vars['age_year_later']
        city_later = self.participant.vars['city_later']
        return dict(
            emotion=emotion,
            emo_dscp=emo_dscp,
            age=age,
            city_later=city_later,
            round_number=self.round_number
        )

    def before_next_page(self):
        self.player.emo = self.participant.vars['emotions'][self.round_number - 1]

    form_model = 'player'
    form_fields = ['short_dscp']


class Imagination(Page):
    def vars_for_template(self):
        event = self.player.short_dscp
        return dict(
            event=event
        )


class Question_filling(Page):
    form_model = 'player'
    form_fields = ['role_emo', 'self_emo', 'clear_emo']


class Description(Page):
    def vars_for_template(self):
        event = self.player.short_dscp
        return dict(
            event=event
        )

    form_model = 'player'
    form_fields = ['dscp_emo']


class Rest(Page):
    def is_displayed(self):
        A = self.round_number % 2 == 0
        B = self.round_number != len(self.participant.vars['emotions'])
        return A & B


page_sequence = [Instructions, Background, Composition, Emo_evoketion, Imagination, Question_filling, Description, Rest]
