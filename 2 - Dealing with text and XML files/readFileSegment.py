import codecs
import sys
import srx_segmenter
import regex


inputfilename=sys.argv[1]
srxfile=sys.argv[2]
srxlang=sys.argv[3]
outputfilename=sys.argv[4]

rules = srx_segmenter.parse(srxfile)

inputstream=codecs.open(inputfilename,"r",encoding="utf-8")
outputstream=codecs.open(outputfilename,"w",encoding="utf-8")

for linia in inputstream:
    linia=linia.rstrip()
    segmenter = srx_segmenter.SrxSegmenter(rules[srxlang],linia)
    segments=segmenter.extract() 
    for segment in segments[0]:
        print(segment)
        outputstream.write(segment+"\n")
    
