import streamlit as st

from script_api import getCatalog, getRemainingPlaces, getStudentID, appendValues, isEnrolled, main

OPTIONS = {}
remainingPlaces = 0

def format_func(option):
    return OPTIONS[option]

credentials = main()
catalog = getCatalog(credentials)
    
st.title("Equipo 2")
st.subheader("Transformacion Digital")

code = st.text_input("Código de Socio Formador", type="password")

if code:
    rows = catalog.loc[catalog['CODE'] == code]
    if not rows.empty:
        OPTIONS = dict(zip(rows["CRN"], rows["Nombre de la experiencia"]))

        orgName = rows["Socio Formador"].iloc[0]
        st.subheader(f"Bienvenido, {orgName}")

        crn = st.selectbox("Seleccione el proyecto", options=list(OPTIONS.keys()), format_func=format_func)
        remainingPlaces = getRemainingPlaces(credentials, crn)
        st.info(f"Cupo restante: {remainingPlaces}")

        student_id = st.text_input("Mátricula del alumno")

        submit = st.button("Agregar a Proyecto")

        if submit and code and student_id and crn != {}:
            if getStudentID(credentials, student_id):
                if remainingPlaces <= 0:
                    st.warning("No hay cupos para este proyecto.")
                elif isEnrolled(credentials, student_id):
                    st.warning("Estudiante ya esta inscrito en un proyecto.")
                else:
                    st.success("Alumno agregado al proyecto")
                    appendValues(credentials, student_id, crn)
            else:
                st.warning("Matricula invalida.")
    else :
        st.warning("Codigo invalido.")