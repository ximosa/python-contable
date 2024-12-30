import streamlit as st
from datetime import date
import database as db

# Funciones auxiliares para la edición y borrado
def editar_movimiento(id, tipo, descripcion, monto, fecha):
    with st.form(key=f"editar_form_{id}"):
        st.subheader(f"Editar movimiento ID: {id}")
        edit_tipo = st.radio("Tipo", options=["Ingreso", "Gasto"], index=0 if tipo == "Ingreso" else 1)
        edit_descripcion = st.text_input("Descripción", value=descripcion)
        edit_monto = st.number_input("Monto (€)", value=int(monto), step=1, format="%d")
        edit_fecha = st.date_input("Fecha", value=date.fromisoformat(fecha))
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Guardar cambios"):
                db.actualizar_movimiento(id, edit_tipo, edit_descripcion, edit_monto, edit_fecha)
                st.success("Movimiento actualizado")
                st.rerun()
        with col2:
             if st.form_submit_button("Borrar"):
                db.borrar_movimiento(id)
                st.success("Movimiento borrado")
                st.rerun()


# Configuración de la página Streamlit
st.set_page_config(page_title="Control de Finanzas", page_icon="💰")
st.title("Control de Finanzas")


# Formulario para añadir un nuevo movimiento
with st.form(key="nuevo_movimiento"):
    st.subheader("Nuevo Movimiento")
    tipo = st.radio("Tipo", options=["Ingreso", "Gasto"])
    descripcion = st.text_input("Descripción")
    monto = st.number_input("Monto (€)", step=1, format="%d")
    fecha = st.date_input("Fecha", value=date.today())
    if st.form_submit_button("Añadir Movimiento"):
        db.insertar_movimiento(tipo, descripcion, monto, fecha.isoformat())
        st.success("Movimiento añadido")
        st.rerun()

# Mostrar los movimientos
st.subheader("Movimientos Registrados")
movimientos = db.obtener_movimientos()
if movimientos:
    for movimiento in movimientos:
        id, tipo, descripcion, monto, fecha = movimiento
        
        st.markdown(f"**ID:** {id} | **Tipo:** {tipo} | **Monto:** {monto} € | **Descripción:** {descripcion} | **Fecha:** {fecha}")
        
        editar_movimiento(id, tipo, descripcion, monto, fecha)

else:
    st.info("No hay movimientos registrados.")
