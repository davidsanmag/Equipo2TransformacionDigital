import streamlit as st
import script_api
import numpy as np
import pandas as pd

OPTIONS = {}
cupoRestante = 0

def format_func(option):
    return OPTIONS[option]

credentials = script_api.main()
catalogo = script_api.getCatalogo(credentials)
    
st.title("Equipo 2")
st.subheader("Transformacion Digital")

code = st.text_input("Código de Socio Formador", type="password")

if code:
    rows = catalogo.loc[catalogo['CODE'] == code]
    if not rows.empty:
        OPTIONS = dict(zip(rows["CRN"], rows["Nombre de la experiencia"]))

        orgName = rows["Socio Formador"].iloc[0]
        st.subheader(f"Bienvenido, {orgName}")

        crn = st.selectbox("Seleccione el proyecto", options=list(OPTIONS.keys()), format_func=format_func)
        cupoRestante = script_api.getRemainingPlaces(credentials, crn)
        st.info(f"Cupo restante: {cupoRestante}")

        student_id = st.text_input("Mátricula del alumno")

        submit = st.button("Agregar a Proyecto")

        if submit and code and student_id and crn != {}:
            if script_api.getStudentID(credentials, student_id):
                if cupoRestante <= 0:
                    st.warning("No hay cupos para este proyecto.")
                elif script_api.isEnrolled(credentials, student_id):
                    st.warning("Estudiante ya esta inscrito en un proyecto.")
                else:
                    st.success("Alumno agregado al proyecto")
                    script_api.appendValues(credentials, student_id, crn)
            else:
                st.warning("Matricula invalida.")
    else :
        st.warning("Codigo invalido.")