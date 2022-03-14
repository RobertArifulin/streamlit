import streamlit as st
from random import random, randint
import datetime
from os.path import exists
from math import sqrt


def run():
    hide_streamlit_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                '''

    st.markdown(
        f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: {1000}px;
        }}
    </style>

    """,
        unsafe_allow_html=True,
    )

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.title('Совместимость пары')
    st.write('Введите даты рождения')

    man = st.date_input("Его дата рождения", datetime.date(1990, 1, 1))
    girl = st.date_input("Её дата рождения", datetime.date(1990, 1, 1))

    button = st.button('Узнать совместимость')


run()
