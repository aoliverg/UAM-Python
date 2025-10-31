from transformers import pipeline
import sys

model_name = "Helsinki-NLP/opus-mt-en-es"
translator = pipeline("translation", model=model_name)

while 1:
    source_sentence = input("Enter the sentence to translate or X to eXit: ")
    if source_sentence=="X" or source_sentence=="x":
        sys.exit()
    translation_result = translator(source_sentence)
    translated_text = translation_result[0]['translation_text']
    print(translated_text)