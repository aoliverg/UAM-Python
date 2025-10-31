from transformers import pipeline

model_name = "Helsinki-NLP/opus-mt-en-es"
translator = pipeline("translation", model=model_name)
 
source_sentence = "This is a test sentence."
translation_result = translator(source_sentence)
translated_text = translation_result[0]['translation_text']
print(translated_text)