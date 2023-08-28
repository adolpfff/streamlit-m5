import streamlit as st
import codecs
import pandas as pd
import numpy as np
import plotly.express as px


# Definicón de funciones
@st.cache
def load_data(nrows):
    doc = codecs.open('Employees.csv','rU','latin1')
    data_employee=pd.read_csv(doc, nrows=nrows)
    return data_employee

def findEmployee(_id_var_):
    filtered_data_id = data[data['Employee_ID'].str.upper().str.contains(_id_var_)]
    return filtered_data_id

def findHometown(_ht_var_):
    filtered_data_hometown = data[data['Hometown'].str.upper() == _ht_var_]
    return filtered_data_hometown

def findUnit(_unit_var_):
    filtered_data_unit = data[data['Unit'].str.upper() == _unit_var_]
    return filtered_data_unit

def filter_education_level(_education_var_):
    filtered_data_education = data[data['Education_Level'] == _education_var_]
    return filtered_data_education


# Creación del Dashboard
data = load_data(500)

st.title('Análisis de deserción de empleados')
st.markdown('Sitio que describe el análisis de la deserción de empleados de una compañia')

st.sidebar.title("Información de los Empleados")

if st.sidebar.checkbox('Mostrar toda la información'):
    st.subheader('Todos los empleados')
    st.write(data)

st.markdown('___')

employee_id = st.text_input('Búsqueda por ID del empleado', '')
BuscarEmployee = st.button('Buscar ID')

hometown = st.text_input('Búsqueda por ciudad del empleado', '')
BuscarHometown = st.button('Buscar ciudad')

unit = st.text_input('Búsqueda por unidad del empleado', '')
BuscarUnit = st.button('Buscar unidad')

if (BuscarEmployee):
    data_id = findEmployee(employee_id.upper())
    count_row = data_id.shape[0]  # Gives number of rows
    st.write(f"Total empleados mostrados por ID: {count_row}")
    st.write(data_id)

if (BuscarHometown):
    data_ht = findHometown(hometown.upper())
    count_row = data_ht.shape[0]  # Gives number of rows
    st.write(f"Total de empleados de la ciudad {hometown} : {count_row}")
    st.write(data_ht)
if (BuscarUnit):
    data_unit = findUnit(unit.upper())
    count_row = data_unit.shape[0]  # Gives number of rows
    st.write(f"Total de empleados de la unidad {unit} : {count_row}")
    st.write(data_unit)


st.sidebar.markdown('___')
education_level = st.sidebar.selectbox("Selecciona el nivel educativo", np.sort(data['Education_Level'].unique()))
btnFilterbyeducation = st.sidebar.button('Filtrar nivel educativo')

if (btnFilterbyeducation):
    educationLevel = filter_education_level(education_level)
    st.markdown('___')
    count_row = educationLevel.shape[0]
    st.write(f"Total de empleados con nivel educativo {education_level} :  {count_row}")
    st.dataframe(educationLevel)

st.sidebar.markdown('___')
sbHometown = st.sidebar.selectbox('Selecciona una ciudad', np.sort(data['Hometown'].unique()))
btnFilterbyHometown = st.sidebar.button('Filtrar por ciudad')

if (btnFilterbyHometown):
    fltrHometown = findHometown(sbHometown.upper())
    st.markdown('___')
    count_row = fltrHometown.shape[0]
    st.write(f"Total de empleados en {sbHometown} : {count_row}")
    st.dataframe(fltrHometown)


st.markdown('___')
filterUnit = st.selectbox('Selecciona una unidad del empleado', np.sort(data['Unit'].unique()))
btnfilterUnit = st.button('Filtrar unidad')

if (btnfilterUnit):
    data_unit = findUnit(filterUnit.upper())
    count_row = data_unit.shape[0]  # Gives number of rows
    st.write(f"Total unidades mostradas : {count_row}")
    st.write(data_unit)

# Histograma de la edad de los empleados
st.markdown('___')
fig_employee_by_age = px.histogram(data,
                               x=data['Age'],
                               title = 'Distribución de empleados por edad',
                               template='plotly_white')

fig_employee_by_age.update_layout(plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_employee_by_age)
st.markdown('>*Se observa mayor número de empleados con un rango de edad entre 25 y 29 alos de edad*')

# Gráfico de Barras del número de empleados por unidad
st.markdown('___')
df_unit_employee = data[['Unit','Employee_ID']].groupby('Unit').count()
df_unit_employee.rename(columns={'Employee_ID':'Numero de empleados'}, inplace=True)
fig_employee_unit = px.bar(df_unit_employee,
                           y=df_unit_employee.index,
                           x=df_unit_employee['Numero de empleados'],
                           orientation='h',
                           color_discrete_sequence=['#7ECBB4'],
                           title='Número de empleados por unidad')

fig_employee_unit.update_layout(plot_bgcolor='rgba(0,0,0,0)')

st.plotly_chart(fig_employee_unit)
st.markdown('>*Hay mayor número de empleados en la unidad de IT, seguido por Logpistica y Ventas*')

# Gráfico del ídice de deserción por ciudad
st.markdown('___')
df_attrition = data[['Hometown','Attrition_rate']].groupby('Hometown').mean('Attrition_rate')
df_attrition.rename(columns={'Attrition_rate':'Índice de deserción'}, inplace=True)
fig_attrition_by_hometown = px.bar(df_attrition,
                           x=df_attrition.index,
                           y=df_attrition['Índice de deserción'],
                           color_discrete_sequence=['#ff006e'],
                           title='Índice de deserción por ciudad')

fig_attrition_by_hometown.update_layout(plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_attrition_by_hometown)
st.markdown('>*Se observa mayor índice de deserción en la ciudad de Clinton*')

# Gráfico del ídice de deserción por edad
st.markdown('___')
df_attrition_age = data[['Age','Attrition_rate']].groupby('Age').mean('Attrition_rate')
df_attrition_age.rename(columns={'Attrition_rate':'Índice de deserción'}, inplace=True)
fig_attrition_by_age = px.bar(df_attrition_age,
                           x=df_attrition_age.index,
                           y=df_attrition_age['Índice de deserción'],
                           color_discrete_sequence=['#3a86ff'],
                           title='Índice de deserción por edad')

fig_attrition_by_age.update_layout(plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_attrition_by_age)
st.markdown('>*Los empleados con 23 años de edad tienen mayor índice de deserción*')

# Gráfico del ídice de deserción por tiempo de servicio
st.markdown('___')
service=data['Time_of_service']
atrittion=data['Attrition_rate']
fig_service_atrition=px.scatter(data,
                                x=service,
                                y=atrittion,
                                title='Relación entre el Índice de deserción y el Tiempo de servicio',
                                template='plotly_white')
fig_service_atrition.update_layout(plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_service_atrition)
st.markdown('>*Existe poca relación entre el tiempo de servicio y el índice de deserción, pero se puede observar que los empleados con a lo mas 30 años de servicio tienen mayor índice de deserción*')