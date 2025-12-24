import streamlit as st

from tools.get_b3_stocks_stats import get_b3_stocks_stats
from tools.get_index_current_comp import get_index_current_comp

    
    # index_stocks

    # g = dict()
    # desconsideradas = list()

    # for c in index_stocks['ticker']:
    #     d = estatisticas['TICKER'][estatisticas['TICKER'] == c]
    #     indice = d.index[0]

    #     if vpa > 0 and lpa > 0:
    #         estatisticas['P/L'][indice] = estatisticas['P/L'][indice].replace('.', '')

    #         valorAtual = float(estatisticas['P/L'][indice].replace(',', '.')) * lpa
    #         valorIntrinseco = round((lpa*vpa*22.5)**(1/2), 2)
    #         margemSeguranca = round(1-valorAtual/valorIntrinseco, 2)

    #         g[c] = {'VALOR_INTRINSECO': valorIntrinseco,
    #                 'MARGEM_DE_SEGURANCA': margemSeguranca}.copy()
    #     else:
    #         desconsideradas.append(c)

if __name__ == "__main__":
    
    index = 'IBOV'
    index_stocks = get_index_current_comp(index)
    stocks_stats = get_b3_stocks_stats()
    index_stocks_stats = stocks_stats[stocks_stats['ticker'].isin(index_stocks['ticker'])]

    new_df = index_stocks_stats[['companyname', 'ticker', 'price', 'vpa', 'lpa']]
    print(new_df)
    new_df.concat()
    new_df['iv'], new_df['ms'] = -1.0, -1000.0
    
    mask = (new_df['vpa'] > 0) & (new_df['lpa'] > 0)    
    new_df.loc[mask, 'iv'] = ((new_df['vpa'] * new_df['lpa'] * 22.5) ** (1/2)).round(2)
    new_df.loc[mask, 'ms'] = ((1 - new_df['price'] / new_df['iv']) * 100).round(2)
    
    # st.dataframe(new_df)
    
    # new_df
    # new_df['iv'] = ((new_df['vpa'] * new_df['lpa'] * 22.5) ** (1/2)).round(2)
    
        # try:
        
    # except Exception as e:
    #     print("\n" + str(e))
    #     print('\nFaild to read content from web.')
        
    #     try:
    #         _file_saving_path = f"files/{index.lower()}_current_compositon.csv"
            
    #         df = pd.read_csv(_file_saving_path,
    #             sep=";",
    #             encoding="latin-1",
    #             decimal=",",
    #             thousands=".",
    #             skipfooter=2,
    #             skiprows=2,
    #             header=None,
    #             names=["ticker", "company", "stock_type", "qty", "percentage"],
    #             index_col=False,
    #             engine='python'
    #         )
    #         df["stock_type"] = df["stock_type"].str.replace(" ", "")
            
    #         print('\nUsing stored .csv file...')
            
    #     except FileNotFoundError as e:
    #         print("\n" + str(e))
    #         exit(1)
    
    # try:
    #     index_stocks = get_index_current_comp("IBOV")
    # except Exception as e:
    #     print("\n" + str(e) + "\n")
