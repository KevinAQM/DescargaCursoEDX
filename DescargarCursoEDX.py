#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importando librerías necesarias
import requests 
import os
from bs4 import BeautifulSoup
from humanfriendly import format_timespan
import time

begin_time = time.time()

# Pegar la URL de cada módulo aquí: notar que la url va entre comillas simples ' 
module0_url = 'https://delftxdownloads.tudelft.nl/EnerTran1x_Energy_Markets_of_Today/Module_0/'
module1_url = 'https://delftxdownloads.tudelft.nl/EnerTran1x_Energy_Markets_of_Today/Module_1/'
module2_url = "https://delftxdownloads.tudelft.nl/EnerTran1x_Energy_Markets_of_Today/Module_2/"
module3_url = 'https://delftxdownloads.tudelft.nl/EnerTran1x_Energy_Markets_of_Today/Module_3/'
module4_url = 'https://delftxdownloads.tudelft.nl/EnerTran1x_Energy_Markets_of_Today/Module_4/'

all_urls = [module0_url, module1_url, module2_url, module3_url, module4_url]

print('---> DESCARGANDO EL CURSO "ENERGY MARKETS OF TODAY" DE TUDELFT <---')

course_folder = 'Energy Markets of Today - TUDelft'

# Creando la carpeta general de curso
try:
    os.mkdir(course_folder)
    print("")
except FileExistsError:
    print("")

# Generando licencia de software
with open('LICENCE.txt', "w") as file:
    file.write('MIT License\n\nCopyright (c) 2020 Kevin A. Quispe Mendizábal\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.')

# Generando licencia de curso
with open('Energy Markets of Today - TUDelft\TUDelft Copyright.txt', "w") as file:
    file.write('Unless otherwise specified the Course Materials of this course are Copyright Delft University of Technology and are licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.\n\nFor further information: https://creativecommons.org/licenses/by-nc-sa/4.0/')

# ----------------------------------------------------------------------
# Descarga archivos para cada url (módulo)
for module_url in all_urls:
    
    # Creando carpetas para módulos
    import os
    
    dirName = module_url[-9:-1].upper()
    dirName = dirName.replace("O", "Ó")
    dirName = dirName.replace("E", "O")
    dirName = dirName.replace("_", " ")

    try:
        os.mkdir('Energy Markets of Today - TUDelft/{}'.format(dirName))
        print("----------------------------------------------")
        print("LA CARPETA DEL '" + dirName.upper() +  "' HA SIDO CREADA")
    except FileExistsError:
        print("----------------------------------------------")
        print("LA CARPETA DEL'" + dirName.upper() +  "' YA EXISTÍA")

# ----------------------------------------------------------------------

    def get_file_links(): 

        # Crear objeto de respuesta de los módulos del curso
        r = requests.get(module_url) 

        # Crear objeto beautiful-soup
        soup = BeautifulSoup(r.content,'html5lib') 

        # Encuentra links dentro de la página web 
        links = soup.findAll('a') 

        # Seleccionando archivos con las siguientes terminaciones: 720.mp4, .srt y slides.pdf
        file_links = [module_url + link['href'] for link in links 
                       if link['href'].endswith('360.mp4') or link['href'].endswith('.srt') or link['href'].endswith('slides.pdf')]

        return file_links

# ----------------------------------------------------------------------

    def download_file_series(file_links): 

        for link in file_links: 

            '''itera a través de todos los enlaces en file_links 
            y descarga uno por uno'''

            # Obteniendo el nombre de cada archivo dividiendo la URL con / y obteniendo la última parte
            file_name = link.split('/')[-1] 
            
            # Texto que se muestra en la descarga
            if file_name[-3:]=='srt':
                print("Descargando subtítulo: " + file_name)
            elif file_name[-3:]=='pdf':
                print("Descargando diapositiva: " + file_name)
            elif file_name[-3:]=='mp4':
                print("Descargando video: " + file_name)

            # Crear objeto de respuesta de cada archivo del curso 
            r = requests.get(link, stream = True) 

            # Empieza la descarga 
            with open('{}/{}/{}'.format(course_folder, dirName, file_name), 'wb') as f: 
                for chunk in r.iter_content(chunk_size = 1024*1024): 
                    if chunk: 
                        f.write(chunk) 

            print("Terminado")

        print("EL "+ dirName.upper()+ " HA SIDO DESCARGADO\n")
        
        return

# ----------------------------------------------------------------------

    if __name__ == "__main__": 

        # Seleccionando los archivos 
        file_links = get_file_links() 

        # Descargando todos los archivos 
        download_file_series(file_links)

print('______________________________________________\n')
print('---> ¡CURSO "ENERGY MARKETS OF TODAY" DESCARGADO! <---\n')

# muestra el tiempo de ejecución
end_time = time.time() - begin_time
print("Tiempo total de descarga: ", format_timespan(end_time))

print(input("\nPresione ENTER para salir del programa: "))

