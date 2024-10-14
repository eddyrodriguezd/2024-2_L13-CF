import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Votes')

def handler(event, context):
    body = json.loads(event['body'])
    option = body['option']

    # Opciones válidas
    valid_options = {'Option1', 'Option2', 'Option3'}

    # Verificar si la opción es válida
    if option not in valid_options:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Opción no válida'})
        }

    # Incrementar el contador de votos
    response = table.update_item(
        Key={'option': option},
        UpdateExpression='SET votes = if_not_exists(votes, :start) + :inc',
        ExpressionAttributeValues={
            ':inc': 1,
            ':start': 0
        },
        ReturnValues='UPDATED_NEW'
    )

    # Retornar respuesta con el nuevo conteo de votos
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Voto registrado',
            'option': option,
            'votes': response['Attributes']['votes']
        })
    }
