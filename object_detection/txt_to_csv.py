import os
import sys
import glob
from PIL import Image




def main():
	dossier_source  = sys.argv[1] #dossier annotations
	fichier_cible = sys.argv[2] #fichier_csv
	if  os.path.exists(fichier_cible):
		os.system("rm "+ fichier_cible)
	fichier_ecriture=open(fichier_cible, "a")
	fichier_ecriture.write("filename,width,height,class,xmin,ymin,xmax,ymax"+"\n")


	dossiers =[s for s in os.listdir(dossier_source)]
	for dos in dossiers:
			fichiers = [s for s in os.listdir(dossier_source+"/"+dos+"/") if s.endswith (".txt")]
			for f in fichiers:
				print (f)
				lecture = open(dossier_source+"/"+dos+"/"+ f, "r")
				lignes= lecture.readlines()
				for l in lignes:
					print (l)
					nom = f
					nom_brut = f.split(".")[0]
					img = Image.open(dossier_source+"/"+dos +"/"+nom_brut +".jpg")
					width, height = img.size
					classe = l.split(" ")[4]
					print(classe)
					'''if classe == "Siganus_rivulatus" :
						classe=classe
					else:
						classe="Other_Fish"'''
					classe=classe.replace("\n","",5)
					print(classe)
					depart_x=l.split(" ")[0]#str(float(l.split(" ")[0])*float(width))
					depart_y=l.split(" ")[1]
					fin_x=l.split(" ")[2]
					fin_y=l.split(" ")[3]
					fichier_ecriture.write( dossier_source+"/"+dos +"/"+nom_brut+".jpg" +","+ str(width)+","+  str(height)+","+ classe+","+  str(depart_x)+","+  str(depart_y)  +","+str(fin_x) +","+ str(fin_y)   +"\n")
#filename,width,height,class,xmin,ymin,xmax,ymax
#53.jpeg,1920,1080,fish,808,106,888,254

#1385 227 1420 244 Siganus_rivulatus 

main()
