# -*- coding: utf-8 -*-
"""
Based on Markowitz, I calculate portofolio of different assets
Created on Tue Apr 26 20:25:23 2016

@author: Pedro
"""

import numpy as np
import matplotlib.pyplot as plt

from auxiliary_functions import output_reader

class asset():
    def __init__(self, equity, standard_deviation, asset_name, source):
        self.r = equity
        self.sigma = standard_deviation
        self.name = asset_name
        self.source = source

class portofolio():
    def __init__(self, data):
        self.r = data['equity']
        self.sigma = data['standard deviation']
        self.name = data['name']
        self.source = data['source']
        self.n = len(data['equity'])
    
    def calculate_for_two(self, asset1_name, asset2_name, x1):
        """"Calculate the equity and standard deviation for any two 
            assets with fractions x1 (number of asset1/total assets)."""
        
        index1 = self.name.index(asset1_name)
        index2 = self.name.index(asset2_name)
        
        r_combined = x1*self.r[index1] + (1-x1)*self.r[index2]
        sigma_combined = x1**2*self.sigma[index1]**2 + \
                         (1-x1)*2*self.sigma[index2]**2
        return r_combined, sigma_combined
    
    def calculate_covariance(self, asset1_name, asset2_name):
        filename1 = 'history_' + asset1_name + '.csv'
        filename2 = 'history_' + asset2_name + '.csv'
        
        data1 = output_reader(filename1, separator = ',', type_data = ['time',
                         'float', 'float', 'float', 'float', 'float', 'float'])
        data2 = output_reader(filename2, separator = ',', type_data = ['time',
                         'float', 'float', 'float', 'float', 'float', 'float'])
        
        #Both datas must have the same length
        if len(data1['Close']) < len(data2['Close']):
            n = len(data1['Close']) 
        else:
            n = len(data2['Close']) 
        matrix = np.vstack([data1['Close'][:n], data2['Close'][:n]])
        
        #Cov(a,b) functions returns matrix:
        #cov(a,a)  cov(a,b)
        #cov(a,b)  cov(b,b)
        covariants = np.cov(matrix)
        
        return covariants[0][1]

    def plot_for_two(self, asset1_name, asset2_name):
        """Plot portofolio of two assets"""
        r_list = []
        sigma_list = []
        
        x1_list = np.linspace(0,1)
        
        for x1 in x1_list:
            r, sigma = self.calculate_for_two(asset1_name, asset2_name, x1)
            r_list.append(r)
            sigma_list.append(sigma)
            
        plt.plot(sigma_list, r_list)
        plt.xlabel("standard deviation ($\sigma$)")
        plt.ylabel("equity (percent)")
        
# Annual return for 3 years
d = {'equity': [0.0098, 0.0146, 0.002],
     'standard deviation': [0.113, 0.1372, 0.0363],
     'name': ['SPY', 'QQQ', 
              'BOND'],
     'source': ['https://finance.yahoo.com/q/rk?s=SPY',
                'https://finance.yahoo.com/q/rk?s=QQQ+Risk',
                'https://finance.yahoo.com/q/rk?s=BOND+Risk']} 

p = portofolio(d)
#p.plot_for_two('SPY', 'BOND')
p.calculate_covariance('SPY', 'BOND')