import streamlit as st


st.title("Equipo 2")
st.subheader("Transformacion Digital")

code = st.text_input("Código de Socio Formador", type="password")

project_name = st.selectbox("Seleccione el proyecto", [
                            "Proyecto 1", "Proyecto 2", "Proyecto 3"])

student_id = st.text_input("Mátricula del alumno")

submit = st.button("Agregar a Proyecto")

if submit:
    st.success("Alumno agregado al proyecto")
