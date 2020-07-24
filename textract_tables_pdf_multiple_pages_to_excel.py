#
# EXTRAÇÃO DA TABELA VIA AWS TEXTRACT IA - DESTINO - ARQUIVO EXCEL COM MACRO .xlsm
#
#



# nome do documento que já está no diretorio do aws_S3 mcaires2-teste-07.....
#  ajustar o nome do arquivo mas manter entre aspas...





NomeArquivo = 'TESTE.pdf' # modificar para o nome do arquivo  NO BUCKET AMAZON S3



# a partir daqui não mudar nada, tudo ocorre automático, é só aguardar...exceto credentiais e diretórios vba_bin  
!pip install XlsxWriter
import boto3
import time
import pandas as pd
from time import sleep
import webbrowser, os
from zipfile import ZipFile
from zipfile import BadZipfile
import json
# nome do documento que já está no diretorio do aws_S3 mcaires2-teste-07.....


# a partir daqui não modificar nada, 

# credenciais
GDriveDiretorio_Mula_VBA_File_Bin_Full_Path_Extraido_tables ='/content/drive/My Drive/Colab Notebooks/Excel_Mula_VBA/vba_bin_extraida_tables/vbaProject.bin'
GDriveDiretorio_Mula_VBA_File_Bin_tables='/content/drive/My Drive/Colab Notebooks/Excel_Mula_VBA/vba_bin_extraida_tables'
GDriveDiretorio_Diretorio_Salvar_Arquivo_Excel_Gerado ='/content/drive/My Drive/Excel_Amazon_AWS_Arquivos_Extraidos'

Diretorio_S3='NOME DO SEU DIRETÓRIO AQUI'
aws_access_key_id2='DIGITE AWS_ACCESS KEY AQUI'
aws_secret_access_key2= 'DIGITE AWS_SECRET_ACCESS KEY AQUI'
region_name2='us-east-1'





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
    response = client.start_document_analysis(
    DocumentLocation={
        'S3Object': {
            'Bucket': s3BucketName,
            'Name': objectName
        }
    },FeatureTypes=['TABLES'])                   # start_document_analysis serve para extrair tables and forms, na FeatureTypes vc define Tables para fins deste projeto

    return response["JobId"]

def isJobComplete(jobId):
    global client
    time.sleep(5)
    response = client.get_document_analysis(JobId=jobId)    
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(5)
        response = client.get_document_analysis(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status

pages = []
table_blocks =[]
csv =''
blocks=[]

def getJobResults(jobId):
    
    global client
    global pages
    global table_blocks
    global blocks
    

    time.sleep(5)
    response = client.get_document_analysis(JobId=jobId)
    pages.append(response)
    print("Resultset page recieved: {}".format(len(pages)))
    nextToken = None                                                # quando tem mais de um lote de retorno, a amazon cria uma sub id unica do próximo lote armazenada 'NextToken' do lote atual
    if('NextToken' in response):
        nextToken = response['NextToken']
    while(nextToken):
        time.sleep(5)
        response = client.get_document_analysis(JobId=jobId, NextToken=nextToken)
        
        pages.append(response)                                                                  # vai guardando todos os lotes na lista pages
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if('NextToken' in response):
            nextToken = response['NextToken']

    
    contador=0
    csv = ''
    blocks=[]
    for item in pages:
      blocks= blocks + pages[contador]['Blocks']                                                # esse é o ponto crucial para qdo houver mais de um lote; vc precisa somar todos os ['Blocks'] na lista blocks, do contrário qdo for reconstruir as tabelas vai ter um erro de Key (parte das informações estão podem estar em lotes diferentes)
      contador= contador+1
    print(contador)
    
    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
          table_blocks.append(block)
            

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"
    
    
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index +1)
        csv += '\n\n'

    return csv
    

def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)
    print(rows)
    table_id = 'Table_' + str(table_index)
    
    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():
        
        for col_index, text in cols.items():
            csv += '{}'.format(text) + "&&"  ## Se quiser modificar o delimiter tem de ser aqui, antes era "," - agora é "&&"; fiz isso porque no Brasil nossa separação decimal é vírgula e conflitos apareciam qdo extrair tabelas envolvendo valores monetários...
        csv += '\n'
        
    csv += '\n\n\n'
    return csv

def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)  #4
    #print(rows)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text



# Document
s3BucketName = Diretorio_S3
documentName = NomeArquivo
Nome_Arquivo_csv =Nome_Puro_Arquivo + '_TABLE.csv'
jobId = startJob(s3BucketName, documentName)
print("Started job with id: {}".format(jobId))
if(isJobComplete(jobId)):
    table_csv  = getJobResults(jobId)
    output_file = Nome_Arquivo_csv
    os.chdir(GDriveDiretorio_Diretorio_Salvar_Arquivo_Excel_Gerado)

    # replace content
    with open(output_file, mode="a+",encoding='utf-8') as fout:   # troquei wt write text to a+ - append + in order to preserve former information already saved on the file
        fout.write(table_csv)
        
    

    sleep(3) # deixar para evitar crash

    import xlsxwriter

    df = pd.read_csv(GDriveDiretorio_Diretorio_Salvar_Arquivo_Excel_Gerado+'/'+output_file,delimiter ='&&')
    Nome_Arquivo_xlsx =Nome_Puro_Arquivo+'.xlsx'
    Nome_Arquivo_xlsm =Nome_Puro_Arquivo+'.xlsm'
    
    writer = pd.ExcelWriter(Nome_Arquivo_xlsx, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='DadosExtraidos')
    workbook  = writer.book
    workbook.filename = Nome_Arquivo_xlsm
    workbook.add_vba_project(GDriveDiretorio_Mula_VBA_File_Bin_Full_Path_Extraido_tables)
    writer.save()
    os.chdir(GDriveDiretorio_Mula_VBA_File_Bin_tables)
    print(' (: ')
    print("Dados Extraídos, favor abrir a pasta própria do Google Drive para acessar o arquivo Excel gerado pelo Script")
    
