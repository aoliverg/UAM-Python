import codecs
import sys
import srx_segmenter
import regex
import stanza  

try:
    stanza.download('en')
except Exception as e:
    print(f"Error downloading the model: {e}")

def tag_segment(segment_text, pipeline):
    doc = pipeline(segment_text)    
    if not doc.sentences:
        return ""  
    tagged_tokens=[]
    for sentence in doc.sentences:
        for word in sentence.words:
            taggedtoken=word.text+"|"+word.pos
            tagged_tokens.append(taggedtoken)
            
    tagged_segment= " ".join(tagged_tokens)
    return(tagged_segment)


inputfilename = sys.argv[1]
outputfilename = sys.argv[2]
srxfile = "segment.srx"
srxlang = "English"

try:
    rules = srx_segmenter.parse(srxfile)
except FileNotFoundError:
    print(f"Error: Rule file not found '{srxfile}'", file=sys.stderr)
    sys.exit(1)

try:
    inputstream = codecs.open(inputfilename, "r", encoding="utf-8")
except FileNotFoundError:
    print(f"Error: Input file not found '{inputfilename}'", file=sys.stderr)
    sys.exit(1)
nlp = stanza.Pipeline('en', processors='tokenize,pos')

outputstream = codecs.open(outputfilename, "w", encoding="utf-8")

for linia in inputstream:
    linia = linia.rstrip()
    if not linia:  # Skip empty lines
        continue

    segmenter = srx_segmenter.SrxSegmenter(rules[srxlang], linia)
    segments = segmenter.extract()

    for segment in segments[0]:
        clean_segment = segment.strip()
        if clean_segment:
            tagged_output = tag_segment(clean_segment, nlp)
            print(tagged_output)
            outputstream.write(tagged_output+"\n")
            

inputstream.close()
outputstream.close()
