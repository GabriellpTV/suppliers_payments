from datetime import datetime
from tkinter.filedialog import askopenfilename
import streamlit as st
import pandas as pd
from xmltoxlsx import *

st.set_page_config(layout="wide")

xml_path = askopenfilename()
xmltoxlsx(xml_path)

base = pd.read_excel("resultado_tabela.xlsx")

base["Data de criação"] = pd.to_datetime(base["Data de criação"], errors='coerce')
base["Data de criação"] = base["Data de criação"].dt.strftime("%d/%m/%Y")

base["Data"] = pd.to_datetime(base["Data"], errors='coerce')
base["Data"] = base["Data"].dt.strftime("%d/%m/%Y")

base["Data do DOC. Fiscal"] = pd.to_datetime(base["Data do DOC. Fiscal"], errors='coerce')
base["Data do DOC. Fiscal"] = base["Data do DOC. Fiscal"].dt.strftime("%d/%m/%Y")

base["Data de vencimento/Receber até"] = pd.to_datetime(base["Data de vencimento/Receber até"], errors='coerce')
base["Data de vencimento/Receber até"] = base["Data de vencimento/Receber até"].dt.strftime("%d/%m/%Y")

base['Valor'] = base['Valor Liquido'].fillna(0) + base['Valor Imposto'].fillna(0)

def centralizar_celulas(df):
    return df.style.set_properties(**{'text-align': 'center'})


def filtrar(x):
    base_unica = base[base["Nome"] == x]
    return (base_unica)

def filtrar_status(parametro, ano=None, mes=None, first=None):
    if first == 0:
        data = datetime.now()
        ano = data.year  
        mes = data.month
        first = False

    if parametro == "Geral":
        base_filtrada = base
        if ano:
            base_filtrada = base_filtrada[pd.to_datetime(base_filtrada['Data'], format="%d/%m/%Y", dayfirst=True).dt.year == ano]
        
        if mes:
            base_filtrada = base_filtrada[pd.to_datetime(base_filtrada['Data'], format="%d/%m/%Y", dayfirst=True).dt.month == mes]

        if base_filtrada.empty:
            base_filtrada = "Sem Resultados"

    else:
        base_filtrada = base_fornecedor[base_fornecedor['Status'] == parametro]

        if ano:
            base_filtrada = base_filtrada[pd.to_datetime(base_filtrada['Data'], format="%d/%m/%Y", dayfirst=True).dt.year == ano]
        
        if mes:
            base_filtrada = base_filtrada[pd.to_datetime(base_filtrada['Data'], format="%d/%m/%Y", dayfirst=True).dt.month == mes]

        if base_filtrada.empty:
            base_filtrada = "Sem Resultados"

    return base_filtrada

st.title("Suplyers Payment")
tab1, tab2 = st.tabs(["Visão Geral", "Visão Cliente"])

with tab1:
    st.header("Visão Geral")
    anos = [''] + sorted(pd.to_datetime(base['Data'], format="%d/%m/%Y", dayfirst=True).dt.year.dropna().astype(int).unique())
    meses = [''] + sorted(pd.to_datetime(base['Data'], format="%d/%m/%Y", dayfirst=True).dt.month.dropna().astype(int).unique())

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        mes_selecionado = st.selectbox('Selecione o Mês', meses, key='mes_geral')
    with col2:
        ano_selecionado = st.selectbox('Selecione o Ano', anos, key='ano_geral')
    
    first = 0
    st.markdown("<hr>", unsafe_allow_html=True)
    base_filtrada = filtrar_status("Geral", ano_selecionado, mes_selecionado, first)

    st.header("Maior Pago Valor no Mês")
    base_filtrada_pagos_mes = base_filtrada[base_filtrada['Status'] == "Pago integralmente"]
    
    max = base_filtrada_pagos_mes['Valor'].max()
    base_filtrada_pagos_mes_max = base_filtrada_pagos_mes[base_filtrada_pagos_mes['Valor'] == max]
    
    col1, col2, col3 = st.columns(3)

    with col1: 
        st.dataframe(base_filtrada_pagos_mes_max['Número da transação'], hide_index= True, use_container_width= True)
        st.dataframe(base_filtrada_pagos_mes_max['Valor'], hide_index= True, use_container_width= True)

    with col2:
        st.dataframe(base_filtrada_pagos_mes_max['Nome'], hide_index= True, use_container_width= True)
        st.dataframe(base_filtrada_pagos_mes_max['Valor Liquido'], hide_index= True, use_container_width= True)

    with col3:
        st.dataframe(base_filtrada_pagos_mes_max['Data de vencimento/Receber até'], hide_index= True, use_container_width= True)
        st.dataframe(base_filtrada_pagos_mes_max['Valor Imposto'], hide_index= True, use_container_width= True)

    st.markdown("<hr>", unsafe_allow_html=True)
    base_filtrada = filtrar_status("Geral", ano_selecionado)
    st.header("Maior Pago Valor no Ano")
    base_filtrada_pagos_ano = base_filtrada[base_filtrada['Status'] == "Pago integralmente"]
    
    max = base_filtrada_pagos_ano['Valor'].max()
    base_filtrada_pagos_ano_max = base_filtrada_pagos_ano[base_filtrada_pagos_ano['Valor'] == max]
    
    col1, col2, col3 = st.columns(3)

    with col1: 
        st.dataframe(base_filtrada_pagos_ano_max['Número da transação'], hide_index= True, use_container_width= True)
        st.dataframe(base_filtrada_pagos_ano_max['Valor'], hide_index= True, use_container_width= True)

    with col2:
        st.dataframe(base_filtrada_pagos_ano_max['Nome'], hide_index= True, use_container_width= True)
        st.dataframe(base_filtrada_pagos_ano_max['Valor Liquido'], hide_index= True, use_container_width= True)

    with col3:
        st.dataframe(base_filtrada_pagos_ano_max['Data de vencimento/Receber até'], hide_index= True, use_container_width= True)
        st.dataframe(base_filtrada_pagos_ano_max['Valor Imposto'], hide_index= True, use_container_width= True) 
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h1>Maiores Valores</h1>", unsafe_allow_html=True)
    st.header("Dez Maiores do Mês")

    col4, col5 = st.columns(2)
    with col4:
        top_dez_mes = base_filtrada_pagos_mes.nlargest(10, 'Valor')
        col6, col7 = st.columns(2)

        with col6:
            st.dataframe(top_dez_mes['Nome'], hide_index= True, use_container_width= True)
        
        with col7:
            st.dataframe(top_dez_mes['Valor'], hide_index= True, use_container_width= True) 

    with col5:
        col6, col7 = st.columns(2)

        with col6:
            st.dataframe(top_dez_mes['Número do documento'], hide_index= True, use_container_width= True)
        
        with col7:
            st.dataframe(top_dez_mes['Número da transação'], hide_index= True, use_container_width= True) 
        

    st.header("Dez Maiores do Ano")

    col4, col5 = st.columns(2)
    with col4:
        top_dez_ano = base_filtrada_pagos_ano.nlargest(10, 'Valor')
        col6, col7 = st.columns(2)

        with col6:
            st.dataframe(top_dez_ano['Nome'], hide_index= True, use_container_width= True)
        
        with col7:
            st.dataframe(top_dez_ano['Valor'], hide_index= True, use_container_width= True) 

    with col5:
        col6, col7 = st.columns(2)

        with col6:
            st.dataframe(top_dez_ano['Número do documento'], hide_index= True, use_container_width= True)
        
        with col7:
            st.dataframe(top_dez_ano['Número da transação'], hide_index= True, use_container_width= True) 


with tab2:
    col1, col2, col3 = st.columns(3)
    with col2:
        opcoes = [''] + list(base['Nome'].unique())
        busca = st.selectbox("Digite o Nome do Fornecedor", opcoes, index=0, key=None)

    base_fornecedor = filtrar(busca)

    tab1, tab2 = st.tabs(["Pagamentos Realizados", "Pagamentos Pendentes"])
    if (busca == ""):
        with tab1:
            st.header("Pagamentos Realizados")
            st.write("Busque por um fornecedor.")

        with tab2:
            st.header("Pagamentos Pendentes")
            st.write("Busque por um fornecedor.")
    else:
        with tab1:
                st.header("Pagamentos Realizados")
                base_filtrada = filtrar_status("Pago integralmente")
                try:
                    if base_filtrada == "Sem Resultados":
                        st.write("Não foi realizado nenhum pagamento")
                        pass
                except:
                    st.header("Filtros")

                    anos = [''] + sorted(pd.to_datetime(base_filtrada['Data'], format="%d/%m/%Y", dayfirst=True).dt.year.dropna().astype(int).unique())
                    meses = [''] + sorted(pd.to_datetime(base_filtrada['Data'], format="%d/%m/%Y", dayfirst=True).dt.month.dropna().astype(int).unique())

                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    with col1:
                        mes_selecionado = st.selectbox('Selecione o Mês', meses, key='mes_pago')
                    with col2:
                        ano_selecionado = st.selectbox('Selecione o Ano', anos, key='ano_pago')

                tab3, tab4 = st.tabs(["Notas", "Detalhes"])
                with tab3:
                    base_filtrada = filtrar_status("Pago integralmente", ano_selecionado, mes_selecionado)
                    
                    try:
                        if base_filtrada == "Sem Resultados":
                            st.write("Ainda não realizamos nenhum pagamento no periodo.")
                    except:
                        st.dataframe(base_filtrada, hide_index= True, use_container_width= True, column_order=["Data", "Número do documento", "Valor", "Data de vencimento/Receber até"])

                        with st.expander("Detalhe das Notas"):
                            notas = [''] + list(base_filtrada["Número do documento"].unique())
                            opcao = st.selectbox('Escolha uma Nota:',(notas))

                            nota = base_filtrada[base_filtrada["Número do documento"] == opcao]

                            if (nota.empty):
                                st.write("Selecione uma Nota Para Analizar.")
                            else:
                                st.write("Informações da Fatura:")

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.dataframe(nota["Número da transação"], hide_index= True, use_container_width= True)
                                with col1:
                                    st.dataframe(nota["Conta"], hide_index= True, use_container_width= True)
                                with col2:
                                    st.dataframe(nota["Data de criação"], hide_index= True, use_container_width= True)
                                with col3:
                                    st.dataframe(nota["Status"], hide_index= True, use_container_width= True)

                                st.write("Datas:")

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.dataframe(nota["Data do DOC. Fiscal"], hide_index= True, use_container_width= True)
                                
                                with col2:
                                    st.dataframe(nota["Data"], hide_index= True, use_container_width= True)

                                with col3:
                                    st.dataframe(nota["Data de vencimento/Receber até"], hide_index= True, use_container_width= True)

                                st.write("Valores:")

                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.dataframe(nota["Valor"], hide_index= True, use_container_width= True)
                                
                                with col2:
                                    st.dataframe(nota["Valor Liquido"], hide_index= True, use_container_width= True)

                                with col3:
                                    st.dataframe(nota["Valor Imposto"], hide_index= True, use_container_width= True)

                                st.write("Descrição:")

                                st.dataframe(nota["Memorando"], hide_index= True, use_container_width= True)
                with tab4:
                    st.header("Valores")
                    col1, col2 = st.columns(2)

                    geral_fornecedor = filtrar_status("Pago integralmente")
                    with col1:
                        geral_fornecedor["Valor Total Pago"] = sum(geral_fornecedor["Valor"])
                        
                        st.dataframe(geral_fornecedor["Valor Total Pago"].head(1), hide_index= True, use_container_width= True)
                        st.markdown("<hr>", unsafe_allow_html=True)
                    with col2:
                        geral_fornecedor["Valor Total Impostos"] = geral_fornecedor["Valor Imposto"].sum()
                        st.dataframe(geral_fornecedor["Valor Total Impostos"].head(1), hide_index= True, use_container_width= True)
                        st.markdown("<hr>", unsafe_allow_html=True)

                    
                    with col1:
                        maior_valor = pd.DataFrame({"Maior Valor (Nota)": [geral_fornecedor["Valor"].max()]})
                        st.dataframe(maior_valor, hide_index=True, use_container_width= True)

                    with col2:
                        indice_maior_valor = geral_fornecedor["Valor"].idxmax()
                        maior_valor = pd.DataFrame({"Número do documento": [geral_fornecedor.loc[indice_maior_valor, "Número do documento"]],})
                        st.dataframe(maior_valor, hide_index=True, use_container_width= True)

                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.header("Pagamentos")

                    geral_fornecedor = base_filtrada
                    geral_fornecedor["Mês"] = pd.to_datetime(geral_fornecedor["Data"], format="%d/%m/%Y", dayfirst=True).dt.month
                    geral_fornecedor["Ano"] = pd.to_datetime(geral_fornecedor["Data"], format="%d/%m/%Y", dayfirst=True).dt.year

                    soma_mensal = geral_fornecedor.groupby("Mês")["Valor"].sum().reset_index()
                    soma_mensal.columns = ["Mês", "Total Mês"]

                    geral_fornecedor = geral_fornecedor.merge(soma_mensal, on="Mês", how="left")

                    soma_anual = geral_fornecedor.groupby("Ano")["Valor"].sum().reset_index()
                    soma_anual.columns = ["Ano", "Total Ano"]

                    geral_fornecedor = geral_fornecedor.merge(soma_anual, on="Ano", how="left")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Pagamentos Totais (mês)")
                        geral_fornecedor = geral_fornecedor.sort_values(by="Mês", ascending=False)
                        for mes in geral_fornecedor["Mês"].unique():
                            
                            base_mes = geral_fornecedor[geral_fornecedor["Mês"] == mes]
                            numero = base_mes["Mês"].head(1)
                            valor = base_mes["Total Mês"].head(1)
                            impostos = pd.DataFrame({"Total Impostos": [base_mes["Valor Imposto"].sum()]})

                            col4, col5, col6 = st.columns(3)

                            with col4:
                                st.dataframe(numero, hide_index=True, use_container_width= True)

                            with col5:
                                st.dataframe(valor, hide_index=True, use_container_width= True)

                            with col6:
                                st.dataframe(impostos, hide_index=True, use_container_width= True)

                    
                    with col2:
                        st.write("Pagamentos Totais (ano)")
                        geral_fornecedor = geral_fornecedor.sort_values(by="Ano", ascending=False)
                        for ano in geral_fornecedor["Ano"].unique():
                            base_ano = geral_fornecedor[geral_fornecedor["Ano"] == ano]
                            numero = base_ano["Ano"].head(1).apply(lambda x: str(x).replace(",", ""))
                            valor = base_ano["Total Ano"].head(1)
                            impostos = pd.DataFrame({"Total Impostos": [base_ano["Valor Imposto"].sum()]})
                            
                            col4, col5, col6 = st.columns(3)

                            with col4:
                                st.dataframe(numero, hide_index=True, use_container_width= True)

                            with col5:
                                st.dataframe(valor, hide_index=True, use_container_width= True)

                            with col6:
                                st.dataframe(impostos, hide_index=True, use_container_width= True)


        with tab2:
            st.header("Pagamentos Pendentes")
            base_filtrada = filtrar_status("Aprovação do supervisor pendente")
            try:
                if base_filtrada == "Sem Resultados":
                    st.write("Nenhum pagamento pendente encontrado")
                    pass
            except:
                st.header("Filtros")
                anos = [''] + sorted(pd.to_datetime(base_filtrada['Data'], format="%d/%m/%Y", dayfirst=True).dt.year.dropna().astype(int).unique())
                meses = [''] + sorted(pd.to_datetime(base_filtrada['Data'], format="%d/%m/%Y", dayfirst=True).dt.month.dropna().astype(int).unique())
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    mes_selecionado = st.selectbox('Selecione o Mês', meses, key='mes_pendente')
                with col2:
                    ano_selecionado = st.selectbox('Selecione o Ano', anos, key='ano_pendente')
                tab3, tab4 = st.tabs(["Notas", "Detalhes"])
                with tab3:
                    base_filtrada = filtrar_status("Aprovação do supervisor pendente", ano_selecionado, mes_selecionado)
                    
                    try:
                        if base_filtrada == "Sem Resultados":
                            st.write("Ainda não realizamos nenhum pagamento no periodo.")
                    except:
                        st.dataframe(base_filtrada, hide_index= True, use_container_width= True, column_order=["Data", "Número do documento", "Valor", "Data de vencimento/Receber até"])
                        with st.expander("Detalhe das Notas"):
                            notas = [''] + list(base_filtrada["Número do documento"].unique())
                            opcao = st.selectbox('Escolha uma Nota:',(notas), key='select_pendente')
                            nota = base_filtrada[base_filtrada["Número do documento"] == opcao]
                            if (nota.empty):
                                st.write("Selecione uma Nota Para Analizar.")
                            else:
                                st.write("Informações da Fatura:")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.dataframe(nota["Número da transação"], hide_index= True, use_container_width= True)
                                with col1:
                                    st.dataframe(nota["Conta"], hide_index= True, use_container_width= True)
                                with col2:
                                    st.dataframe(nota["Data de criação"], hide_index= True, use_container_width= True)
                                with col3:
                                    st.dataframe(nota["Status"], hide_index= True, use_container_width= True)
                                st.write("Datas:")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.dataframe(nota["Data do DOC. Fiscal"], hide_index= True, use_container_width= True)
                                
                                with col2:
                                    st.dataframe(nota["Data"], hide_index= True, use_container_width= True)
                                with col3:
                                    st.dataframe(nota["Data de vencimento/Receber até"], hide_index= True, use_container_width= True)
                                st.write("Valores:")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.dataframe(nota["Valor"], hide_index= True, use_container_width= True)
                                
                                with col2:
                                    st.dataframe(nota["Valor Liquido"], hide_index= True, use_container_width= True)
                                with col3:
                                    st.dataframe(nota["Valor Imposto"], hide_index= True, use_container_width= True)
                                st.write("Descrição:")
                                st.dataframe(nota["Memorando"], hide_index= True, use_container_width= True)
                with tab4:

                    try:
                        if base_filtrada == "Sem Resultados":
                            pass
                    except:
                        st.header("Valores")
                        col1, col2 = st.columns(2)
                        geral_fornecedor = filtrar_status("Aprovação do supervisor pendente")
                        with col1:
                            geral_fornecedor["Valor Total Pago"] = sum(geral_fornecedor["Valor"])
                            
                            st.dataframe(geral_fornecedor["Valor Total Pago"].head(1), hide_index= True, use_container_width= True)
                            st.markdown("<hr>", unsafe_allow_html=True)
                        with col2:
                            geral_fornecedor["Valor Total Impostos"] = geral_fornecedor["Valor Imposto"].sum()
                            st.dataframe(geral_fornecedor["Valor Total Impostos"].head(1), hide_index= True, use_container_width= True)
                            st.markdown("<hr>", unsafe_allow_html=True)
                        
                        with col1:
                            maior_valor = pd.DataFrame({"Maior Valor (Nota)": [geral_fornecedor["Valor"].max()]})
                            st.dataframe(maior_valor, hide_index=True, use_container_width= True)
                        with col2:
                            indice_maior_valor = geral_fornecedor["Valor"].idxmax()
                            maior_valor = pd.DataFrame({"Número do documento": [geral_fornecedor.loc[indice_maior_valor, "Número do documento"]],})
                            st.dataframe(maior_valor, hide_index=True, use_container_width= True)
                        st.markdown("<hr>", unsafe_allow_html=True)
                        st.header("Pagamentos")
                        geral_fornecedor = base_filtrada
                        geral_fornecedor["Mês"] = pd.to_datetime(geral_fornecedor["Data de vencimento/Receber até"], format="%d/%m/%Y", dayfirst=True).dt.month
                        geral_fornecedor["Ano"] = pd.to_datetime(geral_fornecedor["Data de vencimento/Receber até"], format="%d/%m/%Y", dayfirst=True).dt.year

                        soma_mensal = geral_fornecedor.groupby("Mês")["Valor"].sum().reset_index()
                        soma_mensal.columns = ["Mês", "Total Mês"]
                        geral_fornecedor = geral_fornecedor.merge(soma_mensal, on="Mês", how="left")
                        soma_anual = geral_fornecedor.groupby("Ano")["Valor"].sum().reset_index()
                        soma_anual.columns = ["Ano", "Total Ano"]
                        geral_fornecedor = geral_fornecedor.merge(soma_anual, on="Ano", how="left")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("Pendências Totais (mês)")
                            geral_fornecedor = geral_fornecedor.sort_values(by="Mês", ascending=False)
                            for mes in geral_fornecedor["Mês"].unique():
                                
                                base_mes = geral_fornecedor[geral_fornecedor["Mês"] == mes]
                                numero = base_mes["Mês"].head(1)
                                valor = base_mes["Total Mês"].head(1)
                                impostos = pd.DataFrame({"Total Impostos": [base_mes["Valor Imposto"].sum()]})
                                col4, col5, col6 = st.columns(3)
                                with col4:
                                    st.dataframe(numero, hide_index=True, use_container_width= True)
                                    st.markdown("<hr>", unsafe_allow_html=True)
                                with col5:
                                    st.dataframe(valor, hide_index=True, use_container_width= True)
                                    st.markdown("<hr>", unsafe_allow_html=True)
                                with col6:
                                    st.dataframe(impostos, hide_index=True, use_container_width= True)
                                    st.markdown("<hr>", unsafe_allow_html=True)
                        
                        with col2:
                            st.write("Pendências Totais (ano)")
                            geral_fornecedor = geral_fornecedor.sort_values(by="Ano", ascending=False)
                            for ano in geral_fornecedor["Ano"].unique():
                                base_ano = geral_fornecedor[geral_fornecedor["Ano"] == ano]
                                numero = base_ano["Ano"].head(1).apply(lambda x: str(x).replace(",", ""))
                                valor = base_ano["Total Ano"].head(1)
                                impostos = pd.DataFrame({"Total Impostos": [base_ano["Valor Imposto"].sum()]})
                                
                                col4, col5, col6 = st.columns(3)
                                with col4:
                                    st.dataframe(numero, hide_index=True, use_container_width= True)
                                    st.markdown("<hr>", unsafe_allow_html=True)
                                with col5:
                                    st.dataframe(valor, hide_index=True, use_container_width= True)
                                    st.markdown("<hr>", unsafe_allow_html=True)
                                with col6:
                                    st.dataframe(impostos, hide_index=True, use_container_width= True)
                                    st.markdown("<hr>", unsafe_allow_html=True)
                    