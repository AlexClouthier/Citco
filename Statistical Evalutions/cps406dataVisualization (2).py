# -*- coding: utf-8 -*-
"""
Created on Wed Apr  9 01:17:15 2025

@author: Alex
"""

import matplotlib.pyplot as plt
import warnings
import numpy as np
import pandas as pd
from scipy.stats import linregress
warnings.simplefilter('ignore')
#data, will be changed to lists of data gotten from websites

def processFiles(citations_path, grant_money_path):
    citations = pd.read_csv(citations_path, encoding='ISO-8859-1')
    pd.to_numeric(citations['Citations'])
    grants = pd.read_csv(grant_money_path, encoding='ISO-8859-1', skiprows=3)
    grants['Amount($)']=pd.to_numeric(grants['Amount($)'].replace({',':''}, regex=True))
    
    for index in range(len(grants['Fiscal Year'])):
        grants['Fiscal Year'][index]=grants['Fiscal Year'][index][:4]
        
    grants['Fiscal Year']=pd.to_numeric(grants['Fiscal Year'])

    return citations, grants

def plotMoneyData(citations, grants):
    """
    Plots a scatter plot showing the correlation between
    citation count and grant money received.
    """
    #get data, make citations same length, remove grants data not found in citations
    nCitations = grants[['Name']].merge(citations[['Name', 'Citations']], on='Name', how='left')
    nCitations = nCitations.dropna()
    nGrants = grants[grants['Name'].isin(nCitations['Name'])]

        
    #create plot
    plt.figure(figsize=(8, 6))
    plt.scatter(nCitations['Citations'], nGrants['Amount($)'], color='blue', alpha=0.7)
    correlation = nGrants['Amount($)'].corr(nCitations['Citations'])
    print(f"Correlation: {correlation:.3f}")
    
    # labels
    plt.title('Correlation Between Citation Count and Grant Money Received')
    plt.xlabel('Number of times cited')
    plt.ylabel('Grant Money Received ($)')
    plt.grid(True)
    plt.ticklabel_format(style = 'plain', axis = 'y')
    
    #trendline
    z = np.polyfit(nCitations['Citations'], nGrants['Amount($)'], 1)
    p = np.poly1d(z)
    #plt.plot((nCitations['Citations']), p(nCitations['Citations']), "r--")
    
    plt.show()

def plotYearData(citations, grants):
    """
    Plots a scatter plot showing the correlation between
    year and citation count.
    """
    #get data, make citations same length, remove grants data not found in citations
  #  nCitations = grants[['Name']].merge(citations[['Name', 'Citations']], on='Name', how='left')
  #  nCitations = nCitations.dropna()
  #  nGrants = grants[grants['Name'].isin(nCitations['Name'])]
    
    nCitations = citations[['Name', 'Citations']].merge(grants[['Name', 'Fiscal Year']], on='Name', how='left')
   
    #create plot
    plt.figure(figsize=(8, 6))
    #plt.scatter(nGrants['Fiscal Year'], nCitations['Citations'],  color='blue', alpha=0.7)
    plt.hist(nCitations['Fiscal Year'])
    
    # labels
    plt.title('Correlation Between Citation Count and Grant Money Received')
    plt.ylabel('Number of times cited')
    plt.xlabel('Year')
    plt.grid(True)
    plt.ticklabel_format(style = 'plain', axis = 'y')
    
    #trendline
    #z = np.polyfit(nCitations['Citations'], nGrants['Amount($)'], 1)
    #p = np.poly1d(z)
    #plt.plot((nCitations['Citations']), p(nCitations['Citations']), "r--")
    
    plt.show()
    
citations, grants = processFiles('citationCount.csv', 'NSERC_Results_cs.csv')
plotMoneyData(citations, grants)
plotYearData(citations, grants)

def get_individual_data(citations, grants, name):
    """
    Print the data for a specific individual by name.
    """
    
    person = citations[citations['Name'].str.lower() == name.lower()]
    if person.empty:
        print(f"No data found for '{name}'.")
    else:
        nPerson = person[['Name', 'Citations']].merge(grants[['Name', 'Amount($)', 'Fiscal Year']], on='Name', how='left')
        print(nPerson.to_string(index=False))

def contains_name(input, citations):
    possible_names=[]
    for name in citations['Name']:
        if name.__contains__(input):
            possible_names.append(name)
            
    return possible_names

def get_correlation_vals(citations, grants):
    """
    using linregress from scipy.stats to find a p value and std dev 
    """
    nCitations = grants[['Name']].merge(citations[['Name', 'Citations']], on='Name', how='left')
    nCitations = nCitations.dropna()
    nGrants = grants[grants['Name'].isin(nCitations['Name'])]
    
    return linregress(nCitations['Citations'], nGrants['Amount($)'])
    
slope, intercept, r_value, p_value, std_err = get_correlation_vals(citations, grants)
print(f"R-squared: {r_value**2:.3f}")
print(f"P-value: {p_value:.5f}")
   
get_individual_data(citations, grants, 'Hinton, Geoffrey')
#print(contains_name("Geoff", citations))

    