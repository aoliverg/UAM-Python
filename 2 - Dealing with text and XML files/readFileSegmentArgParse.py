import codecs
import argparse  # 1. Import argparse
import srx_segmenter
import regex
# import sys (No longer needed for arguments)

# --- Argparse Setup ---
# 2. Create the parser object
parser = argparse.ArgumentParser(
    description="Segments a text file line by line using SRX rules."
)

# 3. Add the arguments (replacing sys.argv)
parser.add_argument(
    "-i", "--input",
    required=True,  # This argument is mandatory
    help="The input text file to segment.",
    metavar="INPUT_FILE"  # Name shown in help message
)
parser.add_argument(
    "-s", "--srx",
    required=True,  # This argument is mandatory
    help="The SRX rules file (e.g., segmentation.srx).",
    metavar="SRX_FILE"
)
parser.add_argument(
    "-l", "--lang",
    required=True,  # This argument is mandatory
    help="The language code from the SRX file to use (e.g., en, ca).",
    metavar="LANG_CODE"
)
# 4. Add the new output file argument
parser.add_argument(
    "-o", "--output",
    required=True,  # This argument is mandatory
    help="The file to write the segmented output to.",
    metavar="OUTPUT_FILE"
)

# 5. Process the arguments provided by the user
args = parser.parse_args()

# 6. Assign the parsed arguments to variables
inputfilename = args.input
srxfile = args.srx
srxlang = args.lang
outputfilename = args.output  # The new output file path

# --- Main Script Logic ---

# It's good practice to add error handling
try:
    rules = srx_segmenter.parse(srxfile)
    
    # Check if the language exists before opening files
    if srxlang not in rules:
        print(f"Error: Language '{srxlang}' not found in SRX file '{srxfile}'.")
        print(f"Available languages: {list(rules.keys())}")
        exit() # Exit the script

    # 7. Use 'with' for both input and output files
    # This ensures both are closed properly, even if an error occurs
    with codecs.open(inputfilename, "r", encoding="utf-8") as inputstream, \
         codecs.open(outputfilename, "w", encoding="utf-8") as outputstream:
        
        print(f"Processing '{inputfilename}'...")

        for linia in inputstream:
            linia = linia.rstrip()
            if not linia:  # Skip empty lines
                continue
                
            segmenter = srx_segmenter.SrxSegmenter(rules[srxlang], linia)
            segments = segmenter.extract()
            
            # segments[0] contains the list of segments
            if segments and segments[0]:
                for segment in segments[0]:
                    # As in your script, print to console *and* write to file
                    print(segment)
                    outputstream.write(segment + "\n")
        
        print(f"Successfully segmented text to '{outputfilename}'.")

except FileNotFoundError:
    print(f"Error: File not found. Check paths for: {inputfilename} or {srxfile}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
