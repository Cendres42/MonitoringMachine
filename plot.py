import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

def courbeFcnmt(tabGrapheFnmt):
	tabGraph2=pd.DataFrame(tabGrapheFnmt,columns=['Heure','Fcnmt'])
	plt.bar(height=tabGraph2['Fcnmt'],x=tabGraph2['Heure'])
	plt.xlabel('Heures')
	plt.ylabel('Pourcentage de fonctionnement')
	plt.title('Fonctionnement de la machine sur la journée')
	"""def add_value_label(x_list, y_list):
		for i in range(1, len(x_list) + 1):
			plt.text(i, y_list[i - 1], y_list[i - 1], ha="center")
	add_value_label(class_number, no_of_students)
	"""
	plt.show()


# this vizualisation is a lineplot from one data column
def courbeSac(tabGraphSac):
    dataGraph=pd.DataFrame(tabGraphSac,columns=["Date","Heure","NombreDeSacs"])
    #print(dataGraph.head())
    plt.figure()
    sns.lineplot(data=dataGraph,x='Heure',y='NombreDeSacs',color="Blue")
    #plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0, 30]))
    plt.title('Evolution de la  production de sac le ' + str(dataGraph['Date'][1].strftime('%d-%m-%Y')),loc='center',pad=3,fontsize=15,color="Darkred",fontweight='bold')
    plt.xlabel("Heure")
    plt.ylabel("Nombre de sacs")
    plt.xticks(rotation=90)
    plt.gcf().subplots_adjust(left = 0.125, bottom = 0.214, right = 0.9, top = 0.9, wspace = 0.2, hspace = 0.2)
    plt.savefig("C:/Users/Gwen/Desktop/Data/Bulgarie/evol_NB_Sacs.png", dpi=300, format="png")
    plt.show()





    