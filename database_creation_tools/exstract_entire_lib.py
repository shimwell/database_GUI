#!/usr/bin/env python3

"""exstract_entire_lib.py: Exstracts xs vs energy data from h5 based library"""

__author__      = "Jonathan Shimwell"

import openmc
from plotly.offline import download_plotlyjs, plot
from plotly.graph_objs import Scatter, Layout
import matplotlib.pyplot as plt
import openmc.data
from tqdm import tqdm
import os
import numpy as np

datapath = "/home/jshim/openmc_fork/fendl-3.1d-hdf5/"
library = 'fendl 3.1'

list_of_xs = []

for file in os.listdir(datapath)[:2]:
    if file.endswith(".h5"):
        
        isotope_object = openmc.data.IncidentNeutron.from_hdf5(os.path.join(datapath, file))
        
        reactions = isotope_object.reactions

        temperatures = isotope_object.energy.keys()


        for reaction in reactions:
            temperatures = isotope_object[reaction].xs.keys()
            for temperature in temperatures:
                energy = isotope_object.energy[temperature]
                cross_section = isotope_object[reaction].xs[temperature](energy)

                shorter_cross_section = np.trim_zeros(cross_section, 'f')
                
                ofset = len(cross_section) - len(shorter_cross_section)
                
                shorter_energy= energy[ofset:]
                print(len(shorter_cross_section),len(cross_section))
                print(len(shorter_energy),len(energy))
                print()
                list_of_xs.append({
                    'atomic number':isotope_object._atomic_number,
                    'mass number':isotope_object._mass_number,
                    'neutron number':isotope_object._mass_number-isotope_object._atomic_number,
                    'name':isotope_object.name,
                    'atomic symbol':isotope_object.atomic_symbol,
                    'temperature':temperature,
                    'reaction':reaction,
                    'library':library
                    'cross section':shorter_cross_section,
                    'energy':shorter_energy,
                })

# print(list_of_xs)

        #new_xs = {'temperature'}
#             energy = isotope_object.energy['293K'] # 294K is the temperature for tendl this is 293K
#             cross_section = isotope_object[MT_number].xs['293K'](energy)
