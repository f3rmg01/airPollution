import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
# def regresion(v,arboles):
#     suma=0
#     for arbol in arboles:
#         suma+=arbol*(98.5728 + 5.0656*np.sqrt(v[0])  - 1.3855*np.power(v[2], 2) - 61.7951*np.power(v[1] / 100, 0.5) - 12.5009*np.sqrt(v[3]))
#     return suma

def regresion(v,arboles):
    suma=0
    dis = [[0.00000234,0.000001, 0.000002],[0.00002154,0.000002, 0.0000034],[0.00001034,0.00000921, 0.0000005],[0.0000034,0.000013,0.0000009]]
    aum = [0.000004,0.0000092,0.00000091, 0.000000249]
    indice=0
    for arbol in arboles:
        suma+=74.6139 + arbol*(dis[indice][0]*2.3755*np.sqrt(v[0])  - dis[indice][1]*2.1288*np.power(v[2], 2) - dis[indice][2]*67.8621*np.power(v[1] / 100, 0.5))
        indice+=1
    for i in range(len(arboles)):
        suma+= arboles[i]*aum[i]
    return suma




def regresionVerificacion(o3, wsp, rh):
    pm10=0; res = []
    for i in range(365):
        pm10=74.6139 + 2.3755*np.sqrt(o3[i])  - 2.1288*np.power(wsp[i], 2) - 67.8621*np.power(rh[i] / 100, 0.5)
        res.append(pm10)
    return res

#########################################################################
#print('Prueba t Student')
#pm10Prom = pd.read_csv('/home/fer/Documents/NEO/neo/presentacion/regresion/AJM-PM10-pro.csv') 
#dias = [i for i in range(1, 366)]
#plt.plot(dias, pm10Prom['pm10'], label='Original')
# for i in range(16):
#base = pd.read_csv('/home/fer/Documents/NEO/neo/presentacion/final/promedios/1.csv')
#o3 = base['O3']
#wsp = base['WSP']
#rh = base['RH']
#reg = regresionVerificacion(o3, wsp, rh)
#t, pvalue = ttest_ind(reg, pm10Prom['pm10'])
#if pvalue >= 0.05:
#    print('Soy la estacion de AJM')
#    print('pvalue = ',pvalue)
#plt.title('Concentración de PM10 de la estación AJM')
#plt.plot(dias, reg, label='Regresion')
#plt.xlabel('Dias')
#plt.ylabel('Concentracion $\mu g/m^3$')
#plt.legend()
#plt.show()
#######################################################################
# 



# humedad = pd.read_csv('../archivosRegresion/promedios/1.csv')
# # tem = pd.read_csv('../archivosRegresion/AJM-TMP.csv')
# # wsp = pd.read_csv('../archivosRegresion/AJM-WSP.csv')
# pm10 = pd.read_csv('AJM-PM10-pro.csv')

# h, pvalue = spearmanr(humedad['RH'], pm10['pm10'])
# print(spearmanr(humedad['RH'], pm10['pm10']))
# t, pvalue = spearmanr(humedad['TMP'], pm10['pm10'])
# print('tem ', pvalue)
# w, pvalue = spearmanr(humedad['WSP'], pm10['pm10'])
# print('wsp ', pvalue)
# d={}
# v=[]
# for i in range(len(pm10['2016'])):
#     suma=0
#     for j in pm10.keys():
#         suma+=pm10[j][i]
#     v.append(suma/4)
# d['pm10'] = v
# c=1
# suma=0
# pro=[]
# f={}
# co=1
# for i in d['pm10']:
#     suma+=i
#     c+=1
#     if c==24:
#         pro.append(round(suma/24,2))
#         c=1; suma=0
# f['pm10'] = pro
# df = pd.DataFrame(f)
# df.to_csv('AJM-PM10-pro.csv', index= False)

# import statsmodels.api as sm

# import statsmodels.formula.api as smf
# ajm = pd.read_csv('../archivosRegresion/promedios/1.csv')
# pm10b = pd.read_csv('AJM-PM10-pro.csv')
# pm10=pm10b['pm10']
# rh = ajm['RH']
# o3 = ajm['O3']
# tmp = ajm['TMP']
# wsp = ajm['WSP']

# ols = smf.ols('pm10~ np.power(1/np.log(o3),4) + np.power(wsp,2)+np.power(rh/100,0.001) +np.log(tmp)', data={'pm10':pm10, 'o3':o3, 'wsp':wsp, 'rh': rh, 'tmp':tmp}).fit()
# print(ols.summary())


