import numpy as np
import datetime
from plot import *

chemin_src='C:/Users/Gwen/Desktop/Data/Bulgarie/ep-240126.log'
chemin_dest='C:/Users/Gwen/Desktop/Data/Bulgarie/donneesNettoyees2.txt'
#
#@brief fonction qui récupère les logs et le nettoie
#@param le chemin où sont les données
#@return le tableau des données néttoyées, la date de production des données
#
def recupDonnees(chemin_src):
    tab_donnees=[]
    compteur=0
    file = open(chemin_src, "r")
    # utiliser readlines pour lire toutes les lignes du fichier
    # La variable "lignes" est une liste contenant toutes les lignes du fichier
    line = file.readline()
    # Itérer sur les lignes
    toSplit1=line.split("]")
    toSplit2=toSplit1[0].split(" ")
    toSplit3=toSplit2[0].split("-")
    firstdate=datetime.datetime(int(toSplit3[0][1:]),int(toSplit3[1]),int(toSplit3[2]),8,0,1)
    tab_donnees.append((firstdate,'FIRST',0))
    while line:
        toSplit1=line.split("]")
        toSplit2=toSplit1[0].split(" ")
        toSplit3=toSplit2[0].split("-")
        toSplit4=toSplit2[1].split(":")
        if int(toSplit4[2])!="":
            sec=int(toSplit4[2])
        else:
             sec=0
        date=datetime.datetime(int(toSplit3[0][1:]),int(toSplit3[1]),int(toSplit3[2]),int(toSplit4[0])+2,int(toSplit4[1]),sec)
        value=toSplit1[1].strip()
        if value=="BATCH" :
            compteur+=50
        line = file.readline()
        tab_donnees.append((date,value,compteur))
    lastdate=datetime.datetime(int(toSplit3[0][1:]),int(toSplit3[1]),int(toSplit3[2]),17,0,1)
    if date < lastdate:
        tab_donnees.append((lastdate,'END',0))
    file.close()
    return tab_donnees,firstdate
#
#@brief fonction qui sauvegarde les données nettoyées dans un fichier au format txt
#@param le tableau de données nettoyées, le chemin de destination du ficher txt
#
def saveTxt(tab_donnees,chemin_dest):
    tab=np.array(tab_donnees)
    file = open(chemin_dest,'w+')
    for i in range(len(tab)):
        content = str(tab[i])
        file.write(content+"\n")
    file.close()

#
#@brief fonction qui calcule les durée horaires de fonctionnement 
#@param le tableau de données nettoyées, la date de pproduction des données
#@return le tableau des durées de fonctionnement
#  
def fonctionnement(tab_donnees,firstdate):
    tab_debut=[]
    tab_fin=[]
    deb=False
    fin=True
    for i in range(len(tab_donnees)):
        if (tab_donnees[i][1])=="SPEED +" and deb==False:
            debut=(tab_donnees[i][0])
            tab_debut.append(debut)
            deb=True
            fin=False
        if tab_donnees[i][1]=='STOP' and fin==False:
            fin=(tab_donnees[i][0])
            tab_fin.append(fin)
            deb=False
    tab_duree=[]
    for i in range(len(tab_debut)):
        if tab_debut[i] is None:
                continue
        elif i+1<len(tab_debut):
            if tab_debut[i].strftime('%H')!=tab_debut[i+1].strftime('%H'):
                dureetmp=tab_fin[i]-tab_debut[i]
                tab_duree.append((tab_debut[i].strftime('%H'),dureetmp))
            elif tab_debut[i].strftime('%H')==tab_debut[i+1].strftime('%H'):
                dureetmp=tab_fin[i]-tab_debut[i]
                dureetmp2=tab_fin[i+1]-tab_debut[i+1]
                duree=dureetmp+dureetmp2
                tab_debut[i+1]=None
                tab_duree.append((tab_debut[i].strftime('%H'),duree))
    return(tab_duree)
#
#@brief fonction qui produit un tableau pour taux de fonctionnement horaire 
#@param le tableau de durée de fonctionnement par heure
#@return le tableau avec % de fcnmt/heure
#  
def graphFcnmt(tab_duree):
	tabGrapheFnmt=[]
	for i in range(len(tab_duree)):
		td=datetime.timedelta(days=0, minutes=60)
		pourcentage=round((tab_duree[i][1]/td*100),1)
		tabGrapheFnmt.append((tab_duree[i][0],pourcentage))
	return tabGrapheFnmt

def graphSac(tab_donnees,firstdate):
    dateToCompare=firstdate
    minutes = datetime.timedelta(minutes=15)
    tabGraphSac=[]
    for elt in tab_donnees:
            heureTronquee = elt[0].strftime('%H:%M')
            #print(heureTronquee,dateToCompare)
            if heureTronquee==dateToCompare.strftime('%H:%M'):
                tabGraphSac.append((elt[0],heureTronquee,elt[2]))
                dateToCompare=dateToCompare+minutes
            elif heureTronquee>dateToCompare.strftime('%H:%M'):
                 dateToCompare=dateToCompare+minutes
    return tabGraphSac

def main(chemin):
    tab_donnees,firstdate=recupDonnees(chemin)
    saveTxt(tab_donnees,chemin_dest)
    tab_duree=fonctionnement(tab_donnees,firstdate)
    #print(tab_donnees)
    tabGrapheFnmt=graphFcnmt(tab_duree)
    #print(tabGrapheFnmt)
    #courbeFcnmt(tabGrapheFnmt)
    tabGraphSac=graphSac(tab_donnees,firstdate)
    print(tabGraphSac)
    #courbeSac(tabGraphSac)

main(chemin_src)

