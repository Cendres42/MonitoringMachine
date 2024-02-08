import numpy as np
import datetime
from plot import *


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
        if line[0]=="[":
            toSplit1=line.split("]")
            toSplit2=toSplit1[0].split(" ")
            toSplit3=toSplit2[0].split("-")
            toSplit4=toSplit2[1].split(":")
            #print(toSplit4[0])
            if int(toSplit4[2])!="":
                sec=int(toSplit4[2])
            else:
                sec=0
            date=datetime.datetime(int(toSplit3[0][1:]),int(toSplit3[1]),int(toSplit3[2]),int(toSplit4[0])+1,int(toSplit4[1]),sec)
            value=toSplit1[1].strip()
            if value=="BATCH" :
                compteur+=50
            tab_donnees.append((date,value,compteur))
            #print(date,value,compteur)
        else:
            if line=='BATCH':
                compteur+=50
                tab_donnees.append((date,'BATCH',compteur))
            elif line=='SPEED +':
                tab_donnees.append((date,'SPEED +',compteur))
            elif line=='STOP':
                tab_donnees.append((date,'STOP',compteur))
            elif line=='START':
                tab_donnees.append((date,'START',compteur))
            else:
                line = file.readline()
        line = file.readline()
    lastdate=datetime.datetime(int(toSplit3[0][1:]),int(toSplit3[1]),int(toSplit3[2]),17,0,1)
    if date < lastdate:
        tab_donnees.append((lastdate,'END',0))
    file.close()
    return tab_donnees,firstdate,lastdate
        
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
def fonctionnement(tab_donnees,firstdate,lastdate):
    tab_debut=[]
    tab_fin=[]
    deb=False
    flagfin=True
    minutes = datetime.timedelta(minutes=60)
    for i in range(len(tab_donnees)):
        if tab_donnees[i][1]=="SPEED +" and deb==False:
            debut=(tab_donnees[i][0])
            debutdec=debut+minutes
            deb=True
            flagfin=False
        if tab_donnees[i][1]=='STOP' and flagfin==False:
            fin=(tab_donnees[i][0])
            deb=False
            flagfin=True
            if debut.strftime('%H')==fin.strftime('%H'):
                tab_debut.append(debut)
                tab_fin.append(fin)
            elif fin.strftime('%H')==(debutdec).strftime('%H'):
                findec=debut
                findec=findec.replace(minute=59,second=59)
                debutdec=fin
                debutdec=debutdec.replace(minute=0,second=0)
                tab_debut.append(debut)
                tab_fin.append(findec)
                tab_debut.append(debutdec)
                tab_fin.append(fin)
            else:
                finone=debut.replace(minute=59,second=59)
                debuttwo=(debut+minutes).replace(minute=0,second=0)
                fintwo=debuttwo.replace(minute=59,second=59)
                debuthree=fin.replace(minute=0,second=0)
                tab_debut.append(debut)
                tab_fin.append(finone)
                tab_debut.append(debuttwo)
                tab_fin.append(fintwo)
                tab_debut.append(debuthree)
                tab_fin.append(fin)
    tab_duree=[]
    for i in range(len(tab_debut)):
        if tab_debut[i] is None:
           continue
        elif i+1<len(tab_debut):
            if tab_debut[i].strftime('%H')!=tab_debut[i+1].strftime('%H'):
                #print(tab_debut[i].strftime('%H'),tab_debut[i+1].strftime('%H'))
                #rint(tab_fin[i]-tab_debut[i])
                dureetmp=tab_fin[i]-tab_debut[i]
                tab_duree.append((tab_debut[i].strftime('%H'),dureetmp))
            else:
                j=i
                dureetmp=datetime.timedelta(seconds=0)
                while tab_debut[j].strftime('%H')==tab_debut[j+1].strftime('%H'):
                    dureetmp1=tab_fin[j]-tab_debut[j]
                    dureetmp=dureetmp+dureetmp1
                    dureetmp2=tab_fin[j+1]-tab_debut[j+1]
                    tmp=tab_debut[j]
                    tab_debut[j]=None
                    if j+1==len(tab_debut)-1:
                        break
                    else:
                        j+=1
                dureetmp=dureetmp+dureetmp2
                tab_duree.append((tmp.strftime('%H'),dureetmp))
                tab_debut[j]=None
        else:
            dureetmp=tab_fin[i]-tab_debut[i]
            tab_duree.append((tab_debut[i].strftime('%H'),dureetmp))
    #print(tab_duree)
    tab_duree_tot=[]
    firstdate2=firstdate
    minutes = datetime.timedelta(minutes=60)
    t=0
    while firstdate2.strftime('%H')<lastdate.strftime('%H'):
        sec=datetime.timedelta(seconds=0)
        if t<len(tab_duree):
            if firstdate2.strftime('%H')!=tab_duree[t][0]:
                #print(firstdate2.strftime('%H'),tab_duree[i][0])
                
                tab_duree_tot.append((firstdate2.strftime('%H'),sec))
            else:
                tab_duree_tot.append((tab_duree[t][0],tab_duree[t][1]))
                t=t+1
            firstdate2=firstdate2+minutes
        else:
            tab_duree_tot.append((firstdate2.strftime('%H'),sec))
            t=t+1
            firstdate2=firstdate2+minutes
    #print(tab_duree_tot)
    return(tab_duree_tot)
#
#@brief fonction qui produit un tableau pour taux de fonctionnement horaire 
#@param le tableau de durée de fonctionnement par heure
#@return le tableau avec % de fcnmt/heure
#  
def graphFcnmt(tab_duree_tot):
    tabGrapheFnmt=[]
    for i in range(len(tab_duree_tot)):
        td=datetime.timedelta(days=0, minutes=60)
        if tab_duree_tot[i][1]!=0:
            pourcentage=round((tab_duree_tot[i][1]/td*100),1)
        else:
            pourcentage=0
        tabGrapheFnmt.append((tab_duree_tot[i][0],pourcentage))
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