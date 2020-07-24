# textratc_with_aws

Textract Text e Tables - From PDF multiple pages...


É um serviço de OCR combinado com inteligência artificial provido pela Amazon Aws
Ele pode extrair texto, tabelas e formulários.
Este projeto envolve extrair textos ou tabelas de um PDF
Para implementar a extração de informações de um PDF o serviço Textract ocorre de forma assíncrona
Por conta disso é preciso fazer o 'pedido' e aguardar ele ser processado pelo Aws
Ao iniciar o trabalho, ele recebe uma Id Única e nos códigos aqui disponíveis existe uma função que a cada 5 segundos checa se a tarefa foi concluída pelo Textract ('Succeed')
A extração de textos de um PDF ocorreu sem problemas quando o arquivo tem muitas páginas.
O mesmo não se pode dizer quando fomos extrair tabelas. Neste caso quando o arquivo de retorno possui mais de um lote ('token') incorria num erro para encontrar key no momento de construír as tabelas cujas informações estavam no primeiro e segundo lote.
Contornamos isso usando uma técnica simples de fazer um loop for na lista 'pages' e somar todos os blocks ['Blocks'] antes de construir as tabelas.
Depois de criada as informações do arquivo .csv, avançamos e alimentamos um arquivo excel.xlsm (já com uma macro para tratamento de dados instalada nele)
Essa macro é extraída de um arquivo excel que chamamos de mula, cuja localizção deve ser informada pelo usuário (full path)
Também disponibilizamos pequenos scripts que servem para listar, deleter e fazer uploado para o S3 da Amazon.
Neste projeto, o arquivo que será submetido ao Textract tem de estar num bucket do serviço S3 da Amazon.
Usamos o Google Colab para rodar a aplicação.

Deixei no próprio código a alimentação das credenciais do serviço da Amazon.
Tal prática não é aconselhável mas para fins didático e desenvolvimento facilitam a construçao do raciocínio



Sugere-se a seguinte ordem:


1   Criar novo Bucket

2   Upload do arquivo com Texto ou Tables a ser extraído para o S3

3   Listar Arquivos no S3 para ter certeza que o arquivo contendo os dados estão lá no caminho a ser informado qdo da extração

4   Extrair vba do arquivo Excel (mula) (textract_texto_extrair_vba_mula.py) (serve para tables ou textos)

5.1 Se for extrair textos  ir para Extrair Texto PDF (textract_texto_extraindo_Texto_PDF.py)

ou

5.2 Se for extrair tabelas ir para Extrair Tables PDF (textract_tables_pdf_multiple_pages_to_excel.py)


