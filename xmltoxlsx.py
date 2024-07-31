import pandas as pd
from tkinter import *
from tkinter.filedialog import askopenfilename
import xmltodict
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import numbers
import os


def xmltoxlsx(xml_path):
   with open(xml_path, "rb") as f1:
       data_dict = xmltodict.parse(f1)
   data_list = data_dict['Workbook']['Worksheet']['Table']['Row']
   rows = []
   column_names = [cell['Data']['#text'] for cell in data_list[0]['Cell']]
   for row_data in data_list[1:]:
       row = {}
       for i, cell in enumerate(row_data['Cell']):
           if i < len(column_names):
               value = cell.get('Data', {}).get('#text', '')
               row[column_names[i]] = value
       rows.append(row)
   for item in rows:
        if item['Data de criação'] != '' and item['Data de criação'] > '3000-00-00T00:00:00':
           item['Data de criação'] = '2' + item['Data de criação'][1:].split('T')[0]
        else:
           item['Data de criação'] = item['Data de criação'].split('T')[0]

        if item['Data'] != '' and item['Data'] > '3000-00-00T00:00:00':
            item['Data'] = '2' + item['Data'][1:].split('T')[0]
        else:
            item['Data'] = item['Data'].split('T')[0]

        if item['Data de vencimento/Receber até'] != '' and item['Data de vencimento/Receber até'] > '3000-00-00T00:00:00':
            item['Data de vencimento/Receber até'] = '2' + item['Data de vencimento/Receber até'][1:].split('T')[0]
        else:
            item['Data de vencimento/Receber até'] = item['Data de vencimento/Receber até'].split('T')[0]

   df = pd.DataFrame(rows)
   df.to_excel('resultado_tabela.xlsx', index=False)


