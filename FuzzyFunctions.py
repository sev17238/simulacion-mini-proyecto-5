###################################################
# Guatemala, noviembre del 2020
###################################################
# Modelacion y simulacion
# Diego Sevilla 17238
# Alejandro Tejada 17584
###################################################

# Refs:
# https://gist.github.com/ryangmolina/e1c87509b6919ac8aaf3eceb315d3e5e
# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html
# https://vpetro.io/fuzzylogic/fuzzy_mehaan_joy.html

import numpy as np
import random
import math


import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
quality = ctrl.Antecedent(np.arange(0, 11, 1), 'quality')
service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

# Auto-membership function population is possible with .automf(3, 5, or 7)
quality.automf(3)
service.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])