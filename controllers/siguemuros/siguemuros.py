"""master controller."""

# Importamos del modulo del controlador las clases necesarias
# (se corresponden a los elementos con los que vamos a trabajar)
from controller import Robot
from main_controller import goal #importo el punto de destino o meta
import time # se empleará para crear un cronometro y poder comparar el tiempo requerido

# Defino los puntos X e Y a los que debe llegar el robot en funcion del goal elegido    
if goal == 1:
    x_goal = 4.5
    y_goal = 10.5
elif goal == 2:
    x_goal = 12.5
    y_goal = 10.5
elif goal == 3:
    x_goal = 12.5
    y_goal = 5.5
# uestro por terminal las coordenadas de dicho punto
print(f'La meta se encuentra en las coordenadas: {x_goal}, {y_goal}')

# create the Robot instance.
robot = Robot()

# Obtener la instancia de la cámara
camera = robot.getDevice("camera")  
# Establecer la frecuencia de muestreo de la cámara
camera.enable(10) 

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# defino la velocidad max para las ruedas
max_speed = 6.28 # rad/s segun el manual de e-puck

# inicializo los sensores de posicion
ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i])) # Obtengo del robot los valores de ps0... y los guardo en el array ps
    ps[i].enable(timestep) # necesario para que los sensores funcionen

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
motor_left = robot.getDevice('left wheel motor') 
motor_right = robot.getDevice('right wheel motor')
gps = robot.getDevice('gps')
imu = robot.getDevice('inertial unit')

gps.enable(timestep)
imu.enable(timestep)

# Leo la posicion inicial del robot
gps_vals = gps.getValues()
target_reached = False #booleana para indicar que hemos alcanzado el objetivo

motor_left.setVelocity(0.0) #inicio el motor de la rueda izq con velocidad 0
motor_right.setVelocity(0.0) #inicio el motor de la rueda dcha con velocidad 0
# Para que los motores giren continuamente le ponemos la posicion objetivo=infinito
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))

#Vamos a trabajar con una máquina de estados
state = 0
#0 estado avanzar hacia delante
#1 estado espera de obstaculos mientras avanza
#2 estado girar a la derecha
#3 estado girar a la izquierda
pared = False #booleana que indica cuando se encuentra la pared
message_displayed = False #booleana para mostrar un unico mensaje final
start_time = time.time() #inicio el cronometro

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1 and not target_reached: #El bucle acaba al alcanzar la meta
    # Obtengo la posicion gps del robot
    gps_vals = gps.getValues()
    # Obtener la orientación angular de la IMU
    orientation = imu.getRollPitchYaw()[2]  # Yaw representa la rotación alrededor del eje vertical
    
    # Obtener la imagen de la cámara
    image = camera.getImage()

    # Process sensor data here.
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    # Maquina de estados, modifica las actuaciones del robot
    if state == 0: #Orden avanzar
        # sigue hacia delante
        leftSpeed  = max_speed
        rightSpeed = max_speed
        print('Avanza!')
        state = 1
    elif state == 1: #Espero la deteccion de obstaculos
        if psValues[7]>80.0: #si detecto obstaculo en el sensor delantero izquierdo
            print('Gira a la derecha!')
            state = 2 # Cambio al estado 2, gira a la derecha
            pared = True #He encontrado la primera pared
        elif psValues[6]<80.0 and pared: #Siguiendo la pared me alejo de ella
            print('Gira a la izquierda!')
            state = 3 # Cmbio al estado 3 para girar a la izq y juntarme de nuevo
    elif state == 2: #Giro a la derecha      
        leftSpeed  = 0.2 * max_speed
        rightSpeed = -0.2 * max_speed #Le pasamos una velocidad negativa para provocar el giro
        if psValues[6]<200.0: # Cuando estemos lo suficientemente cerca de la pared dejo de girar
            state = 0 #para avanzar de nuevo
    elif state == 3: #Giro a la izquierda     
        leftSpeed  = -0.2 * max_speed
        rightSpeed = 0.2 * max_speed
        if psValues[6]>200.0: # Cuando estemos lo suficientemente cerca de la pared dejo de girar
            state = 0
    #Compruebo continuamente si he alcanzado la posicion deseada
    #Comparo la posicion gps del robot en X e Y con las de nuestra meta        
    if gps_vals[0] > x_goal and gps_vals[1] > y_goal: 
        target_reached = True #Si se cumple
        # Detener el giro
        leftSpeed = 0.0
        rightSpeed = 0.0
        # Mostrar el mensaje solo una vez junto con el valor del tiempo transcurrido
        if not message_displayed:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Objetivo alcanzado! Algoritmo Sigue paredes. Tiempo transcurrido: {elapsed_time:.2f} segundos.")
            message_displayed = True
                
    # Paso a los motores la velocidad definida en cada estado
    motor_left.setVelocity(leftSpeed)
    motor_right.setVelocity(rightSpeed)
    pass
exit()