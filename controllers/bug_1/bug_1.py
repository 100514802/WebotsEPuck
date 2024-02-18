"""bug_1 controller."""
# Importamos del modulo del controlador las clases necesarias
# (se corresponden a los elementos con los que vamos a trabajar)
from controller import Robot
from math import atan2
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
# Muestro por terminal las coordenadas de dicho punto
print(f'La meta se encuentra en las coordenadas: {x_goal}, {y_goal}')

# create the Robot instance.
robot = Robot()

# Obtener la instancia de la cámara
camera = robot.getDevice("camera")  
# Establecer la frecuencia de muestreo de la cámara
camera.enable(10) 

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Establecer la posición objetivo
target_position = [x_goal, y_goal, 0]

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
imu = robot.getDevice("inertial unit")
gps = robot.getDevice('gps')

gps.enable(timestep)
imu.enable(timestep)

# Leo la posicion inicial del robot
robot_pos = gps.getValues()
target_reached = False #booleana para indicar que hemos alcanzado el objetivo

motor_left.setVelocity(0.0) #inicio el motor de la rueda izq con velocidad 0
motor_right.setVelocity(0.0) #inicio el motor de la rueda dcha con velocidad 0
# Para que los motores giren continuamente le ponemos la posicion objetivo=infinito
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))

#Vamos a trabajar con una máquina de estados
state = 0
#0 estado iniciar avance hacia el objetivo
#1 estado de espera mientras rodeo el obstaculo
#2 estado para girar a la derecha
#3 estado para girar a la izquierda
#4 estado para avanzar recto (sigue pared del obstaculo)

obstaculo = False #Booleana que indica que estoy rodeando un obstaculo
message_displayed = False #booleana para mostrar un unico mensaje final
start_time = time.time() #inicio el cronometro
print('Inicio buscando la direccion adecuada')
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1 and not target_reached: #El bucle acaba al alcanzar la meta
    # Obtener la posición y orientación actuales del robot
    robot_pos = gps.getValues()
    # Obtener la orientación angular de la IMU
    robot_orientation = imu.getRollPitchYaw()
    
    # Obtener la imagen de la cámara
    image = camera.getImage()
    
    # Calcular la distancia hasta el objetivo
    distance_to_target = ((target_position[0] - robot_pos[0])**2 + (target_position[1] - robot_pos[1])**2)**0.5
    
    # Calcular el ángulo hacia el objetivo
    angle_to_target = -robot_orientation[2] + atan2(target_position[1] - robot_pos[1], target_position[0] - robot_pos[0])

    # Process sensor data here.
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
    # Maquina de estados, modifica las actuaciones del robot
    if state == 0: #Avanza hacia el objetivo
        # Controlar la velocidad de las ruedas para avanzar hacia el objetivo
        leftSpeed=(max_speed*0.5 - angle_to_target)
        rightSpeed=(max_speed*0.5 + angle_to_target)
        obstaculo = False #Reset de la booleana obstaculo
        compruebo_repeticion = False #Booleana para comprobar si el robot ha completado una vuelta al obstaculo
        obstaculo_rodeado = False #Booleana indica obstaculo rodeado por completo
        min_dist = float('inf') #Variable para guardar la minima distancia entre el robot y la meta
        init_pos = [0.0, 0.0] #Almacena el punto donde se comienza a rodear el obstaculo
        min_pos = [0.0, 0.0] #Almacena el punto alrededor del obstaculo más cercano a la meta
        if psValues[0]>80.0 or psValues[7]>80: #Si los sensores detectan un obstaculo
            print('Rodear obstaculo!')
            init_pos=[robot_pos[0],robot_pos[1]] #Guardo la posicion de contacto inicial con el obstaculo
            state = 1
    elif state == 1: #Estado de espera mientras se rodea el obstaculo
        if psValues[7]>80.0 or psValues[0]>80.0: #Si el obstaculo esta delante
            print('Gira a la izq!')
            state = 3 # Ordeno girar a la izquierda
            obstaculo = True # Seteo la booleana para indicar que estoy rodeando el obs
        elif psValues[1]<80.0 and obstaculo: #Si estoy rodeando el obs y me alejo, giro a la dcha
            print('Gira a la dcha!')
            compruebo_repeticion = True #A partir de este momento compruebo si vuelvo a pasar por la posicion incial
            state = 2         
    elif state == 2: #Estado para girar a la derecha     
        leftSpeed  = 0.2 * max_speed
        rightSpeed = -0.2 * max_speed
        if psValues[1]>100.0: #Cuando detecto pared a la dcha del robot, continua recto
            print('Avanza!')
            state = 4
    elif state == 3: #Estado para girar a la izquierda       
        leftSpeed  = -0.2 * max_speed
        rightSpeed = 0.2 * max_speed
        if psValues[1]<200.0: #Cuando detecto pared una distancia adecuada, continua recto
            print('Avanza!')
            state = 4
    elif state == 4: #Avanza recto, siguiendo el contorno del obstaculo
        # sigue hacia delante
        leftSpeed  = 0.5 * max_speed
        rightSpeed = 0.5 * max_speed
        print('Avanza!')
        state = 1
    
    #Compruebo si ya he rodeado el obstaculo
    if (((init_pos[0] - robot_pos[0])**2 + (init_pos[1] - robot_pos[1])**2)**0.5)<0.04 and compruebo_repeticion:
        obstaculo_rodeado = True
    #Si he rodeado el obstaculo, cuando vuelva a pasar por el punto
    #mas cercano a la meta, oriento hacia la meta y avanzo (estado 0)
    if (((min_pos[0] - robot_pos[0])**2 + (min_pos[1] - robot_pos[1])**2)**0.5)<0.04 and obstaculo_rodeado:       
        state = 0
    #Actualizo el punto de minima distancia a la meta
    if distance_to_target < min_dist and obstaculo:
        min_dist = distance_to_target
        min_pos = [robot_pos[0],robot_pos[1]]
           
    # Verificar si el robot ha llegado al objetivo
    if robot_pos[0] > x_goal and robot_pos[1] > y_goal:
        target_reached = True #Seteo la booleana que me indica que he alcanzado la meta
        # Detener el giro
        leftSpeed = 0.0
        rightSpeed = 0.0
        # Mostrar el mensaje solo una vez
        if not message_displayed:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Objetivo alcanzado! Algoritmo Bug 1. Tiempo transcurrido: {elapsed_time:.2f} segundos.")
            message_displayed = True    
    # Escribo la velocidad establecida en los estados, en los motores correspondientes
    motor_left.setVelocity(leftSpeed)
    motor_right.setVelocity(rightSpeed)
    pass    
exit()