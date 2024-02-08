from plot import *
from tableaux import *

v=30
z=33

#chemin_dest='C:/Users/Gwen/Desktop/Data/Bulgarie/donneesNettoyees2.txt'


def dothejob(chemin_src):
    tab_donnees,firstdate,lastdate=recupDonnees(chemin_src)
    #print(tab_donnees,firstdate,lastdate)
    #saveTxt(tab_donnees,chemin_dest)
    tab_duree_tot=fonctionnement(tab_donnees,firstdate,lastdate)
    #print(tab_duree_tot)
    tabGrapheFnmt=graphFcnmt(tab_duree_tot)
    #print(tabGrapheFnmt)
    courbeFcnmt(tabGrapheFnmt,firstdate)
    tabGraphSac=graphSac(tab_donnees,firstdate)
    #print(tabGraphSac)
    courbeSac(tabGraphSac)


for v in range(v,z):
    chemin_src='C:/Users/Gwen/Desktop/Data/Bulgarie/europack-'+str(v)+'.log'
    dothejob(chemin_src)

