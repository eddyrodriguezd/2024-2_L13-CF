import boto3
from boto3.dynamodb.conditions import Key
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Votes')

def handler(event, context):    
    # Escanear toda la tabla para obtener todas las opciones de voto
    response = table.scan()
    items = response.get('Items', [])
    
    # Ordenar las opciones por el campo 'votes' en orden descendente
    sorted_items = sorted(items, key=lambda x: x['votes'], reverse=True)
    
    # Devolver los resultados ordenados
    return {
        'statusCode': 200,
        'body': json.dumps(sorted_items)
    }
