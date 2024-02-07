import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def courbeFcnmt(tabGrapheFnmt,firstdate):
    tabGraph2=pd.DataFrame(tabGrapheFnmt,columns=['Heure','Fcnmt'])
    pos=list(range(len(tabGraph2['Heure'])))
    width=0.5
    plt.figure(figsize=[8,6])
    plt.subplot(111)
    plt.bar([p + width for p in pos], tabGraph2['Fcnmt'],width)
    plt.xlabel('Hours')
    plt.ylabel('Operating percentage')
    plt.xticks(pos,tabGraph2['Heure'])
    plt.ylim([0, 100])
    plt.title('Operation of the machine on the day : '+str(firstdate.strftime('%d-%m-%Y')))
    plt.savefig("C:/Users/Gwen/Desktop/Data/Bulgarie/fnmtMachine"+str(firstdate.strftime('%d-%m-%Y'))+".png", dpi=300, format="png")
    plt.show()
    plt.close()


# this vizualisation is a lineplot from one data column
def courbeSac(tabGraphSac):
    dataGraph=pd.DataFrame(tabGraphSac,columns=["Date","Heure","NombreDeSacs"])
    #print(dataGraph.head())
    plt.figure()
    sns.lineplot(data=dataGraph,x='Heure',y='NombreDeSacs',color="Blue")
    #plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(byminute=[0, 30]))
    plt.title('Evolution of bag production on ' + str(dataGraph['Date'][1].strftime('%d-%m-%Y')),loc='center',pad=3,fontsize=15,color="Darkred",fontweight='bold')
    plt.xlabel("Hours")
    plt.ylabel("Number of bags")
    plt.grid(which='major', axis='x', color='lightgrey', linestyle='dashed')
    plt.grid(which='major', axis='y', color='lightgrey', linestyle='dashed')
    plt.xticks(rotation=90)
    plt.gcf().subplots_adjust(left = 0.125, bottom = 0.214, right = 0.9, top = 0.9, wspace = 0.2, hspace = 0.2)
    plt.savefig("C:/Users/Gwen/Desktop/Data/Bulgarie/evol_NB_Sacs"+ str(dataGraph['Date'][1].strftime('%d-%m-%Y'))+".png", dpi=300, format="png")
    plt.show()


def courbeFcnmtLabels(tabGrapheFnmt,firstdate):
    tabGraph2=pd.DataFrame(tabGrapheFnmt,columns=['Heure','Fcnmt'])
    pos=list(range(len(tabGraph2['Heure'])))
    tabGraph2['Fcnmt']
    width=0.5
    plt.figure(figsize=[8,6])
    plt.subplot(111)
    plt.bar(height=tabGraph2['Fcnmt'],x=pos)
    plt.xlabel('Hours')
    plt.ylabel('Operating percentage')
    labels_X=('8h-9h', '9h-10h', '10h-11h', '11h-12h', '12h-13h','13h-14h','14h-15h','15h-16h','16h-17h')
    plt.xticks(pos,labels_X)
    plt.title('Operation of the machine on the day : '+str(firstdate.strftime('%d-%m-%Y')))
    plt.savefig("C:/Users/Gwen/Desktop/Data/Bulgarie/fnmtMachine"+str(firstdate.strftime('%d-%m-%Y'))+".png", dpi=300, format="png")
    plt.show()
    plt.close()




    