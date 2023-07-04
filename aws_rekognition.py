import boto3
import os
from dotenv import load_dotenv

# Funcion que retorna etiquetas para imagenes
def detectLabels(image_path, rekognition_client):
    # Abre la imagen
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()
    
    # Llama a la api rekognition
    response = rekognition_client.detect_labels(
        Image={'Bytes': image_bytes}
    )
    
    labels = response['Labels']
    for label in labels:
        print(label['Name'], label['Confidence'])

load_dotenv()

# Retrieve AWS credentials from environment variables
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region_name = os.environ.get('AWS_REGION')

if access_key and secret_key:
    # Create an AWS Rekognition client
    rekognition_client = boto3.client(
        'rekognition',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='us-east-2'
    )

    image_path = './parking.jpeg'
    detectLabels(image_path, rekognition_client)
    print('success')
else:
    print("AWS credentials not found in the .env file.")





