import boto3

#
# LISTAR ARQUIVOS SALVOS NO AWS S3
#


#login conta aws amazon
Diretorio_S3='NOME DO SEU DIRETÓRIO AQUI'
aws_access_key_id2='DIGITE AWS_ACCESS KEY AQUI'
aws_secret_access_key2= 'DIGITE AWS_SECRET_ACCESS KEY AQUI'
# region_name2='DIGITE AQUI A REGIÃO DO SEU DIRETÓRIO_S3'
region_name2='us-east-1'

s3_resource = boto3.resource('s3', aws_access_key_id= aws_access_key_id2, aws_secret_access_key= aws_secret_access_key2,region_name=region_name2)
Diretorio = s3_resource.Bucket(Diretorio_S3)

Lista_Arquivos = []
for s3_file in Diretorio.objects.all():
        Lista_Arquivos.append(s3_file.key)
print(Lista_Arquivos)
