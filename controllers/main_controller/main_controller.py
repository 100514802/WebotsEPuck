"""main_controller."""
# En este fichero se escoge el controlador que se quiere emplear:
# - Siguemuros: el robot avanza hasta chocar con un muro y lo recorre hasta la meta
# - Algoritmo Bug 0
# - Algoritmo Bug 1
import os
# Defino una función para lanzar el controlado escogido
def run(runfile):
    try:
        with open(runfile, 'r') as rnf:
            exec(rnf.read())
    except Exception as e:
        print(f"Error al ejecutar '{runfile}': {e}")

# Seleccione el algoritmo que desea emplear        
#algoritmo = 'BUG1'
#algoritmo = 'BUG1'
algoritmo = 'SIGUEMUROS'

# Seleccione a que esquina del mapa quiere llegar
#goal = 1 # punto (4.5, 10.5)
goal = 2 # esquina diagonal opuesta (12.5, 10.5)
#goal = 3 # punto (12.5, 5.5)

# Ejecutamos la función definida para lanzar el algoritmo elegido (especificando su ruta)
if algoritmo == 'BUG0':
    print(f'Ejecutando el algoritmo: {algoritmo}')
    run(os.path.join('..', 'bug_0', 'bug_0.py')) # Lanzo el fichero bug_0.py
elif algoritmo == 'BUG1':
    print(f'Ejecutando el algoritmo: {algoritmo}')
    run(os.path.join('..', 'bug_1', 'bug_1.py')) # Lanzo el fichero bug_1.py
elif algoritmo == 'SIGUEMUROS':
    print(f'Ejecutando el algoritmo: {algoritmo}')
    run(os.path.join('..', 'siguemuros', 'siguemuros.py')) # Lanzo el fichero siguemuros.py
else: # Si el algoritmo elegido no se corresponde a ninguno de los definidos
    print('ALGORITMO DESCONOCIDO INGRESADO!')
    archivo_a_ejecutar = None 
