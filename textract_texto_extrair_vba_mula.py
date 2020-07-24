
# TEXT
# EXTRAIR VBA_BIN PARA INCLUSÃO NO ARQUIVO EXCEL CRIADO PELO PANDAS
# EXECUTAR SEM MODIFICAÇÕES, TUDO AUTOMÁTICO, ajustar apenas os diretórios onde estão localizado o arquivo excel .xlsm que tem a macro a ser extraída e o diretório destino do vba_bin
# Resultado Experado se tudo der certo vai ser:
# Extracted: vbaProject.bin




import sys
from zipfile import ZipFile
from zipfile import BadZipfile
import os

GDriveDiretorio_Mula_VBA_File_Full_Path ='/content/drive/My Drive/Colab Notebooks/Excel_Mula_VBA/Mula_VBA_TEXTRACT.xlsm' #exemplo com full path da localização do arquivo mula
GDriveDiretorio_Mula_VBA_File_Bin_Full_Path_Extraido ='/content/drive/My Drive/Colab Notebooks/Excel_Mula_VBA/vba_bin_extraida' #exemplo com full path do diretório de destino do vba_bin extraído

# The VBA project file we want to extract.
vba_filename = 'vbaProject.bin'

xlsm_file = GDriveDiretorio_Mula_VBA_File_Full_Path



try:
    # Open the Excel xlsm file as a zip file.
    xlsm_zip = ZipFile(xlsm_file, 'r')

    # Read the xl/vbaProject.bin file.
    vba_data = xlsm_zip.read('xl/' + vba_filename)

    # Write the vba data to a local file.
    os.chdir(GDriveDiretorio_Mula_VBA_File_Bin_Full_Path_Extraido)
    vba_file = open(vba_filename, "wb")
    vba_file.write(vba_data)
    vba_file.close()

except IOError as e:
    print("File error: %s" % str(e))
    exit()

except KeyError as e:
    # Usually when there isn't a xl/vbaProject.bin member in the file.
    print("File error: %s" % str(e))
    print("File may not be an Excel xlsm macro file: '%s'" % xlsm_file)
    exit()

except BadZipfile as e:
    # Usually if the file is an xls file and not an xlsm file.
    print("File error: %s: '%s'" % (str(e), xlsm_file))
    print("File may not be an Excel xlsm macro file.")
    exit()

except Exception as e:
    # Catch any other exceptions.
    print("File error: %s" % str(e))
    exit()

print("Extracted: %s" % vba_filename)
