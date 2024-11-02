import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt



#"Control Difuso de Velocidad de Ventilador en Función de Temperatura y Humedad"#
# Definición de las variables difusas
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')
humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
velocidad = ctrl.Consequent(np.arange(0, 31, 1), 'velocidad')

# Funciones de membresía para temperatura
temperatura['baja'] = fuzz.trimf(temperatura.universe, [0, 0, 15])
temperatura['media'] = fuzz.trimf(temperatura.universe, [10, 20, 30])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [25, 40, 40])

# Funciones de membresía para humedad
humedad['baja'] = fuzz.trimf(humedad.universe, [0, 0, 50])
humedad['media'] = fuzz.trimf(humedad.universe, [30, 50, 70])
humedad['alta'] = fuzz.trimf(humedad.universe, [60, 100, 100])

# Funciones de membresía para velocidad
velocidad['lenta'] = fuzz.trimf(velocidad.universe, [0, 0, 15])
velocidad['moderada'] = fuzz.trimf(velocidad.universe, [10, 15, 20])
velocidad['rapida'] = fuzz.trimf(velocidad.universe, [15, 30, 30])

# Definición de las reglas difusas
rule1 = ctrl.Rule(temperatura['baja'] & humedad['baja'], velocidad['lenta'])
rule2 = ctrl.Rule(temperatura['baja'] & humedad['media'], velocidad['lenta'])
rule3 = ctrl.Rule(temperatura['baja'] & humedad['alta'], velocidad['moderada'])
rule4 = ctrl.Rule(temperatura['media'] & humedad['baja'], velocidad['lenta'])
rule5 = ctrl.Rule(temperatura['media'] & humedad['media'], velocidad['moderada'])
rule6 = ctrl.Rule(temperatura['media'] & humedad['alta'], velocidad['rapida'])
rule7 = ctrl.Rule(temperatura['alta'] & humedad['baja'], velocidad['moderada'])
rule8 = ctrl.Rule(temperatura['alta'] & humedad['media'], velocidad['rapida'])
rule9 = ctrl.Rule(temperatura['alta'] & humedad['alta'], velocidad['rapida'])

# Controlador difuso
controlador = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
simulador = ctrl.ControlSystemSimulation(controlador)

# Entrada de valores para simular
simulador.input['temperatura'] = 30  # Ejemplo de temperatura en grados Celsius
simulador.input['humedad'] = 65      # Ejemplo de humedad en porcentaje

# Ejecución de la simulación
simulador.compute()

# Resultado
print(f"Velocidad del ventilador: {simulador.output['velocidad']:.2f} unidades")

# Visualización de los resultados
temperatura.view(sim=simulador)
humedad.view(sim=simulador)
velocidad.view(sim=simulador)

# Mantiene las ventanas abiertas
plt.show()