import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definición de las variables difusas
rendimiento_local = ctrl.Antecedent(np.arange(0, 11, 1), 'rendimiento_local')  # 0 a 10
rendimiento_visitante = ctrl.Antecedent(np.arange(0, 11, 1), 'rendimiento_visitante')  # 0 a 10
resultado = ctrl.Consequent(np.arange(0, 101, 1), 'resultado')  # Probabilidad 0% a 100%

# Funciones de membresía para rendimiento del Barcelona
rendimiento_local['bajo'] = fuzz.trimf(rendimiento_local.universe, [0, 0, 5])
rendimiento_local['medio'] = fuzz.trimf(rendimiento_local.universe, [4, 5, 6])
rendimiento_local['alto'] = fuzz.trimf(rendimiento_local.universe, [5, 10, 10])

# Funciones de membresía para rendimiento del Real Madrid
rendimiento_visitante['bajo'] = fuzz.trimf(rendimiento_visitante.universe, [0, 0, 5])
rendimiento_visitante['medio'] = fuzz.trimf(rendimiento_visitante.universe, [4, 5, 6])
rendimiento_visitante['alto'] = fuzz.trimf(rendimiento_visitante.universe, [5, 10, 10])

# Funciones de membresía para resultado
resultado['derrota'] = fuzz.trimf(resultado.universe, [0, 0, 50])
resultado['empate'] = fuzz.trimf(resultado.universe, [20, 50, 80])
resultado['victoria'] = fuzz.trimf(resultado.universe, [50, 100, 100])

# Definición de las reglas difusas
rule1 = ctrl.Rule(rendimiento_local['alto'] & rendimiento_visitante['bajo'], resultado['victoria'])
rule2 = ctrl.Rule(rendimiento_local['alto'] & rendimiento_visitante['medio'], resultado['victoria'])
rule3 = ctrl.Rule(rendimiento_local['alto'] & rendimiento_visitante['alto'], resultado['empate'])
rule4 = ctrl.Rule(rendimiento_local['medio'] & rendimiento_visitante['bajo'], resultado['victoria'])
rule5 = ctrl.Rule(rendimiento_local['medio'] & rendimiento_visitante['medio'], resultado['empate'])
rule6 = ctrl.Rule(rendimiento_local['medio'] & rendimiento_visitante['alto'], resultado['derrota'])
rule7 = ctrl.Rule(rendimiento_local['bajo'] & rendimiento_visitante['bajo'], resultado['empate'])
rule8 = ctrl.Rule(rendimiento_local['bajo'] & rendimiento_visitante['medio'], resultado['derrota'])
rule9 = ctrl.Rule(rendimiento_local['bajo'] & rendimiento_visitante['alto'], resultado['derrota'])

# Controlador difuso
controlador = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
simulador = ctrl.ControlSystemSimulation(controlador)

# Entrada de valores para simular, aqui es realista jeje
simulador.input['rendimiento_local'] = 9  # Rendimiento del Barcelona
simulador.input['rendimiento_visitante'] = 5  # Rendimiento del Real Madrid

# Ejecución de la simulación
simulador.compute()

# Resultado
print(f"Probabilidad de victoria del Barcelona: {simulador.output['resultado']:.2f}%")

# Visualización de los resultados
rendimiento_local.view(sim=simulador)
rendimiento_visitante.view(sim=simulador)
resultado.view(sim=simulador)

# Mantiene las ventanas abiertas
plt.show()
