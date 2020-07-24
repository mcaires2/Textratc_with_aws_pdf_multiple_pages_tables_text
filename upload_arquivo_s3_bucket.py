#
# UPLOAD
#
# Digite entre aspas simples o nome do arquivo que vai ser feito o upload, não esquecer a extensão dele também


Arquivo_Nome ='TabelaTesteAWS.PNG'


import boto3


#login conta aws amazon
Diretorio_S3='NOME DO SEU DIRETÓRIO AQUI'
aws_access_key_id2='DIGITE AWS_ACCESS KEY AQUI'
aws_secret_access_key2= 'DIGITE AWS_SECRET_ACCESS KEY AQUI'
region_name2='us-east-1'

s3_resource = boto3.resource('s3', aws_access_key_id= aws_access_key_id2, aws_secret_access_key= aws_secret_access_key2,region_name=region_name2)
Diretorio = s3_resource.Bucket(Diretorio_S3)

# setup do diretório do caminho do arquivo que vai ser feito upload, full path
GDriveDiretorio ='DIGITE AQUI O FULL PATH DO ARQUIVO DE ORIGEM'

s3_resource.Object(Diretorio_S3, Arquivo_Nome).upload_file(
    Filename=(GDriveDiretorio + Arquivo_Nome))

# lista dos arquivos que estão salvo na Amazon após o upload...
Lista_Arquivos = []
for s3_file in Diretorio.objects.all():
        Lista_Arquivos.append(s3_file.key)
print(Lista_Arquivos)
