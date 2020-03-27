import requests
import urllib
import numpy as np


class Reporter:
    def __init__(self, markov_chain):
        self.mc = markov_chain
        self.rouble = 0
        self.starts = [['top', 'news'], ['fresh', 'news'], ['turns', 'out'], ['news', ':']]
        self.ends_backwards = [['at', 'stopped', 'rate', 'exchange', 'ruble\'s', 'to', 'euro'], 
                     ['to', 'developed', 'ruble', 'to', 'rate', 'exchange', 'euro']]


    def __get_dollar_rouble_rate(self):
        host = 'https://api.exchangeratesapi.io'
        try:
            request = requests.get(f'{host}/latest')
            request.raise_for_status()
            result = request.json()
            self.rouble = result['rates']['RUB']
        except requests.HTTPError as er:
            print(f'{er}')
            self.rouble = 0


    def __format_report(self, text):
        text = text[0].upper() + text[1:]
        if text[-1] != '.':
            text = text + '.'
        return text


    def __translate_to_russian(self, text):
        text = urllib.parse.quote(text, safe='~@#$&()*!+=:;,.?/\'')
        url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=' \
            + 'en' + '&tl=' + 'ru'+ '&dt=t&q=' + text
        try:
            request = requests.get(url)
            request.raise_for_status()
            result = request.json()
            return result
        except requests.HTTPError as er:
            print(f'{er}')
            return ''


    def report_rouble(self, use_translator=True):
        self.__get_dollar_rouble_rate()
        end = self.ends_backwards[np.random.choice(len(self.ends_backwards))].copy()
        end.insert(0, str(self.rouble))
        start = self.starts[np.random.choice(len(self.starts))].copy()

        for _ in range(2):
            start.append(self.mc.predict_next(start[len(start) - 2], start[len(start) - 1]))
            end.append(self.mc.predict_prev(end[len(end) - 2], end[len(end) - 1]))

        try:
            start.append(self.mc.predict_mid(start[len(start) - 1], end[len(end) - 1]))
        except ValueError as er:
            start.append('is that')

        for i in end[::-1]:
            start.append(i)

        report = ' '.join(start)

        if use_translator:
            report = self.__translate_to_russian(report)[0][0][0]

        report = self.__format_report(report)

        return report
