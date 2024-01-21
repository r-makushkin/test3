import streamlit as st
import os
import pandas as pd

def list_files(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return files

def load_data(folder_paths):
    data = []
    for folder_path in folder_paths:
        files = list_files(folder_path)
        for file in files:
            data.append({'uid': file.split('.')[0], 'type': 'retro', 'folder': folder_path.split('/')[-1]})
    df = pd.DataFrame(data)
    unique_uids = df['uid'].unique()
    new_data = {'uid': unique_uids, 'type': 'retro','parsing': [0] * len(unique_uids), 'semantic': [0] * len(unique_uids), 'summarization': 0}

    for uid in unique_uids:
        idx = new_data['uid'].tolist().index(uid)
        parsing_done = (df['folder'] == 'posts') & (df['uid'] == uid)
        parsing_error = (df['folder'] == 'errors') & (df['uid'] == uid)
        new_data['parsing'][idx] = '🟢🟢🟢' if parsing_done.any() else ('🔴🔴🔴' if parsing_error.any() else '🟡🟡🟡')

        semantic_done = (df['folder'] == 'SAcompleted') & (df['uid'] == uid)
        semantic_error = (df['folder'] == 'errors') & (df['uid'] == uid)
        new_data['semantic'][idx] = '🟢🟢🟢' if semantic_done.any() else ('🔴🔴🔴' if semantic_error.any() else '🟡🟡🟡')


    new_df = pd.DataFrame(new_data)
    return pd.DataFrame(new_df)


#def delete_all(folder_paths):
#    for folder in folder_paths:
#        for filename in os.listdir(folder):
#            file_path = os.path.join(folder, filename)
#            os.remove(file_path)


st.title("Status bar")
df = pd.DataFrame()

filter_parsing = st.multiselect("Filter by Parsing", ['🟢🟢🟢', '🔴🔴🔴', '🟡🟡🟡'])
filter_semantic = st.multiselect("Filter by Semantic", ['🟢🟢🟢', '🔴🔴🔴', '🟡🟡🟡'])

folder_paths = ['ldb/tasks', 'ldb/tasks/completed', 'ldb/tasks/errors', 'ldb/posts', 'ldb/SAcompleted']

col1, col2, col3 = st.columns([4, 1, 1])
with col2:
    refresh_button = st.button("refresh", key='refresh_button')
    if refresh_button:
        df = load_data(folder_paths)
with col3:
    delete_button = st.button('delete all', key='delete_all')
#    if delete_all:
#        delete_all(folder_paths)

if filter_parsing:
    df = df[df['parsing'].isin(filter_parsing)]
if filter_semantic:
    df = df[df['semantic'].isin(filter_semantic)]
    
st.table(df)
