
#
# EXTRAÇÃO DO TEXTO VIA AWS TEXTRACT IA 
# EXECUTAR ANTES O SCRIPT QUE FAZ A EXTRAÇÃO DO VBA BIN SE FOR USAR EM CONJUNTO COM A CRIAÇÃO DE UM ARQUIVO EXCEL .xlsm
#



# nome do documento que já está no diretorio do aws_S3 mcaires2-teste-07.....
#ajustar o nome do arquivo mas manter entre aspas...





NomeArquivo = 'TESTE.pdf' # DIGITE AQUI O NOME DO SEU ARQUIVO - APENAS O NOME



# a partir daqui não mudar nada, tudo ocorre automático, é só aguardar...
!pip install XlsxWriter
import boto3
import time
import pandas as pd
from time import sleep
import os
from zipfile import ZipFile
from zipfile import BadZipfile
# nome do documento que já está no diretorio do aws_S3 mcaires2-teste-07.....


# a partir daqui não modificar nada, EXCETO OS FULL PATHS e dados de credenciais para login no Amazon Aws

# credenciais
GDriveDiretorio_Mula_VBA_File_Bin_Full_Path_Extraido ='/content/drive/My Drive/Colab Notebooks/Excel_Mula_VBA/vba_bin_extraida/vbaProject.bin' # full path do arquivo vbaProject.bin
GDriveDiretorio_Mula_VBA_File_Bin='/content/drive/My Drive/Colab Notebooks/Excel_Mula_VBA/vba_bin_extraida' # full path do diretório ondes está localizado o arquivo vbaProject.bin
GDriveDiretorio_Diretorio_Salvar_Arquivo_Excel_Gerado ='/content/drive/My Drive/Excel_Amazon_AWS_Arquivos_Extraidos' # full path do diretório onde vai salvar o arquivo Excel com o texto extraído

Diretorio_S3='NOME DO SEU DIRETÓRIO AQUI'
aws_access_key_id2='DIGITE AWS_ACCESS KEY AQUI'
aws_secret_access_key2= 'DIGITE AWS_SECRET_ACCESS KEY AQUI'
region_name2='us-east-1'

# Nome Puro do arquivo é extraído do arquivo pdf e será o nome do aquivo final Excel .xlsm

Nome_Puro_Arquivo = NomeArquivo.replace('.pdf',"")

#fim das credenciais...



# carregando client boto3 com as credenciais e criando funções...

client = boto3.client('textract', 
                          region_name=region_name2, 
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)

def startJob(s3BucketName, objectName):
    
    global client
    response = None
    response = client.start_document_text_detection( # essa linha serve para extrair textos; se quiser extrair tabelas ou formulários terá de usar outro comando aqui
    DocumentLocation={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
        }
    })

    return response["JobId"]

def isJobComplete(jobId):
    global client
    time.sleep(5)
    response = client.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

def getJobResults(jobId):
    global client
    pages = []
    time.sleep(5)
    response = client.get_document_text_detection(JobId=jobId)
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None
    if('NextToken' in response):
        nextToken = response['NextToken']       # 'NextToken' ocorre quando o texto a ser extraído extrapola o lote de informações... Qdo isso ocorre a Amazon distribuí em vários lotes com a Id unica identificada no 'NextToken'

    while(nextToken):
        time.sleep(5)

        response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)

        pages.append(response)   # vou acomulando na lista pages todos os lotes de informações extraídas...
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    return pages

# Document
s3BucketName = Diretorio_S3
documentName = NomeArquivo

jobId = startJob(s3BucketName, documentName)
print("Started job with id: {}".format(jobId))
if(isJobComplete(jobId)):
    response = getJobResults(jobId)

#print(response)

# # Print detected text
# for resultPage in response:
#     for item in resultPage["Blocks"]:
#         if item["BlockType"] == "LINE":
#             print ('\033[94m' +  item["Text"] + '\033[0m')


#Pegando a resposta do trabalho já executado

texto_linhas =[]
texto_linhas_confidence =[]

for resultPage in response:
   for block in resultPage["Blocks"]:
    if block['BlockType'] != 'PAGE':
      if block['BlockType'] == 'LINE':
                texto_linhas.append(block['Text'])
                texto_linhas_confidence.append("{:.2f}".format(block['Confidence']) + "%")
                #texto_linhas_confidence.append(block['Confidence'])
    
print(texto_linhas_confidence, texto_linhas)   

sleep(2)


        # criando um dicionário com listas (array) para exportar via pandas para um arquivo texto.csv

        # Nome_Arquivo_csv =Nome_Puro_Arquivo+'.csv'
        # dicionario = {'Grau Certeza IA':texto_linhas_confidence,'Dados':texto_linhas}
        # df = pd.DataFrame(dicionario)
        # df.to_csv(Nome_Arquivo_csv,encoding="utf-8")
        # print(Nome_Arquivo_csv)

# ou pode gerar arquivo xlsm já com a macro que vc salvou no arquivo excel mula para tratamento do texto extraído

import xlsxwriter

Nome_Arquivo_xlsx =Nome_Puro_Arquivo+'.xlsx'
Nome_Arquivo_xlsm =Nome_Puro_Arquivo+'.xlsm'
dicionario = {'Grau Certeza IA':texto_linhas_confidence,'Dados':texto_linhas}
df = pd.DataFrame(dicionario)
writer = pd.ExcelWriter(Nome_Arquivo_xlsx, engine='xlsxwriter')

df.to_excel(writer, sheet_name='DadosExtraidos')  # se vc preferir, pode mudar o nome da subplanilha do arquivo excel para qq outro, deixei sheet_name='DadosExtraidos'

workbook  = writer.book
workbook.filename = Nome_Arquivo_xlsm
workbook.add_vba_project(GDriveDiretorio_Mula_VBA_File_Bin_Full_Path_Extraido) # localização  full path de onde está o vba_bin
os.chdir(GDriveDiretorio_Diretorio_Salvar_Arquivo_Excel_Gerado)
writer.save()
os.chdir(GDriveDiretorio_Mula_VBA_File_Bin)
print(' (: ')
print("Dados Extraídos, favor abrir a pasta própria do Google Drive para acessar o arquivo Excel gerado pelo Script")
