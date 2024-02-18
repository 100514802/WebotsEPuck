# Resolver laberinto con robot E-Puck en Webots
## Alumno: Jose Enrique Muñoz Manero
### Nº: 100514802
### Asignatura: Simuladores de robots
En el presente proyecto se ha generado un mapa con obstaculos para ser resuelto por el robot E-Puck en Webots.
Se ha conseguido desarrollar la programación de tres controladores diferentes que son capaces de mover el robot desde el origen (esquina más cercana a origen) hasta tres posibles metas diferentes. 

Dentro de la carpeta *Controllers* se encuentra el fichero *Main_controller* que es el que se debe seleccionar en la configuración del robot. Dentro de este fichero, empleando **#** se puede comentar/descomentar las lineas pertinentes de modo que podemos elegir con que algoritmo queremos que el robot llegue hasta la meta. También se puede comentar/descomentar en cual de las tres posibles localizaciones queremos situar la meta.

Los tres posibles algoritmos a emplear son:
- Siguemuros: el robot avanza hasta que choca contra un muro, a partir de ese momento seguirá el muro en sentido horario hasta que alcanza la meta. Esto se puede hacer porque la meta siempre se encuentra pegada al muro exterior del mapa.
- Bug 0: el robot avanza siempre siguiendo la dirección de la meta hasta que se topa con un obstaculo. En ese momento rodea el obstaculo hasta que puede volver a colocarse en dirección a la meta y avanzando en dicha dirección.
- Bug 1: el robot avanza siempre siguiendo la dirección de la meta hasta que se topa con un obstaculo. En ese momento rodea el obstaculo por completo, almacenando que punto del contorno del obstaculo esta más cerca de la meta. En la segunda vuelta que describe alrededor del obstaculo comprueba que alcanza el punto de minima distancia y en ese momento se orienta hacia la meta y avanza en dicha dirección.

En el desarrollo de todos los algoritmos se ha definido una máquina de estados. De modo que en función del estado en el que se encontraba, el robot realizaba unas acciones u otras. De este modo se consigue un controlador no bloqueante que funcione de forma correcta.

Las funciones extras que se han implementado son:
1. Muestra de comentarios a través de terminal que indican que acción esta realizando el robot en cada momento. Además al alcanzar la meta se indicará el tiempo empleado.
2. Empleo de un temporizador que cronometra cuánto tarda el robot en llegar hasta la meta.
3. Desarrollo de tres algoritmo diferentes que permiten resolver el mapa, de acuerdo a lo aprendido en la asignatura de planificación.
4. Generación y resolución de un mapa con obstaculos no solo adyacentes al muro exterior, también formando islas.
5. Empleo del GPS e IMU para la resolución del problema.
6. Habilitación y empleo de la cámara, de modo que se puede tener la sensación de resolver el laberinto en primera persona.
7. Desarrollo de un fichero principal, *main_controller*, que lanza el controlador escogido e indica al robot a que punto de los posibles quiere ir.
