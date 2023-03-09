import streamlit as st
import script_api
import numpy as np

credentials = script_api.main()
catalogo = script_api.getCatalogo(credentials)

st.title("Equipo 2")
st.subheader("Transformacion Digital")

code = st.text_input("Código de Socio Formador", type="password")


project_name = st.selectbox("Seleccione el proyecto", [
                            "Proyecto 1", "Proyecto 2", "Proyecto 3"])

student_id = st.text_input("Mátricula del alumno")

submit = st.button("Agregar a Proyecto")


if submit:
    st.success("Alumno agregado al proyecto")
    script_api.appendValues(credentials, student_id)
