import streamlit as st
import script_api
import numpy as np
import pandas as pd

OPTIONS = {}
# CRN = ''

def format_func(option):
    return OPTIONS[option]

credentials = script_api.main()
catalogo = script_api.getCatalogo(credentials)
st.dataframe(catalogo)

st.title("Equipo 2")
st.subheader("Transformacion Digital")

code = st.text_input("Código de Socio Formador", type="password")

if code:
    rows = catalogo.loc[catalogo['CODE'] == code]
    OPTIONS = dict(zip(rows["CRN"], rows["Nombre de la experiencia"]))
    # OPTIONS = rows['Nombre de la experiencia']
    # CRN = rows['CRN']
    st.dataframe(rows)
    # st.dataframe(CRN)


crn = st.selectbox("Seleccione el proyecto", options=list(OPTIONS.keys()), format_func=format_func)
print(crn)
st.write(f"You selected option {crn} called {format_func(crn)}")

student_id = st.text_input("Mátricula del alumno")

submit = st.button("Agregar a Proyecto")


if submit:
    st.success("Alumno agregado al proyecto")
    script_api.appendValues(credentials, student_id, crn)
