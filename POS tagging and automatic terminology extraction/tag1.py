import stanza

try:
    stanza.download('en')
except Exception as e:
    print(f"Error downloading the model: {e}")

nlp = stanza.Pipeline('en', processors='tokenize,pos')
text = "The quick brown fox jumps over the lazy dog."
doc = nlp(text)

for sentence in doc.sentences:
    for word in sentence.words:
        print(word.text,word.pos,)