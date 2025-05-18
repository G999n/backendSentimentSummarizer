from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import logging

from .sentimentModel import infer_sentiment
from .summarizerModel import summarize

logger = logging.getLogger(__name__)

@csrf_exempt
def sentiment(request):
    if request.method != "POST":
        return JsonResponse({'error': 'POST request required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    user_input = data.get("input", "")
    try:
        sentiment, val = infer_sentiment(user_input)
    except Exception as e:
        logger.error(f"Sentiment inference failed: {e}")
        return JsonResponse({'error': 'Inference error'}, status=500)

    return JsonResponse({'sentiment': sentiment, 'val': val})

@csrf_exempt
def summarizer(request): 
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)
    try:
        data = json.loads(request.body)
        input_text = data.get("input", "")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        summary = summarize(input_text)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"summary": summary})
