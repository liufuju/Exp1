from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Alignment_info(Page):
    form_model = 'player'
    form_fields = ['name', 'student_id', 'exp_date']


class Instruction(Page):
    pass


class Background(Page):
    def before_next_page(self):
        emotions = ['anger', 'sadness']
        emo_dscp = ['anger', 'sadness']
        self.participant.vars['emotions'] = emotions
        self.participant.vars['emo_dscp'] = emo_dscp

        self.participant.vars['age_year_later'] = self.player.age_year_later
        self.participant.vars['city'] = self.player.city

    form_model = 'player'
    form_fields = ['age_year_later', 'city']


page_sequence = [Alignment_info, Instruction, Background]
