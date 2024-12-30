import streamlit as st
from datetime import date
import database as db

# Función para calcular el balance total
def calcular_balance(movimientos):
    balance = 0
    for movimiento in movimientos:
        tipo, monto = movimiento[1], movimiento[3]
        if tipo == "Ingreso":
            balance += monto
        elif tipo == "Gasto":
            balance -= monto
    return balance


# Función para la edición
def editar_movimiento(id, tipo, descripcion, monto, fecha):
    if st.session_state.get(f"editar_{id}", False): # Verificamos si estamos editando
        with st.form(key=f"editar_form_{id}"):
            col1, col2 = st.columns(2)
            with col1:
              edit_tipo = st.radio("Tipo", options=["Ingreso", "Gasto"], index=0 if tipo == "Ingreso" else 1, horizontal=True)
              edit_monto = st.number_input("Monto (€)", value=int(monto), step=1, format="%d")
            with col2:
              edit_descripcion = st.text_input("Descripción", value=descripcion)
              edit_fecha = st.date_input("Fecha", value=date.fromisoformat(fecha))
            col3, col4=st.columns(2)
            with col3:
               if st.form_submit_button("Guardar cambios"):
                  db.actualizar_movimiento(id, edit_tipo, edit_descripcion, edit_monto, edit_fecha)
                  st.session_state[f"editar_{id}"] = False # Desactivamos el modo de edición
                  st.rerun()
            with col4:
                if st.form_submit_button("Cancelar"):
                     st.session_state[f"editar_{id}"] = False
                     st.rerun()

# Función para el borrado
def borrar_movimiento(id):
    if st.button(f"Borrar", key=f"borrar_btn_{id}"):
        db.borrar_movimiento(id)
        st.success("Movimiento borrado")
        st.rerun()

# Configuración de la página Streamlit
st.set_page_config(page_title="Control de Finanzas", page_icon="💰")
st.title("Control de Finanzas")

# Formulario para añadir un nuevo movimiento
with st.form(key="nuevo_movimiento"):
    st.subheader("Nuevo Movimiento")
    col1, col2 = st.columns(2)
    with col1:
         tipo = st.radio("Tipo", options=["Ingreso", "Gasto"], horizontal=True)
         monto = st.number_input("Monto (€)", step=1, format="%d")
    with col2:
        descripcion = st.text_input("Descripción")
        fecha = st.date_input("Fecha", value=date.today())
    if st.form_submit_button("Añadir Movimiento"):
        db.insertar_movimiento(tipo, descripcion, monto, fecha.isoformat())
        st.success("Movimiento añadido")
        st.rerun()


# Mostrar los movimientos y el balance
st.subheader("Movimientos Registrados")
movimientos = db.obtener_movimientos()

if movimientos:
    balance = calcular_balance(movimientos)
    st.markdown(f"**Balance Total:** {balance} €")

    for movimiento in movimientos:
        id, tipo, descripcion, monto, fecha = movimiento

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.write(f"ID: {id}")
        with col2:
            st.write(f"Tipo: {tipo}")
        with col3:
            st.write(f"Monto: {monto} €")
        with col4:
            st.write(f"Descripción: {descripcion}")
        with col5:
            st.write(f"Fecha: {fecha}")
            
        col6, col7 = st.columns(2)
        with col6:
             if st.button("Editar", key=f"edit_btn_{id}"):
                st.session_state[f"editar_{id}"] = True
        with col7:
            borrar_movimiento(id)
        editar_movimiento(id, tipo, descripcion, monto, fecha)

else:
    st.info("No hay movimientos registrados.")
