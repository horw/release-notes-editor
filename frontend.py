import os

import pandas as pd
import streamlit as st
import requests

host = os.getenv("BACKEND_URL", "localhost")
base_url = f'http://{host}:8000'
api_endpoint = '/release-notes/'

all_notes = requests.get(f'{base_url}{api_endpoint}').json()
all_notes = [note | {"show_history": False} for note in all_notes]


def update_mr():
    for key, val in st.session_state["MR"]['edited_rows'].items():
        if 'show_history' in val:
            if val['show_history']:
                st.session_state["history"] = all_notes[key]['id']

        all_notes[key].update(val)
        requests.put(
            f'{base_url}{api_endpoint}',
            json=all_notes[key]
        )


df = pd.DataFrame(
    all_notes
)

edited_df = st.data_editor(df, key="MR", on_change=update_mr, hide_index=True)

element = st.container()
if "history" in st.session_state:
    res = requests.get(f'{base_url}/release-notes/{st.session_state["history"]}/history').json()
    element.table(res)
    h_bt = element.button("Hide history")
    if h_bt:
        del st.session_state['history']
