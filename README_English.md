Textract Text and Tables - From PDF multiple pages ...

It is an OCR service combined with artificial intelligence provided by Amazon Aws

It can extract text, tables and forms.

This project involves extracting texts or tables from a PDF

To implement the extraction of information from a PDF, the Textract service occurs asynchronously

Because of this it is necessary to place the 'order' and wait for it to be processed by Aws

When starting the job, he receives a Unique Id and in the codes available there is a function that every 5 seconds checks if the task has been completed by Textract ('Succeed')

Extracting text from a PDF went smoothly when the file has many pages.

The same cannot be said when we went to extract tables. In this case, when the return file has more than one batch ('token'), an error occurred to find a key when building the tables whose information was in the first and second batch.

We get around this using a simple technique of looping forwards in the 'pages' list and adding (+)(not append) all the blocks ['Blocks'] before building the tables.

After creating the information from the .csv file, we move on and feed an excel.xlsm file (already with a data processing macro installed on it)

This macro is extracted from an excel file that we call a mule, whose location must be informed by the user (full path)

We also provide small scripts that serve to list, delete and download for Amazon's S3.

In this project, the file that will be submitted to Textract must be in a bucket of Amazon's S3 service.

We use Google Colab to run the application.

I left in the code itself the supply of Amazon service credentials.

Such practice is not advisable but for didactic and development purposes it facilitates the construction of reasoning

The following order is suggested:

1 Create new Bucket

2 Upload the file with Text or Tables to be extracted to S3

3 List files in S3 to make sure the file containing the data is there on the way to be informed when extracting

4 Extract vba from Excel file (mule) (textract_texto_extrair_vba_mula.py) (serves for tables or texts)

5.1 If you are going to extract texts go to Extract Text PDF (textract_texto_extrANDO_Texto_PDF.py)

or

5.2 If extracting tables go to Extract Tables PDF (textract_tables_pdf_multiple_pages_to_excel.py)
