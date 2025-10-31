import codecs
import sys
import srx_segmenter
import regex
from transformers import pipeline


inputfilename=sys.argv[1]
outputfilename=sys.argv[2]

srxfile="segment.srx"
srxlang="English"

model_name = "Helsinki-NLP/opus-mt-en-es"
translator = pipeline("translation", model=model_name)

rules = srx_segmenter.parse(srxfile)

inputstream=codecs.open(inputfilename,"r",encoding="utf-8")
outputstream=codecs.open(outputfilename,"w",encoding="utf-8")

for linia in inputstream:
    linia=linia.rstrip()
    segmenter = srx_segmenter.SrxSegmenter(rules[srxlang],linia)
    segments=segmenter.extract() 
    liniatrad=[]
    contsegment=0
    for segment in segments[0]:
        print(segment)
        translation_result = translator(segment)
        translated_text = translation_result[0]['translation_text']
        print(translated_text)
        print("-------------------------")
        liniatrad.append(translated_text)
        liniatrad.append(segments[1][contsegment])
        contsegment+=1
    liniatrad="".join(liniatrad)   
    outputstream.write(liniatrad+"\n")
    
