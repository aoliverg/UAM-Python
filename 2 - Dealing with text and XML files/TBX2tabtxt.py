import xml.etree.ElementTree as ET
import sys
import codecs
fentrada=sys.argv[1]
L1_LANG=sys.argv[2]
L2_LANG=sys.argv[3]
fsortida=sys.argv[4]


sortida=codecs.open(fsortida,"w",encoding="utf-8")
tree = ET.parse(fentrada)
root = tree.getroot()
namespaces = {
    'ns': 'urn:iso:std:iso:30042:ed-2',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

concept_entries = root.findall('.//ns:conceptEntry', namespaces)
for conceptEntry in concept_entries:
    l1_sec = conceptEntry.find(f'./ns:langSec[@xml:lang="{L1_LANG}"]', namespaces)
    l2_sec = conceptEntry.find(f'./ns:langSec[@xml:lang="{L2_LANG}"]', namespaces)
    if l1_sec is not None and l2_sec is not None:
        l1_term_elements = l1_sec.findall('.//ns:term', namespaces)
        l1_terms = [term.text.strip() for term in l1_term_elements if term.text]
  
        l2_term_elements = l2_sec.findall('.//ns:term', namespaces)
        l2_terms = [term.text.strip() for term in l2_term_elements if term.text]
      
        if l1_terms and l2_terms:
            l2_string = ", ".join(l2_terms)
            for l1_term in l1_terms:
                print(f"{l1_term}\t{l2_string}")
                sortida.write(f"{l1_term}\t{l2_string}\n")
        