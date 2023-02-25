#!/usr/bin/python3
# -*- coding: utf-8 -*-

# AWS Documentation
# https://aws.amazon.com/pt/blogs/big-data/analyzing-google-analytics-data-with-amazon-appflow-and-amazon-athena/


# In case your data is in a s3 bucket
# s3_source_table_path = f's3://{raw_bucket}/{key_raw_bucket}/{table_name}'
# s3_target_table_path = f's3://{transition_bucket}/{key_transition_bucket}/{table_name}'

# Creating json in the format that AppFlow integrates
json_salvo_appflow = {"reports":[{"columnHeader":{"dimensions":["ga:date","ga:adGroup","ga:campaign"],"metricHeader":{"metricHeaderEntries":[{"name":"ga:sessions","type":"INTEGER"},{"name":"ga:users","type":"INTEGER"}]}},"data":{"rows":[{"dimensions":["20230210","(not set)","(not set)"],"metrics":[{"values":["10","15"]}]},{"dimensions":["20230210","(not set)","campanha_um"],"metrics":[{"values":["1","2"]}]},{"dimensions":["20230210","ads_dois","campanha_dois"],"metrics":[{"values":["55","110"]}]},{"dimensions":["20230210","ads_tres","campanha_tres"],"metrics":[{"values":["112","110"]}]},{"dimensions":["20230211","(not set)","(not set)"],"metrics":[{"values":["3","2"]}]},{"dimensions":["20230211","(not set)","campanha_um"],"metrics":[{"values":["1","1"]}]},{"dimensions":["20230211","ads_dois","campanha_dois"],"metrics":[{"values":["83","80"]}]},{"dimensions":["20230211","ads_tres","campanha_tres"],"metrics":[{"values":["90","90"]}]}],"totals":[{"values":["17","163"]}],"rowCount":8,"minimums":[{"values":["1","1"]}],"maximums":[{"values":["112","110"]}]}}]}

# In case of data in s3
# Reading json file
#record_data = wr.s3.read_json(path=s3_source_table_path)

# Normalizing list
#df = pd.json_normalize(record_data['reports'])

# In case of this example
# Normalizing list
df = pd.json_normalize(json_salvo_appflow['reports'])

df_final = pd.DataFrame() # para dar o append dos dataframes tratados de cada linha do arquivo

# Iterar para pegar os valores dos arquivos diferentes, que ficam em linhas diferentes
for row in df.index:
    print(f'Iterating line {row}')
    df_tratado = pd.DataFrame() #Criando dataframe em branco para ir agregando as colunas

    linha_iterar = df.iloc[[row]] #Seleciona linha que tem os valores para serem tratados
    vazio = pd.isna(linha_iterar['data.rows']).iloc[0] # parametro para pular quando não tiver nada no dia anterior

    if vazio == False:
        
        print('Treating dimensions')
        dimensions = linha_iterar['columnHeader.dimensions']
        tamanho_dimensions = linha_iterar['columnHeader.dimensions'].apply(pd.Series).shape[1]

        # Tratar e criar dataframe dimensões
        for i in range(0,tamanho_dimensions):
            titulo = dimensions[row][i]
            titulo=titulo.replace('ga:','') # limpando titulo para não dar problema no spark sql
            valor_titulo = [r['dimensions'][i] for r in linha_iterar['data.rows'][row]]
            df_tratado[titulo] = valor_titulo # inserindo coluna no dataframe
        
        print('Treating metrics')
        metrics = linha_iterar['columnHeader.metricHeader.metricHeaderEntries']
        tamanho_metrics = linha_iterar['columnHeader.metricHeader.metricHeaderEntries'].apply(pd.Series).shape[1]
        
        # Tratar e criar dataframe metrics
        for i in range(0,tamanho_metrics):
            dict = metrics[row][i]
            titulo = dict['name']
            titulo=titulo.replace('ga:','') # limpando titulo para não dar problema no spark sql
            valor_titulo = [r['metrics'][0]['values'][i] for r in linha_iterar['data.rows'][row]]
            df_tratado[titulo] = valor_titulo # inserindo coluna no dataframe

        df_final = pd.concat([df_tratado,df_final],axis=0) # append ao dataframe tratado da linha anterior
    else:
        pass

print(df_final)
print(df_final.info())

# In case you want to record your data in a s3 bucket
# print(f'writing table on {s3_target_table_path}')
# wr.s3.to_parquet(
#     df=df_final,
#     path=s3_target_table_path,
#     dataset=True,
#     mode='overwrite')
# print(f'tablle written successfully')
