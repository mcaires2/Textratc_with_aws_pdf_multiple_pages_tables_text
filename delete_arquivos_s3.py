#
# DELETAR TODOS OS ARQUIVOS SALVOS NA AMAZON AWS_s3
#

#login conta aws amazon

Diretorio_S3='NOME DO SEU DIRETÓRIO AQUI'
aws_access_key_id2='DIGITE AWS_ACCESS KEY AQUI'
aws_secret_access_key2= 'DIGITE AWS_SECRET_ACCESS KEY AQUI'
region_name2='us-east-1'

s3_resource = boto3.resource('s3', aws_access_key_id= aws_access_key_id2, aws_secret_access_key= aws_secret_access_key2,region_name=region_name2)
Diretorio = s3_resource.Bucket(Diretorio_S3)


for s3_file in Diretorio.objects.all():
        print('deletando arquivo', '-->',s3_file.key)
        s3_resource.Object(Diretorio_S3, s3_file.key).delete()
        print('(: arquivo deletado')
