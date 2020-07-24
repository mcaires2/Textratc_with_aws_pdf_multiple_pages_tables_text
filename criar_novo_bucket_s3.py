#
# CRIAR UM NOVO BUCKET
#


# BUCKETS (DIRETÓRIOS) no serviço S3 tem de ter nome único, não utilizado por qualquer outro usuário.
# este script gera uma combinação de caracteres após um prefixo definido pelo usuário ao fim de atingir o objetivo de criar um nome de bucket único.



import uuid
import boto3

#login conta aws amazon

aws_access_key_id2='DIGITE AWS_ACCESS KEY AQUI'
aws_secret_access_key2= 'DIGITE AWS_SECRET_ACCESS KEY AQUI'
region_name2='us-east-1'

s3_resource = boto3.resource('s3', aws_access_key_id= aws_access_key_id2, aws_secret_access_key= aws_secret_access_key2,region_name=region_name2)


# função para criar um nome de diretório usando meu prefixo pessoal - nome tem de ser unico dentre todos os existentes na amazon, ferrameta util porque mistura meu prefixo com caracteres aleatórios
# mcaires2-teste-07c7dd5a-144b-4b52-882b-ab3a36902820
# mcaires2-pdf-extrair--b9c748aa-242a-4aaf-923b-1ce7fae3ac3d
# não pode usar underlines e outros símbolos, melhor usar dash

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

bucket_name = create_bucket_name('mcaires2-pdf-extrair--')
s3_resource.create_bucket(Bucket=bucket_name)
print(bucket_name)
