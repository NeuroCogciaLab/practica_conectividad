"""
Script para ejecutar el análisis de conectividad de 1 sujeto con parcelación con el atlas Harvard-Oxford con 48 regiones
"""
from bids import BIDSLayout
from nilearn import image as nimg
from nilearn import datasets, plotting
from nilearn.maskers import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from nilearn.interfaces.fmriprep import load_confounds
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Se carga la carpeta en que se encuentran tus datos
"""Ajusta la ruta de los archivos en fmri_dir para que coincida con 
la ubicación en que se encuentran los datos de tu equipo"""

fmri_dir='/home/ebotello/CF_atlas/bids_dir/'
layout=BIDSLayout(fmri_dir,config=['bids','derivatives'])

# Se obtienen los sujetos que se encuentran en la carpeta
sub=layout.get_subjects()
print("""Los sujetos encontrados en el directorio BIDS son: sub-{0} y sub-{1}""".format(sub[0],sub[1]))

# Se obtienen los archivos de los sujetos (funcional y máscara)
func_files=layout.get(subject=sub,datatype='func',task='rest',desc='preproc',space='MNI152NLin2009cAsym',extension='nii.gz',return_type='file')

confounds_simple , sample_mask = load_confounds(func_files,strategy=("high_pass","motion","wm_csf","ica_aroma","scrub"),motion="basic",wm_csf="basic",ica_aroma="basic")

print('Se obtuvieron datos del archivo NiFTI y la máscara cerebral de los sujetos')

# Se carga el atlas de parcelación a usar
harv_oxf = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
atlas_filename = harv_oxf.maps
roi_names = harv_oxf.labels
roi_names.remove('Background')
print('La imagen nifti del atlas Harvard-Oxford se localiza '
'en: %s' % atlas_filename)   

# Crea una máscara para extraer los datos funcionales de las parcelas del atlas
masker= NiftiLabelsMasker(labels_img=atlas_filename, standardize=True, memory='nilearn_cache',verbose=5,detrend=True,low_pass = 0.08, high_pass = 0.009,t_r=2)
         
# Obtiene los datos del primer sujeto 
func_file=func_files[1]
confounds_file=confounds_simple[1]
sample_file=sample_mask[1]
print('Se recuperaron datos del sujeto {0}'.format(sub[1]))

# Carga la imagen funcional (NIFTI 4D) del sujeto
func_img=nimg.load_img(func_file)
print('Se cargó la imagen funcional del sujeto sub-{0}'.format(sub[1]))

# Se extrae la serie temporal de las regiones del atlas en el sujeto
print('Preparándose para extraer la serie temporal de las ROIs... Cargando datos:')
time_series=masker.fit_transform(func_img,confounds=confounds_file,sample_mask=sample_file)
roi_shape=time_series.shape
print('Se obtuvo la serie temporal de las ROI para el sujeto {0}'.format(sub[1]))
print('La extracción se hizo para X y Y (X=Puntos temporales,Y=Número de regiones): {0}'.format(roi_shape))

# Calculando la conectividad 
correlation_measure = ConnectivityMeasure(kind='correlation')
correlation_matrix = correlation_measure.fit_transform([time_series])
corr_mat_shape=correlation_matrix.shape
print("""Se construyó una matriz de conectividad con las características:
(numero de sujetos,número de regiones, número de regiones):{0}""".format(corr_mat_shape))

# Guardando la matriz de correlación 
print("Guardando datos...")
numpy_matrix=np.squeeze(correlation_matrix)
np.save('matriz_correlacion_Harv-Oxf.npy',numpy_matrix)

# Graficando la matriz de correlación
coordinates= plotting.find_parcellation_cut_coords(labels_img=atlas_filename)
plotting.plot_connectome(correlation_matrix[0],coordinates,edge_threshold="30%",title='Harvard-Oxford 48')
plt.savefig("conectoma_Harv-Oxf.png")

plotting.plot_matrix(correlation_matrix[0],labels=roi_names,figure=(11, 10),auto_fit=True,reorder='single' ,colorbar=True, vmax=1,vmin=-1)
plt.savefig("matriz_conectividad_Harv-Oxf.png")

import os
ubicacion=os.getcwd()
print("""Se guardaron 3 archivos:
  -Archivo con resultados numéricos de correlaciones: matriz_correlacion_Harv-Oxf.npy
  - Imagen del grafo (retiene 30% de las conexiones más fuertes): conectoma_Harv-Oxf.png
  - Imagen de la matriz de conectividad: matriz_conectividad_Harv-Oxf.png
  Puedes encontrarlos en {0}""".format(ubicacion))
