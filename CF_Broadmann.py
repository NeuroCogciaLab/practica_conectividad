"""
Script para ejecutar el análisis de conectividad de 1 sujeto con parcelación con el mapa de Broadmann
"""
from bids import BIDSLayout
from nilearn import image as nimg
from nilearn import datasets, plotting
from nilearn.maskers import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure
from nilearn.interfaces.fmriprep import load_confounds
import matplotlib.pyplot as plt
import numpy as np
# Se carga la carpeta en que se encuentran tus datos
"""Ajusta la ruta de los archivos en fmri_dir para que coincida con 
la ubicación en que se encuentran los datos en tu cuenta"""

fmri_dir='/home/ebotello/CF_atlas/bids_dir/'
layout=BIDSLayout(fmri_dir,config=['bids','derivatives'])

# Se obtienen los sujetos que se encuentran en la carpeta
sub=layout.get_subjects()
print("""Los sujetos encontrados en el directorio BIDS son: sub-{0} y sub-{1}""".format(sub[0],sub[1]))

# Se obtienen los archivos de los sujetos (funcional y máscara)
func_files=layout.get(subject=sub,datatype='func',task='rest',desc='preproc',space='MNI152NLin2009cAsym',extension='nii.gz',return_type='file')

confounds_simple , sample_mask = load_confounds(func_files,strategy=("high_pass","motion","wm_csf","ica_aroma","scrub"),motion="basic",wm_csf="basic",ica_aroma="basic")

mask_files= layout.get(subject=sub,datatype='func',task='rest',desc='brain',suffix="mask",space='MNI152NLin2009cAsym',extension='.nii.gz',return_type='file')

print('Se obtuvieron datos del archivo NiFTI y la máscara cerebral de los sujetos')

# Se carga el atlas de parcelación a usar
broadmann = datasets.fetch_atlas_talairach(level_name='ba')
print('La imagen nifti (3D) del mapa de Broadmann se localiza '
'en: %s' % broadmann['maps'])   

# Crea una máscara para extraer los datos funcionales de las parcelas del atlas
masker= NiftiLabelsMasker(labels_img=broadmann['maps'], standardize=True, memory='nilearn_cache',verbose=1,detrend=True,low_pass = 0.08, high_pass = 0.009,t_r=2)
         
# Obtiene los datos del primer sujeto 
func_file=func_files[0]
mask_file=mask_files[0]
confounds_file=confounds_simple[0]
sample_file=sample_mask[0]
print('Se recuperaron datos del sujeto {0}'.format(sub[0]))

# Carga la imagen funcional (NIFTI 4D) del sujeto
func_img=nimg.load_img(func_file)
print('Se cargó la imagen funcional del sujeto sub-{0}'.format(sub[0]))

# Se extrae la serie temporal de las regiones del atlas en el sujeto
time_series=masker.fit_transform(func_img,confounds=confounds_file,sample_mask=sample_file)
roi_shape=time_series.shape
print('Se obtuvo la serie temporal de las ROI para el sujeto {0}'.format(sub[0]))
print('Puntos temporales, número de regiones: {0}'.format(roi_shape))

# Calculando la conectividad 
correlation_measure = ConnectivityMeasure(kind='correlation')
correlation_matrix = correlation_measure.fit_transform([time_series])
corr_mat_shape=correlation_matrix.shape
print("""Se construyó una matriz de conectividad con las características:
(numero de sujetos,número de regiones, número de regiones):{0}""".format(corr_mat_shape))
# Guardando la matriz de correlación 
numpy_matrix=np.squeeze(correlation_matrix)
np.save('matriz_correlacion.npy',numpy_matrix)

# Graficando la matriz de correlación
coordinates= plotting.find_parcellation_cut_coords(labels_img=broadmann['maps'])
plotting.plot_connectome(correlation_matrix[0],coordinates,edge_threshold="80%",title='Mapa de Broadmann')
print('Se generó el gráfico de la matriz, preparando para mostrarlo...')
plt.savefig("conectoma.png")
#plt.show()

plotting.plot_matrix(correlation_matrix[0],labels=broadmann['labels'],colorbar=True, vmax=1,vmin=-1)
plt.savefig("matriz_conectividad.png")
#plt.show()
