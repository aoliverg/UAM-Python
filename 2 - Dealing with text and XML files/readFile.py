import codecs
import sys

inputfilename=sys.argv[1]

inputstream=codecs.open(inputfilename,"r",encoding="utf-8")

for linia in inputstream:
    linia=linia.rstrip()
    print(linia)
    
