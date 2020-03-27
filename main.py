import os
import json
from tqdm import tqdm

from markov import MarkovChainTrigrams
from reporter import Reporter


mark_chain = MarkovChainTrigrams()

directory = 'fin_dataset/666_webhose-2015-07_20170904105917/'
for i in tqdm(os.listdir(directory)):
    with open(os.path.join(directory, i)) as file:
        mark_chain.add_text(json.load(file)['text'])

rep = Reporter(mark_chain)
print(rep.report_rouble())




