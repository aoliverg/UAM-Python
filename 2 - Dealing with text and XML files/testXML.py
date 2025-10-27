import xml.etree.ElementTree as etree
import sys

xmlfile=sys.argv[1]

for event, elem in etree.iterparse(xmlfile,events=("start", "end")):
    print(event,elem,elem.tag,elem.attrib)