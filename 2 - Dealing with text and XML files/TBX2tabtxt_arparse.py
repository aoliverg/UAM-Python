import xml.etree.ElementTree as ET
import codecs
import argparse  # Import argparse
import sys       # We keep it for sys.exit on error

def main():
    # 1. Setup Argparse
    parser = argparse.ArgumentParser(
        description="Extracts L1/L2 term pairs from a TBX (IATE) file to a tab-separated format.",
        epilog="Example usage: python script.py -i my_file.tbx -l1 en -l2 es -o output.txt"
    )
    
    # Define the arguments the script will accept
    parser.add_argument(
        "-i", "--input", 
        dest="input_file",  # The variable name in 'args'
        required=True,      # This argument is mandatory
        help="Input XML (TBX) file."
    )
    parser.add_argument(
        "-l1", "--lang1", 
        dest="l1_lang", 
        required=True, 
        help="L1 language code (e.g., 'en')."
    )
    parser.add_argument(
        "-l2", "--lang2", 
        dest="l2_lang", 
        required=True, 
        help="L2 language code (e.g., 'es')."
    )
    parser.add_argument(
        "-o", "--output", 
        dest="output_file", 
        required=True, 
        help="Output file (tab-separated text)."
    )
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # 2. Define the namespaces
    namespaces = {
        'ns': 'urn:iso:std:iso:30042:ed-2',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }

    # 3. Process the file
    try:
        print(f"Processing file: {args.input_file}...")
        
        # Use 'with' to open the output file. It will be closed automatically.
        with codecs.open(args.output_file, "w", encoding="utf-8") as output_stream:
            
            # Parse the input file
            tree = ET.parse(args.input_file)
            root = tree.getroot()

            concept_entries = root.findall('.//ns:conceptEntry', namespaces)
            count = 0

            for conceptEntry in concept_entries:
                # Find the sections using the arguments from 'args'
                l1_sec = conceptEntry.find(f'./ns:langSec[@xml:lang="{args.l1_lang}"]', namespaces)
                l2_sec = conceptEntry.find(f'./ns:langSec[@xml:lang="{args.l2_lang}"]', namespaces)
                
                # Check if both language sections exist
                if l1_sec is not None and l2_sec is not None:
                    # Get all L1 terms
                    l1_term_elements = l1_sec.findall('.//ns:term', namespaces)
                    l1_terms = [term.text.strip() for term in l1_term_elements if term.text]
            
                    # Get all L2 terms
                    l2_term_elements = l2_sec.findall('.//ns:term', namespaces)
                    l2_terms = [term.text.strip() for term in l2_term_elements if term.text]
                    
                    # If we have terms in both lists, write them
                    if l1_terms and l2_terms:
                        l2_string = ", ".join(l2_terms)
                        for l1_term in l1_terms:
                            # Write to the output file (not 'print')
                            # Add a newline character '\n'
                            output_stream.write(f"{l1_term}\t{l2_string}\n")
                            count += 1

        print(f"Process complete. Written {count} lines to {args.output_file}.")

    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except ET.ParseError as e:
        print(f"Error: Could not parse XML in '{args.input_file}'. Detail: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error: Could not write to output file '{args.output_file}'. Detail: {e}", file=sys.stderr)
        sys.exit(1)

# Good practice: run 'main' only if the script is executed directly
if __name__ == "__main__":
    main()