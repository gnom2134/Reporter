import requests
import urllib
import random


class Reporter:
    def __init__(self, markov_chain):
        self.mc = markov_chain
        self.starts = [['top', 'news'], ['fresh', 'news'], ['turns', 'out'], ['news', ':']]
        self.ends_backwards = [['at', 'stopped', 'rate', 'exchange', 'ruble\'s', 'to', 'euro'], 
                     ['to', 'developed', 'ruble', 'to', 'rate', 'exchange', 'euro']]


    def __get_dollar_rouble_rate(self):
        host = 'https://api.exchangeratesapi.io'
        try:
            request = requests.get(f'{host}/latest')
            request.raise_for_status()
            result = request.json()
            return result['rates']['RUB']
        except requests.HTTPError as er:
            print(f'{er}')
            return 0


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
        rouble = self.__get_dollar_rouble_rate()
        end = random.choices(self.ends_backwards, k=1)[0]
        end.insert(0, str(rouble))
        start = random.choices(self.starts, k=1)[0]

        for _ in range(2):
            start.append(self.mc.predict_next(start[-2], start[-1]))
            end.append(self.mc.predict_prev(end[-2], end[-1]))

        start.append(self.mc.predict_mid(start[-1], end[-1]))

        report = ' '.join(start + end[::-1])

        if use_translator:
            report = self.__translate_to_russian(report)[0][0][0]

        report = self.__format_report(report)

        return report
