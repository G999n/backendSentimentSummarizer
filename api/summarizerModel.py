import transformers
from transformers import pipeline
import json

summarizer = pipeline("summarization", model="G999n/my_awesome_billsum_model")

def summarize(input_value):
    output = summarizer(input_value)
    return output[0]['summary_text']

