## Práctica 2

Este repositorio contiene scripts de [Python](https://www.python.org/) para ejecutar análisis de conectividad con distintos atlas de parcelación. Funciona para la ejecución de 1 sujeto a la vez. 

### Consideraciones para la ejecución ⚙
 
Los scripts asumen que los datos fueron previamente preprocesados y hay funciones que únicamente tienen compatibilidad con outputs del pipeline [fMRIPrep](https://fmriprep.org/en/20.1.1/index.html).

Las carpetas y los nombres de los archivos deben seguir el formato [BIDS](https://bids-specification.readthedocs.io/en/stable/). La estructura general de un directorio BIDS (con datos sin preprocesar) es la siguiente:

```
data/bids/
├── CHANGES
├── dataset_description.json
├── LICENSE
├── participants.json
├── participants.tsv
├── README
├── README.md
├── sub-002
│   ├── anat
│   │   ├── sub-002_T1w.json
│   │   └── sub-002_T1w.nii.gz
│   ├── fmap
│   │   ├── sub-002_dir-PA_epi.json
│   │   └── sub-002_dir-PA_epi.nii.gz
│   └── func
│       ├── sub-002_task-rest_bold.json
│       └── sub-002_task-rest_bold.nii.gz
```

La estructura mínima que requieren los scripts para su ejecución es la siguiente:

```
data/bids/
├── dataset_description.json
├── sub-001
│   └── ses-1 
│  	   └── func
│      		 ├── sub-001_task-rest_desc-preproc_bold.json
│		 └── sub-001_task-rest_desc-confounds_regressors.tsv
│		 ├── sub-001_task-rest_bold.dtseries.json
│		 └── sub-001_task-rest_bold.dtseries.nii
```

### Descargando este repositorio 🔽


Para tener estos datos en tu cuenta debes clonar el repositorio. Ubica el icono code en la parte superior de esta página y copia la URL de la opción ‘HTTPS’. 

![icono](https://docs.github.com/assets/cb-36330/images/help/repository/https-url-clone.png)

Ve a tu sesión y ubicate en la terminal:

![terminal_vc](https://i.stack.imgur.com/bTPA1.jpg)

Pega la url que copiaste escribiendo el comando ```git clone``` con la siguiente estructura:

```
git clone git@github.com:usuario/repositorio.git
```
### Cargando el entorno virtual 📂

Este repositorio cuenta con un entorno virtual generado mediante [pipenv](https://pipenv-es.readthedocs.io/es/latest/). Este ambiente contiene información sobre todos los paquetes externos a  python que se requieren para la ejecución de los scripts. Para instalar los paquetes que viven en los archivos ```Pipfile``` y ```Pipfile.lock``` ejecuta el siguiente comando en tu terminal:

```
pipenv sync
```

### Ejecutando un script 📑

Para ejecutar el script, primero debes asegurarte de actualizar la ruta de ```fmri_dir```. Una vez que te has asegurado de que el script trabaje con los datos del sujeto que elegiste, ejecuta tu archivo dentro del ambiente virtual con:

```
pipenv run python CF.py
```
Este comando ejecuta todas las instrucciones del script siempre y cuando estén escritas de manera adecuada. Para seleccionar un atlas de parcelación distinto solo debes ejecutar el archivo con el nombre del atlas elegido (ej. ```pipenv run python CF_pauli.py```).

También puedes ir ejecutando cada línea del script. Para esto ejecuta en la terminal el comando:

```
pipenv run python
```
Al copiar y pegar las instrucciones en la terminal irás ejecutando cada línea de manera independiente. 

### Consideraciones sobre el análisis de conectividad 🧠

Los scripts trabajan principalmente con funciones del paquete [Nilearn](https://nilearn.github.io/stable/index.html). Nilearn contiene un conjunto de datos precargados, entre ellos atlas a los que puede accederse con el comando ```fetch_atlas_nombre_atlas()```. Este repositorio cuenta con ejemplos de uso de 5 atlas de parcelación distintos:

**Funcionalmente definidos**
 + Yeo 17 Networks. Consulta: [documentación de nilearn](https://nilearn.github.io/stable/modules/generated/nilearn.datasets.fetch_atlas_yeo_2011.html#nilearn.datasets.fetch_atlas_yeo_2011) o [articulo](https://journals.physiology.org/doi/full/10.1152/jn.00338.2011).
 + Schaefer 100 Parcelas. Consulta: [documentación de nilearn](https://nilearn.github.io/stable/modules/generated/nilearn.datasets.fetch_atlas_schaefer_2018.html#nilearn.datasets.fetch_atlas_schaefer_2018) o [articulo](https://academic.oup.com/cercor/article/28/9/3095/3978804?login=false)

**Anatómicamente definidos**
 + Harvard-Oxford (48 regiones). Consulta [documentación de nilearn](https://nilearn.github.io/stable/modules/generated/nilearn.datasets.fetch_atlas_harvard_oxford.html#nilearn.datasets.fetch_atlas_harvard_oxford), [visualización](https://neurovault.org/collections/262/) o [documentación de FSL](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases)
 + Broadmann (Versión atlas de Talairach).  Consulta [documentación de nilearn](https://nilearn.github.io/stable/modules/generated/nilearn.datasets.fetch_atlas_talairach.html#nilearn.datasets.fetch_atlas_talairach) o [página del atlas](http://talairach.org/about.html#Labels)
 + Pauli (atlas subcortical). Consulta [documentación de nilearn](https://nilearn.github.io/stable/modules/generated/nilearn.datasets.fetch_atlas_pauli_2017.html#nilearn.datasets.fetch_atlas_pauli_2017) o [artículo](https://www.nature.com/articles/sdata201863)

Para conocer otros atlas y datos disponibles consulta [nilearn.datasets](https://nilearn.github.io/stable/modules/reference.html#module-nilearn.datasets).

Consulta la documentación de otras funciones de nilearn empleadas en los scripts:
* [load_confounds](https://nilearn.github.io/stable/modules/generated/nilearn.interfaces.fmriprep.load_confounds.html#nilearn.interfaces.fmriprep.load_confounds).
* [NiftiLabelsMasker y fit_transform](https://nilearn.github.io/stable/modules/generated/nilearn.maskers.NiftiLabelsMasker.html#nilearn.maskers.NiftiLabelsMasker).
* [load_img](https://nilearn.github.io/stable/modules/generated/nilearn.image.load_img.html#nilearn.image.load_img).
* [ConnectivityMeasure](https://nilearn.github.io/stable/modules/generated/nilearn.connectome.ConnectivityMeasure.html#nilearn.connectome.ConnectivityMeasure).
* [find_parcellation_cut_coords](https://nilearn.github.io/stable/modules/generated/nilearn.plotting.find_parcellation_cut_coords.html#nilearn.plotting.find_parcellation_cut_coords).
* [plot_connectome](https://nilearn.github.io/stable/modules/generated/nilearn.plotting.plot_connectome.html#nilearn.plotting.plot_connectome).
* [plot_matrix](https://nilearn.github.io/stable/modules/generated/nilearn.plotting.plot_matrix.html#nilearn.plotting.plot_matrix).

Consulta la [documentación general](https://nilearn.github.io/stable/user_guide.html) y los [ejemplos de uso de nilearn](https://nilearn.github.io/stable/auto_examples/index.html).

Consulta [esta alternativa para graficar la matriz de correlación](https://brainiak.org/tutorials/08-connectivity/). 

Consulta otros paquetes de python empleados en el script:
* [bids](https://bids-standard.github.io/pybids/generated/bids.layout.BIDSLayout.html?highlight=bidslayout#bids.layout.BIDSLayout). 
* [matplotlib.pyplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html)
* [numpy.save](https://numpy.org/doc/stable/reference/generated/numpy.save.html).

Adicionalmente puedes consultar el ejercicio de [esta lección](https://carpentries-incubator.github.io/SDC-BIDS-fMRI/07-functional-connectivity-analysis/index.html) para ver un análisis de correlación con múltiples sujetos. 

### Consideraciones sobre la práctica
Debes ajustar la ruta del objeto ```fmri_dir``` para que coincida con la ubicación de los archivos. Ejemplo, tus carpetas siguen esta estructura:

```
data/bids/
├── dataset_description.json
├── sub-001
│   └── ses-1 
│  	   └── func
│      		 ├── sub-001_task-rest_desc-preproc_bold.json
│		 └── sub-001_task-rest_desc-confounds_regressors.tsv
│		 ├── sub-001_task-rest_bold.dtseries.json
│		 └── sub-001_task-rest_bold.dtseries.nii
├── sub-002
│   └── ses-1 
│  	   └── func
│      		 ├── sub-002_task-rest_desc-preproc_bold.json
│		 └── sub-002_task-rest_desc-confounds_regressors.tsv
│		 ├── sub-002_task-rest_bold.dtseries.json
│		 └── sub-002_task-rest_bold.dtseries.nii
├── sub-003
│   └── ses-1 
│  	   └── func
│      		 ├── sub-003_task-rest_desc-preproc_bold.json
│		 └── sub-003_task-rest_desc-confounds_regressors.tsv
│		 ├── sub-003_task-rest_bold.dtseries.json
│		 └── sub-003_task-rest_bold.dtseries.nii

```
La ruta dentro de tu objeto debe ser: ```fmri_dir='/data/bids/'```

Además de la ruta, debes ajustar el sujeto con el que vas a trabajar. El script está programado para mostrarte en qué orden están acomodados los archivos al ejecutar las líneas:
```
sub=layout.get_subjects()
print("Los IDs de los sujetos encontrados en el directorio BIDS son: {0}".format(sub)) 
```
Para la carpeta del ejemplo, la salida en la terminal se vería así:

```
Los IDs de los sujetos encontrados en el directorio BIDS son: ['001', '002','003']
```
Python asigna a cada elemento una posición en particular, empezando desde cero:

```
'001' [0]
'002' [1]
'003' [2]
```
Para recuperar algún elemento en particular, basta con especificar la posición asignada por Python. En el script, hay 3 líneas que son muy importantes, pues recuperan los datos de un solo sujeto. Estas son las líneas:
```
func_file = func_files[1]
confounds_file = confounds_simple[1]
sample_file = sample_mask[1]
```
Esta instrucción le está indicando a Python que acceda a los objetos almacenados en la posición 1, en nuestro ejemplo serían datos del sujeto con el identificador (ID) 002. 

Considera que si no modificas las notas que se imprimen en la terminal con la función ```print()``` el script no va a reflejar en automático el cambio de sujeto con el que está trabajando. Por ejemplo, si modificaste los objetos ```func_files```,```confounds_simple``` y ```sample_mask``` pero no la instrucción ```print('Se recuperaron datos del sujeto {0}'.format(sub[0]))```, el script estará procesando los datos del sujeto 002, pero en terminal verás el mensaje:
```
Se recuperaron datos del sujeto 001
```
Puedes modificar esto al poner la posición 1 en la instrucción: ```print('Se recuperaron datos del sujeto {0}'.format(sub[1]))``` y ahora tu salida en terminal reflejaría los datos con los que está trabajando el script (mostraría ```Se recuperaron datos del sujeto 002```). Se tendrían que corregir de la misma forma todos los comandos que incluyan ```.format(sub[0])```.


