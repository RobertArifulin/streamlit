import streamlit as st
import random
import datetime


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

    man = st.date_input("Его дата рождения", datetime.date(2000, 1, 1))
    girl = st.date_input("Её дата рождения", datetime.date(2000, 1, 1))

    if st.button('Узнать совместимость'):
        if str(man) == "2007-03-21" and str(girl) == "2005-04-26":
            st.text(f"Ваша совместимость {100}%")
        else:
            seed = int((str(man) + str(girl)).replace("-", ""))
            random.seed(seed)
            n = random.randint(0, 100)
            st.text(f"Ваша совместимость {n}%")

run()
