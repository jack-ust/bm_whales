import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from bokeh.plotting import figure

from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter, StringFormatter, DateFormatter, NumberFormatter



@st.cache
def get_data():
    data_url = 'https://api.flipsidecrypto.com/api/v2/queries/48068a37-cc2c-4843-8291-343186744841/data/latest'
    df = pd.read_json(data_url)
    df['DATE'] = pd.to_datetime(df['DATE']).dt.date.astype(str)
    df['LUNA'] = df['LUNA'].astype(np.int64)
    df['BURN_LAST90D'] = df['BURN_LAST90D'].astype(np.int64)
    df['MINT_LAST90D'] = df['MINT_LAST90D'].astype(np.int64)
    df = df.reindex(['DATE', 'TRADER', 'DIRECTION', 'LUNA', 'BURN_LAST90D','MINT_LAST90D'], axis=1)
    return df

st.set_page_config(layout="wide")

df = get_data()

st.write("### Daily top Luna burners / minters and their long term burn / mint")

select = st.selectbox("Choose date", df['DATE'].unique())

xf = df[df['DATE'] == select]

cds = ColumnDataSource(xf)

def mcol(x, formatter):
    return TableColumn(field=x, title=x, formatter=formatter)

columns = [
        mcol('DATE', StringFormatter()),
TableColumn(field="TRADER", title="TRADER", formatter=HTMLTemplateFormatter(template='<a href="https://finder.extraterrestrial.money/mainnet/account/<%= value %>"target="_blank"><%= value %>')),
mcol('DIRECTION', StringFormatter()),
mcol('LUNA', NumberFormatter()),
mcol('BURN_LAST90D', NumberFormatter()),
mcol('MINT_LAST90D', NumberFormatter())
]


p = DataTable(source=cds, columns=columns, css_classes=["my_table"], autosize_mode='fit_columns',
               sizing_mode='stretch_both')
st.bokeh_chart(p)
