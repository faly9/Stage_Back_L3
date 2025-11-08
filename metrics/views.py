from django.shortcuts import render
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

# Compteur de requêtes HTTP
http_requests_total = Counter('http_requests_total', 'Total des requêtes HTTP reçues')

def metrics(request):
    http_requests_total.inc()
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)

