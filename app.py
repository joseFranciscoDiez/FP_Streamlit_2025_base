import streamlit as st
import pandas as pd

class Paciente:
	def __init__(self, nombre, alergenos):
		self.nombre = nombre
		self.restricciones = restricciones
		self.historico_dietas = []

	def __repr__(self):
		return f"Paciente({self.nombre}, {self.restricciones})"

class CentroSalud:
	def __init__(self, nombre):
		self.nombre = nombre
		self.pacientes = []
		# completa

	def agregar_paciente(self, paciente):
		self.pacientes.append(paciente)

	def eliminar_paciente(self, nombre):
		# Es un poco distinto, en este caso se elimina por nombre
		self.pacientes = [p for p in self.pacientes if p.nombre != nombre]

	def asignar_dieta(self):
		pass

	def resumen_dietas(self):
		resumen = {}
		for paciente in self.pacientes:
			resumen[paciente.nombre] = paciente.historico_dietas
		return pd.DataFrame(resumen)

if "hubu" not in st.session_state:
	st.session_state.hubu = CentroSalud("HUBU")

if "mostrar_formulario_anadir" not in st.session_state:
	st.session_state.mostrar_formulario_anadir = False
if "mostrar_formulario_eliminar" not in st.session_state:
	st.session_state.mostrar_formulario_eliminar = False

def main():
	st.title("Gestión de Pacientes y Dietas")
	st.subheader("Pantalla Principal")


	col1, col2, col3, col4 = st.columns(4)

	if col1.button("Añadir Paciente"):
		st.session_state.mostrar_formulario_anadir = True
		st.session_state.mostrar_formulario_eliminar = False
        

	if col2.button("Eliminar Paciente"):
		st.session_state.mostrar_formulario_eliminar = True
		st.session_state.mostrar_formulario_anadir = False
       
    
	if col3.button("Asignar Dieta"):
		st.session_state.hubu.asignar_dieta()
		st.success("Dietas asignadas a todos los pacientes.")
		st.session_state.mostrar_formulario_eliminar = False
		st.session_state.mostrar_formulario_anadir = False

	if col4.button("Resumen de Dietas"):
		mostrar_resumen_dietas()
		st.session_state.mostrar_formulario_eliminar = False
		st.session_state.mostrar_formulario_anadir = False

	if st.session_state.mostrar_formulario_anadir:
		mostrar_formulario_anadir()
	if st.session_state.mostrar_formulario_eliminar:
		mostrar_formulario_eliminar()

def mostrar_formulario_anadir():
	st.header("Añadir Paciente")
	alergenos_opciones = ["Gluten", "Lácteos", "Frutos secos"]

	with st.form("form_anadir_paciente"):
		nombre = st.text_input("Nombre")
		alergenos = st.multiselect("Alérgenos", alergenos_opciones)
		submitted = st.form_submit_button("Añadir")


	if submitted:
		if not nombre.strip():
			st.error("El nombre del paciente no puede estar vacío.")
			st.stop()
		else:
			nuevo_paciente = Paciente(nombre, alergenos)
			st.session_state.hubu.agregar_paciente(nuevo_paciente)
			st.success(f"Paciente {nombre} añadido con éxito.")
			st.session_state.mostrar_formulario_anadir = False
			st.rerun()

def mostrar_formulario_eliminar():
	st.header("Eliminar Paciente")

	if not st.session_state.hubu.pacientes:
		st.warning("No hay pacientes para eliminar.")
		st.stop()
    
	nombres_pacientes = [p.nombre for p in st.session_state.hubu.pacientes]
	nombre_seleccionado = st.selectbox("Selecciona un paciente para eliminar", nombres_pacientes)


	if st.button("Eliminar"):
		st.session_state.hubu.eliminar_paciente(nombre_seleccionado)        
		st.success(f"Paciente {nombre_seleccionado} eliminado con éxito.")
		st.session_state.mostrar_formulario_eliminar = False
		st.rerun()

def mostrar_resumen_dietas():
	st.header("Resumen de Dietas")
	if not st.session_state.hubu.pacientes:
		st.warning("No hay pacientes registrados.")
	else:
		resumen = st.session_state.hubu.resumen_dietas()
		st.dataframe(resumen)

if __name__ == "__main__":
	main()
