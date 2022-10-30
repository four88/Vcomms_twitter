from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

API_KEY = 'ce4af7c4b08e4385bf51e159f6a168c7'
ENDPOINT = 'https://climatechangecog.cognitiveservices.azure.com/'

def client():
    client = TextAnalyticsClient(
        endpoint = ENDPOINT,
        credential=AzureKeyCredential(API_KEY)
    )
    return client
