#!/usr/bin/env python
# coding: utf-8

# In[579]:


import pandas as pd
import numpy as np
import os
import csv
from pylab import*
import numpy as np
import scipy.stats 
from scipy.special import gamma
import seaborn as sns
from scipy.stats import beta
from scipy.stats import spearmanr


# In[580]:


#Ejercicio 1
baseinterna = pd.read_csv("/Users/nefta/Downloads/base_ini_interna.csv")


# In[581]:


baseinterna
# En la base interna tenemos 9 variables, con un total de 50,000, los cuales son clientes que solicitan un prestamo.Cada cliente cuenta con un ID UNICO.
# con la fecha en la que solicta el prestamo. Contaos con 4 distintos componentes lo cuales son.
#El comp_interno1 nos indica la cantidad de dinero que tiene dentro del banco.
# El comp_interno2 es la caracteristica del prestamo que esta solicitando cada cliente.
# El comp_interno3 nos indica el numero de adeudos que tiene el cliente.
# El comp_interno 4 , podemos suponer que nos indica la edad del cliente por el rango en el que se encuntran los datos en el cual el minimo es de 24 anios 
# y el maximo de 79.
# Categoria 1 podemos suponer que nos indica el rango de ingresos que tiene cada cliente.
# Podemos suponer que categoria2 es el rango de estudios del cliente.
#Por lo que podemos decir que las variables que no nos sirven son, comp_interno4 y todas las que son tipo categorico ya que no nos dan informacion suficiente 
# para poder decidir si se le otroga el prestamo.


# In[582]:


print(baseinterna["comp_interno4"].max())
print(baseinterna["comp_interno4"].min())


# In[583]:


baseinterna= baseinterna.drop(["comp_interno4", "categoria1", "categoria2", "categoria3"],axis =1)
baseinterna
#se eliminan las variables con informacion deficiente


# In[584]:


baseexterna = pd.read_csv("/Users/nefta/Downloads/base_ini_externa.txt", sep=" ")


# In[585]:


baseexterna 


# In[586]:


#Convertimos base_ini_externa.txt en un dataframe 
# En esta tabla tenemos el ID de cada cliente que solicita un prestamo y cuatro distintos componentes externos:
#comp_externo1 es el ingreso diario del cliente 
#comp_externo2 es la razon de ingresos y egresos del cliente 
#comp_externo 3 es la diferencia entre ingresos y egresos 
#comp_externo no aporta informacion relevante


# In[587]:


print(baseexterna["comp_externo2"].max())
print(baseexterna["comp_externo2"].min())
print(baseexterna["comp_externo3"].max())
print(baseexterna["comp_externo3"].min())
print(baseexterna["comp_externo4"].unique())


# In[588]:


baseexterna= baseexterna.drop(["comp_externo4"],axis =1)
baseexterna


# In[589]:


basecomp2 = pd.read_csv("/Users/nefta/Downloads/base_comportamiento_2.txt",sep=" ")
basecomp2
#En esta tabla nos dan el registro de los clientes a los que se les dio el prestamo, mediantes los folios(num_caso) que se les asigno.
#Mes_informacion nos representa las fechas en las que se realizaria el pago del prestamo.
#Concluimos que no se elimina ninguna variable debido a que todas nos proporcinan informacion acerca delas personas que recibieron el prestamo. 


# In[590]:


basecomp2_corr = basecomp2.groupby(['num_caso']).count()
basecomp2_corr= basecomp2_corr.drop(["mes_informacion"], axis=1)
basecomp2_corr


# In[591]:


basecomp3 = pd.read_csv("/Users/nefta/Downloads/base_comportamiento_3.csv")
basecomp3
#En esta base podemos notar que el comportamiento j nos dice el numero de pagos pendiente del cliente que ya recibio el prestamo, si en la base aparece un cero 
#quiere decir que no debe ningun pago, pero si en la base aparece 1,2,3,... quiere decir que debe esos pagos, si en la base aparece un cero despues
# de un numero mayor o igual a uno quiere decir que ya liquido los pagos pendientes. Por lo que con base a esta informacion podriamos hacer una clasificaccion de los clientes
# si el numero de veces que aparace un numero mayor o igual a 1 es cero, entonces podriamos calificar como un buen cliente ya que no tiene ningun adeudo, 
# y su calificacion ira bajando entre mas adeudos tenga


# In[592]:


basecomp3_cor = basecomp3[ basecomp3["comportamiento_j"]>0]
basecomp3_cor= basecomp3_cor.drop(["mes_informacion"], axis=1)
basecomp3_corr= basecomp3_cor.groupby(["num_caso"]).count()
basecomp3_corr


# In[593]:


basecompmixto = pd.read_csv("/Users/nefta/Downloads/base_ini_parte1.csv")


# In[594]:


basecompmixto
# En esta tabla nos dan los dos ID's que le corresponden a cada cliente.
#El comp_mixto1 es el indice entre el comp_interno1 y el comp_externo1
# Al no tener informacion comp_mixto1 decidimos no ocupar dicha variable


# In[595]:


basecompmixto= basecompmixto.drop(["comp_mixto1"],axis =1)
basecompmixto


# In[596]:


basecompint4 = pd.read_table("/Users/nefta/Downloads/bd_inicio_parte1.txt")


# In[597]:


basecompint4
#podemos ver que tiene los mismo datos que la base interna, por lo que los datos que necesitamos los podemos obtener de esa tabla
#por lo que no es necesario usar esta base 


# In[598]:


baseinversion = pd.read_csv("/Users/nefta/Downloads/base_inversion.txt", sep=" ")


# In[599]:


baseinversion


# In[600]:


#En esta tabla tenemos dos variables en la cual nos representa el id2 de cada cliente y su inversion en el banco presente


# In[601]:


cruce1 = pd.merge(baseinterna, baseexterna, how="inner", on=["_id_"])
cruce1
#En este cruce ya tenemos los comportaminetos internos y extrernos que les corresponden a cada cliente


# In[602]:


cruce2= pd.merge(basecompmixto, cruce1, how="inner", on=["_id_"])
cruce2


# In[603]:


cruce3= pd.merge(cruce1, cruce2, how="outer", on=["_id_","fecha_inicio",'comp_interno1','comp_interno2','comp_interno3','comp_externo1','comp_externo2','comp_externo3'])
cruce3


# In[604]:


cruce4= pd.merge(basecomp2_corr, basecomp3_corr, how="outer", on=["num_caso"])
cruce4.fillna(0)
# En este cruce nos proporciona la duracion del credito y el numero veces en las que tenia adeudo. 


# In[ ]:


#Podemos notar que no se puede realizar un cruce entre el cruce 3 y 4 debido a que no cuentan con variables iguales.

