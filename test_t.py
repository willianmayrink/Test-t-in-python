import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

import re
import pandas as pd
import numpy as np
def get_list_of_university_towns():
    '''Returna a DataFrame cidade e estado em university_towns.txt. 
    Exemplo:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    ref_arquivo = open("university_towns.txt","r")
    dados= ref_arquivo.readlines()
    df=[]
    x=[]
    i=0
    while(i<len(dados) and i!=len(dados) ):
        if('[edit]' in dados[i]):
            x=dados[i].split('[')
            estado=x[0]
            i=i+1
            while( (len(dados)!=i) and  not('[edit]' in dados[i])):
                y=dados[i].split('(')
                df.append([estado, y[0].rstrip(' ')])
                i=i+1
    df= pd.DataFrame(df)
    df=df.rename(columns={0:'State',1:'RegionName'})
    
    return df



import pandas as pd
def get_recession_start():
   	 #Retorna o ano e o trimestre da recessão, no formato: 2005q3
    df= pd.read_excel('gdplev.xls', usecols=[4, 5], skiprows=219)
    df= df.rename(columns={'1999q4':'Quarter', 9926.1:'GDP $'})
    for i in range(0,len(df)-3,1):
        if(df.loc[i,'GDP $']>df.loc[i+1,'GDP $']<df.loc[i+2,'GDP $']<df.loc[i+3,'GDP $']):
            x=df.loc[i, 'Quarter']
    return x



def get_recession_end():
	#retorna o fim da recessão trimestre e ano:2005q3
    df= pd.read_excel('gdplev.xls', usecols=[4, 5], skiprows=219)
    df= df.rename(columns={'1999q4':'Quarter', 9926.1:'GDP $'})
    for i in range(0,len(df)-3,1):
        if(df.loc[i,'GDP $']>df.loc[i+1,'GDP $']<df.loc[i+2,'GDP $']<df.loc[i+3,'GDP $']):
            x=df.loc[i+3, 'Quarter']
    return x


def get_recession_bottom():
    df= pd.read_excel('gdplev.xls', usecols=[4, 5], skiprows=219)
    df= df.rename(columns={'1999q4':'Quarter', 9926.1:'GDP $'})
    for i in range(0,len(df)-3,1):
        if(df.loc[i,'GDP $']>df.loc[i+1,'GDP $']<df.loc[i+2,'GDP $']<df.loc[i+3,'GDP $']):
            x=df.loc[i+1, 'Quarter']
    return x





def convert_housing_data_to_quarters():
  	#Fazendo a media dos valores de casas para cada trimestre e alterando no dataframe.
    hd= pd.read_csv('City_Zhvi_AllHomes.csv')
    hd=hd.set_index('State')
    hd= hd.rename(index=(states))
    hd= hd.reset_index()
    x= hd.loc[:,'2000-01':'2016-08']
    m=x.T
    m.index = pd.to_datetime(m.index)
    m=m.resample('3M').mean()
    m=m.drop(m.index[-1])
    m=m.reset_index()
    new=[]
    for i in range(0,len(m)):
        if(m.loc[i, ('index')].quarter == 1):
            new.append(str(m.loc[i, ('index')].year)+'q'+str(m.loc[i, ('index')].quarter))
        elif(m.loc[i, ('index')].quarter == 2):
            new.append(str(m.loc[i, ('index')].year)+'q'+str(m.loc[i, ('index')].quarter))
        elif(m.loc[i, ('index')].quarter == 3):
            new.append(str(m.loc[i, ('index')].year)+'q'+str(m.loc[i, ('index')].quarter))
        elif(m.loc[i, ('index')].quarter == 4):
            new.append(str(m.loc[i, ('index')].year)+'q'+str(m.loc[i, ('index')].quarter))
    m['Quarter']=new
    m=m.set_index('Quarter')
    m=m.T
    m=m.drop(m.index[0])
    y=hd.loc[:,'State']
    z=hd.loc[:,'RegionName']
    m['State']=y
    m['RegionName']=z
    m=m.set_index(["State","RegionName"])
    m=m.reset_index()
    return m

def run_ttest():
    
    univ=pd.merge(get_list_of_university_towns(), convert_housing_data_to_quarters(), how='inner',left_on=['State','RegionName'], right_on=['State','RegionName'] )
    x=get_recession_start()

    if(x[5]=='1'):
        y=int(x[0:4])-1
        y=str(y)+'q4'
    else:
        y=int(x[5])-1
        y=x[0:5]+str(y)
    univ['Ratio Price']=univ[y]/univ[get_recession_bottom()]
    houses=convert_housing_data_to_quarters()
    houses=houses.loc[~houses.index.isin(houses.merge(get_list_of_university_towns().assign(a='key'),how='left').dropna().index)]
    houses['Ratio Price']=houses[y]/houses[get_recession_bottom()]
    
    pvalue=ttest_ind(houses['Ratio Price'].dropna(),univ['Ratio Price'].dropna())
    if(houses['Ratio Price'].dropna().mean()>univ['Ratio Price'].dropna().mean()):
        better='university town'
    else:
        better='non-university town'
    if(pvalue[1]<0.01):
        different=True
    else:
        different=False
    return  different, better, pvalue[1]


