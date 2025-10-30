import re
from collections import Counter
import sys

def find_patterns(tagged_text, tag_patterns):
    tags = ' '.join(item.split('|')[1] for item in tagged_text.split())
    forms = [item.split('|')[0] for item in tagged_text.split()]
    found_sequences = []
    for tag_pattern in tag_patterns:
        reggex_pattern = re.compile(tag_pattern.replace(' ', r'\s+'))
        for match in reggex_pattern.finditer(tags):
            start, end = match.span()
            index_start_form = tags[:start].count(' ')
            index_end_form = index_start_form + tag_pattern.count(' ') + 1
            seq_forms = forms[index_start_form:index_end_form]
            found_sequences.append(' '.join(seq_forms))
    frequency = Counter(found_sequences)
    return dict(frequency)
    

patterns = ["NOUN NOUN","NOUN NOUN NOUN","ADJ NOUN","ADJ ADJ NOUN"]

inputfile=sys.argv[1]
outputfile=sys.argv[2]

total_frequency = Counter()

inputstream=open(inputfile, 'r', encoding='utf-8')
outputstream=open(outputfile, 'w', encoding='utf-8')

for line in inputstream:
    tagged_sentence = line.strip()
    line_frequencies = find_patterns(tagged_sentence, patterns)
    total_frequency.update(line_frequencies)
    
sorted_results = total_frequency.most_common()

for term in sorted_results:
    freqterm=str(term[1])+"\t"+term[0]
    print(freqterm)
    outputstream.write(freqterm+"\n")