# mapa_lat_long_v3
 Geração de arquivo de municipios, bairros e ruas com latitude e longitude

# Processamento de Indicadores de Leitura

Este repositório contém um script Python para processar e combinar dados de leituras de uma companhia de água e esgoto. O script realiza a leitura de múltiplos arquivos CSV e TXT, faz junções entre os dados, e gera arquivos de saída nos formatos CSV e Parquet.

## Requisitos

- Python 3.6 ou superior
- Pandas
- NumPy
- Glob

## Estrutura de Diretórios

```
project
│   README.md
│   script.py
│
└───data
    ├── MUNICIPIOS_LAT_LONG.csv
    ├── lista_enderecos.del
    └── fases
        ├── file1.txt
        ├── file2.txt
        └── ...
```

## Instalação

1. Clone este repositório.
   ```bash
   git clone https://github.com/ericfp87/mapa_lat_long_v3.git
   cd seu-repositorio
   ```

2. Instale as dependências.
   ```bash
   pip install pandas numpy
   ```

## Uso

1. Coloque os arquivos `MUNICIPIOS_LAT_LONG.csv` e `lista_enderecos.del` na pasta `data`.
2. Coloque os arquivos TXT com os dados das fases na pasta `data/fases`.
3. Execute o script.
   ```bash
   python script.py
   ```

## Explicação do Código

1. **Leitura dos Arquivos CSV**: Lê os arquivos `MUNICIPIOS_LAT_LONG.csv` e `lista_enderecos.del`.
   ```python
   df1 = pd.read_csv(r"C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\MUNICIPIOS_LAT_LONG.csv", delimiter=';')
   df2 = pd.read_csv(r"C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\lista_enderecos.del", delimiter='|', encoding='latin1')
   ```

2. **Conversão de Colunas para Minúsculas**: Converte as colunas relevantes para minúsculas para evitar problemas na junção.
   ```python
   df1['Municipio'] = df1['Municipio'].str.lower()
   df1['Logradouro'] = df1['Logradouro'].str.lower()
   df2['Nome_Localidade'] = df2['Nome_Localidade'].str.lower()
   df2['Nome_logradouro'] = df2['Nome_logradouro'].str.lower()
   ```

3. **Junção dos DataFrames**: Realiza um outer join entre os dois DataFrames.
   ```python
   df = pd.merge(df1, df2, how='outer', left_on=['Municipio', 'Logradouro'], right_on=['Nome_Localidade', 'Nome_logradouro'])
   ```

4. **Filtragem e Seleção de Arquivos TXT**: Filtra os arquivos TXT na pasta `fases` e seleciona os mais recentes para cada palavra-chave.
   ```python
   directory = r"C:\Files\Leitura\Dados\5RM3\Fases"
   keywords = ["unce", "unle", "unmt", "unnt", "unoe", "unsl"]
   files = glob.glob(os.path.join(directory, "*.txt"))
   ```

5. **Leitura e Junção dos Arquivos TXT**: Lê os arquivos TXT, realiza a junção com os dados CSV e combina os resultados.
   ```python
   for file in latest_files:
       df_txt = pd.read_csv(file, delimiter=';', encoding='latin1', usecols=['MATRICULA', 'OCORRENCIA'])
       df_txt_final = pd.concat([df_txt_final, df_txt])
   df_final = pd.merge(df, df_txt_final, how='left', left_on='Mat_calc', right_on='MATRICULA')
   ```

6. **Salvando os Resultados**: Salva os resultados finais em arquivos CSV e Parquet.
   ```python
   df_final.to_csv(r"C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\mapa.csv", index=False)
   df_final.to_parquet(r"C:\Files\INDICADORES DE LEITURAS - COPASA\DATABASE\mapa.parquet")
   ```

## Contribuição

Sinta-se à vontade para abrir issues ou enviar pull requests. Toda contribuição é bem-vinda.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

Se tiver alguma dúvida ou sugestão, entre em contato.

Happy coding!