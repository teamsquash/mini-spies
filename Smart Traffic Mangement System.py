#Smart Traffic Management System

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from numpy import arange
from skfuzzy.control import Antecedent
import time

traffic_density = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic_density')
pedestrian_density = ctrl.Antecedent(np.arange(0, 101, 1), 'pedestrian_density')
signal_duration = ctrl.Consequent(np.arange(0, 101, 1), 'signal_duration')

traffic_density['low'] = fuzz.trimf(traffic_density.universe, [0, 0, 30])
traffic_density['medium'] = fuzz.trimf(traffic_density.universe, [20, 50, 80])
traffic_density['high'] = fuzz.trimf(traffic_density.universe, [70, 100, 100])

pedestrian_density['low'] = fuzz.trimf(pedestrian_density.universe, [0, 0, 30])
pedestrian_density['medium'] = fuzz.trimf(pedestrian_density.universe, [20, 50, 80])
pedestrian_density['high'] = fuzz.trimf(pedestrian_density.universe, [70, 100, 100])

signal_duration['short'] = fuzz.trimf(signal_duration.universe, [0, 0, 30])
signal_duration['medium'] = fuzz.trimf(signal_duration.universe, [20, 50, 80])
signal_duration['long'] = fuzz.trimf(signal_duration.universe, [70, 100, 100])

rule1 = ctrl.Rule(traffic_density['low'] & pedestrian_density['low'], signal_duration['short'])
rule2 = ctrl.Rule(traffic_density['medium'] | pedestrian_density['medium'], signal_duration['medium'])
rule3 = ctrl.Rule(traffic_density['high'] | pedestrian_density['high'], signal_duration['long'])

signal_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

while True:
    traffic_sim_value = int(input("Enter traffic density (0-100): "))
    pedestrian_sim_value = int(input("Enter pedestrian density (0-100): "))

    signal_sim = ctrl.ControlSystemSimulation(signal_ctrl)
    signal_sim.input['traffic_density'] = traffic_sim_value
    signal_sim.input['pedestrian_density'] = pedestrian_sim_value
    signal_sim.compute()

    print("Input values: Traffic density = {}, Pedestrian density = {}".format(traffic_sim_value, pedestrian_sim_value))
    print("Output value: Signal duration = {}".format(signal_sim.output['signal_duration']))

    exit_choice = input("Press q to quit or any other key to continue: ")
    if exit_choice == 'q':
      break
