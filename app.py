import streamlit as st
from datetime import date
import database as db
from calendar import monthrange

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
    if st.button("🗑️", key=f"borrar_btn_{id}", help="Borrar Movimiento"):
        db.borrar_movimiento(id)
        st.success("Movimiento borrado")
        st.rerun()

# Función para duplicar
def duplicar_movimiento(id, tipo, descripcion, monto, fecha):
    if st.button("➕", key=f"duplicar_btn_{id}", help="Repetir Movimiento"):
        db.insertar_movimiento(tipo, descripcion, monto, fecha)
        st.success("Movimiento duplicado")
        st.rerun()


# Configuración de la página Streamlit
st.set_page_config(page_title="Control de Finanzas", page_icon="💰")
st.title("Control de Finanzas")

# Mostrar el balance total arriba
movimientos = db.obtener_movimientos()
if movimientos:
    balance = calcular_balance(movimientos)
    st.markdown(f"<h2 style='text-align:center;'>Balance Total: {balance} €</h2>", unsafe_allow_html=True)


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
    
# Calendario para filtrar por fecha
st.subheader("Filtrar por fecha")
all_dates = {date.fromisoformat(movimiento[4]) for movimiento in movimientos}
min_date = min(all_dates) if all_dates else date.today()
max_date = max(all_dates) if all_dates else date.today()
selected_date = st.date_input("Selecciona una fecha", min_value=min_date, max_value=max_date, value=date.today())

# Función para marcar los días que tienen movimientos
def month_cal(fecha):
  with_moves = set()
  for movimiento in movimientos:
     if date.fromisoformat(movimiento[4]).month == fecha.month and date.fromisoformat(movimiento[4]).year == fecha.year:
         with_moves.add(date.fromisoformat(movimiento[4]))

  def highlight(date):
       return date in with_moves
  return highlight

# Mostrar los movimientos
st.subheader("Movimientos Registrados")


if movimientos:
    # Filtrar movimientos por la fecha seleccionada
    filtered_movimientos = [movimiento for movimiento in movimientos if date.fromisoformat(movimiento[4]) == selected_date]
    # Paginación
    items_per_page = 10
    num_movimientos = len(filtered_movimientos)
    num_pages = (num_movimientos + items_per_page - 1) // items_per_page
    
    if num_pages > 1:
         page = st.slider("Página", min_value=1, max_value=num_pages, step=1,value=1)
    else:
         page = 1

    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, num_movimientos)

    if filtered_movimientos:
      for movimiento in filtered_movimientos[start_index:end_index]:
          id, tipo, descripcion, monto, fecha = movimiento
          
          col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 3, 2, 3])
          
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
          with col6:
              col7, col8, col9=st.columns(3)
              with col7:
                  if st.button("✏️", key=f"edit_btn_{id}", help="Editar Movimiento"):
                      st.session_state[f"editar_{id}"] = True
              with col8:
                  borrar_movimiento(id)
              with col9:
                   duplicar_movimiento(id, tipo, descripcion, monto, fecha)
          editar_movimiento(id, tipo, descripcion, monto, fecha)
    else:
         st.info("No hay movimientos registrados en esta fecha.")
    
    st.calendar(default_value=selected_date,  format='YYYY-MM-DD',  on_change=st.rerun,  key=f'month_cal_{selected_date.year}-{selected_date.month}' ,
             month_names= ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
              day_of_week_names = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
            )
    st.session_state["calendar_highlighter"] = month_cal(selected_date)
    st.session_state["calendar_highlighter"]
else:
    st.info("No hay movimientos registrados.")
