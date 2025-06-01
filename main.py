import streamlit as st
import sqlitecloud
import polars as pl

from google import genai

from pathlib import Path

st.set_page_config(page_icon='Model Tuning', layout='wide')

st.sidebar.text_input('SQLITE DB', value=None, key='db_key', type='password')
st.sidebar.text_input('Gemini API KEY', value=None, key='llm_key', type='password')

if not st.session_state.db_key and not st.session_state.llm_key:
    st.warning('Please provide the correct keys to proceed')
    st.stop()

if not st.session_state.db_key:
    st.warning('Please provide the db key to proceed')
    st.stop()

if not st.session_state.llm_key:
    st.warning('Please provide the LLM key to proceed')
    st.stop()

if st.session_state.db_key != st.secrets.get('db_key'):
    st.warning('Incorrect db key provided')
    st.stop()

if st.session_state.llm_key != st.secrets.get('llm_key'):
    st.warning('Incorrect llm key provided')
    st.stop()


@st.cache_resource(ttl=3600, show_spinner=False)
def connect_to_db(db_name: str) -> sqlitecloud.Connection:

    conn_string = f"sqlitecloud://ck7kek7bhz.g1.sqlite.cloud:8860?apikey={st.session_state.db_key}"
    conn = sqlitecloud.connect(conn_string)
    conn.execute(f"USE DATABASE {db_name}")

    return conn

def add_record(conn: sqlitecloud.Connection):

    if 'question' in st.session_state and 'answer' in st.session_state:
        question: str = st.session_state.question
        answer: str = st.session_state.answer

        query = 'INSERT INTO fine_tuned_christian (question, answer) VALUES (?, ?)'
        conn.execute(query, parameters=(question, answer,))

def update_record(conn: sqlitecloud.Connection, id: int):

    if 'question' in st.session_state and 'answer' in st.session_state:
        question: str = st.session_state.question
        answer: str = st.session_state.answer

        query = 'UPDATE fine_tuned_christian SET question = ?, answer = ? WHERE id = ?'
        conn.execute(query, parameters=(question, answer, id, ))
        
def remove_record(conn: sqlitecloud.Connection, id: int):

    query = 'DELETE FROM fine_tuned_christian WHERE id = ?'
    conn.execute(query, parameters=(id,))

@st.fragment()
def interact_with_db():

    conn = connect_to_db('llm-stuff')

    cols = st.columns([.7,.3])

    with cols[0]:

        st.html('<p style="text-align: center; font-style: italics;">Select a row to edit it</p>')
        
        df = pl.read_database(query="SELECT * FROM fine_tuned_christian", connection=conn)
        row = st.dataframe(df.select('question', 'answer'), selection_mode='single-row', on_select='rerun')

        EDIT = False
        if row['selection']['rows']:
            row_id = row['selection']['rows'][0]
            EDIT = True
            edit_row = df.row(row_id)

    with cols[1]:

        if EDIT:

            id = edit_row[0]
            q = edit_row[1]
            a = edit_row[2]

            with st.form(key='form1', clear_on_submit=True):

                st.text_input('Question', value=q, key='question')
                st.text_input('Answer', value=a, key='answer')

                cols = st.columns(2)
                with cols[0]:
                    st.form_submit_button(label='Update', on_click=update_record, args=(conn, id), use_container_width=True, type='primary')
                with cols[1]:
                    st.form_submit_button(label='Delete', on_click=remove_record, args=(conn, id), use_container_width=True, type='secondary')


        elif not EDIT:

            with st.form(key='form1', clear_on_submit=True):

                st.text_input('Question', key='question')
                st.text_input('Answer', key='answer')

                st.form_submit_button(label='Submit', on_click=add_record, args=(conn, ), use_container_width=True, type='primary')



@st.cache_resource(ttl=3600, show_spinner=False)
def connect_to_llm() -> genai.Client:
    return genai.Client(api_key=st.session_state.llm_key)

@st.fragment()
def interact_with_llm():

    client = connect_to_llm()

    with st.form('llm-question'):
        question = st.text_input('Ask a question?', value=None)
        st.form_submit_button('Ask', use_container_width=True, type='primary')

    if question:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=question
        )

        st.markdown(response.text)


home, data, chat, overview = st.tabs(['Home', 'Fine Tune Data', 'Chat', 'Overview'])

with home:
    st.markdown(Path.cwd().joinpath('README.md').read_text())


with data:
    interact_with_db()
    

with chat:
    interact_with_llm()