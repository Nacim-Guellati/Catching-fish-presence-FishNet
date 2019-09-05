import tensorflow as tf
import numpy as np
import cv2
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import matplotlib.pyplot as plt
from visualization_utils import visualize_boxes_and_labels_on_image_array
from label_map_util import create_category_index, load_labelmap, convert_label_map_to_categories
import sys
import os
import operator
PATH_TO_LABELS = "/home/marbec/Bureau/deeplelz/rfcn_resnet101_coco_2018_01_28/data/object_detection.pbtxt"
NUM_CLASSES=5
class TrafficLightClassifier(object):
    def __init__(self):
        PATH_TO_MODEL = '/home/marbec/Bureau/deeplelz/rfcn_resnet101_coco_2018_01_28/model/fine_tuned_model/frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            # Works up to here.
            #with tf.gfile.GFile("/home/sebv/SebV/RCNN-detection/fish_detection/fish_detection_mobile_net/fine_tuned_fish_model/frozen_inference_graph.pb", 'rb') as fid:
            with tf.gfile.GFile("/home/marbec/Bureau/deeplelz/rfcn_resnet101_coco_2018_01_28/model/fine_tuned_model/frozen_inference_graph.pb", 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            self.d_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            self.d_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.d_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_d = self.detection_graph.get_tensor_by_name('num_detections:0')
        self.sess = tf.Session(graph=self.detection_graph)

    def get_classification(self, img,dossier_cible):
    # Bounding Box Detection.
        with self.detection_graph.as_default():
            # Expand dimension since the model expects image to have shape [1, None, None, 3].
            image = Image.open(img)
            print (type(image))
            image_name=img.split("/")[(img.split("/")).__len__()-1]
            label_map = load_labelmap(PATH_TO_LABELS)
            categories = convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
            category_index = create_category_index(categories)


            (im_width, im_height) = image.size
            im2=np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8) #image en bgr
            im2_rgb = im2[...,::-1]
            #cv2.imshow('image',im2)
            #plt.axis("off")
            #plt.imshow(cv2.cvtColor(im2, cv2.COLOR_BGR2RGB))
            #plt.show()
            #plt.imshow(cv2.cvtColor(im2_rgb, cv2.COLOR_BGR2RGB))
            #plt.show()
            #cv2.waitKey(0)
            img_expanded = np.expand_dims(im2, axis=0) 
            (boxes, scores, classes, num) = self.sess.run([self.d_boxes, self.d_scores, self.d_classes, self.num_d], feed_dict={self.image_tensor: img_expanded})
            #transforme scores
            liste_score=[]
            liste_classes=[]
            liste_boxes=[]
            for j in classes[0]:
                liste_classes.append(j)
            for k in scores[0]:
                liste_score.append(k)
            for l in boxes[0]:
                liste_boxes.append(l)
            np_liste_score = np.array(liste_score)
            np_liste_classes=np.array(liste_classes)
            np_liste_boxes=np.array(liste_boxes)
            image_boxes=visualize_boxes_and_labels_on_image_array(im2,np_liste_boxes,np_liste_classes,np_liste_score,category_index,use_normalized_coordinates=True,line_thickness=5)
            #plt.imshow(im2)
            #plt.show()
            #cv2.imshow('image',image_boxes)
            #cv2.waitKey(0)
            im = Image.fromarray(image_boxes)
            im.save(dossier_cible+"/"+image_name)
            print (dossier_cible+"/"+image_name)

        return boxes, scores, classes, num, image_boxes

def cropND(img, bounding):
    image = Image.open(img)
    (im_width, im_height) = image.size
    img=np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8) #image en bgr
    image_pil = Image.fromarray(np.uint8(img)).convert('RGB')
    im_width, im_height = image_pil.size
    print (im_width, im_height)
    ymin, ymax, xmin, xmax =bounding

    (left, right, top, bottom) = (int(ymax * im_width), int(xmax * im_width),
                                  int(ymin * im_height), int(xmin * im_height))
    #ici on fa fait une approx pour avoir des int
    #print (bounding)
    #print (left,right,top,bottom)
    box = (left, top, right, bottom)
    area = image_pil.crop(box)
    #area.show()
    return area


def get_bounding_box_list(img, txt_file):

        mon_fichier = open(txt_file, "r")
        lignes_fichier= mon_fichier.readlines()
        liste_box_vt=[]#key=startX_startY_endX_endY, value=espece

        for l in lignes_fichier:
            startX=l.split(' ')[0]
            startY=l.split(' ')[1] 
            endX=l.split(' ')[2] 
            endY=l.split(' ')[3] 
            espece=l.split(' ')[4]
            espece=espece.replace("\n","",1)
            liste_box_vt.append(startX+"_"+startY+"_"+endX+"_"+endY+"_"+espece)
        return liste_box_vt


def main():
    #image = "/media/sebv/Data/RESULTS_DETECTION/poissons/training/J2_43_C_GP020213-5a65f392d9044_18_04_04/57.jpeg"
    #image = "/media/sebv/Data/test_detect/images/162.jpeg"
    dossier_source = sys.argv[1] #dossier contenant les frames poissons a traiter
    dossier_cible = sys.argv[2] #dossier contenant les frames poissons a traiter
    liste_espece=sys.argv[3]
    #TrafficLightClassifier().__init__()
    images =[ k for k in os.listdir (dossier_source) if k.endswith ('.jpg') ]

    dico_espece={}
    dico_lecture= open(liste_espece, "r")
    dico_lignes= dico_lecture.readlines()
    for l in dico_lignes:
        num=l.split(":")[0]
        espece=l.split(":")[1]
        espece=espece.replace("\n","",1)
        dico_espece[int(num)]=espece
    print (dico_espece)
    for image in images:
        image_dessin = Image.open(dossier_source+"/"+image)
        draw = ImageDraw.Draw(image_dessin)
        im_width,im_height=image_dessin.size



        nom_image = image.split(".")[0]
        txt_img=nom_image+".txt"
        liste_box_vt=get_bounding_box_list(dossier_source+"/"+image ,dossier_source+"/"+txt_img)
        compteur_boxes_corrects=0
        compteur_boxes_corrects_mauvaise_espece=0
        boxes,scores,classes,num,image_boxes=TrafficLightClassifier().get_classification(dossier_source+'/'+image,dossier_cible)
        #print (boxes)
        compteur=0
        ########decoup des vignettes dans la frame###########
        liste_classe_over_threshold=[]
        liste_boxes_over_threshold=[]
        for box in boxes[0]:
            score=scores[0][compteur]
            if score >= 0.75:
                #print (box)
                #image_crop=cropND(dossier_source+"/"+image, box)
                #print (score)
                liste_classe_over_threshold.append(classes[0][compteur])
                liste_boxes_over_threshold.append(boxes[0][compteur].tolist())
            compteur+=1

                #image_crop.show()
        #####################################################
        #print (boxes)
        #print (scores)


        #########################################TEST COMPOSITION######
        #on recup la liste des espece du reseau
        liste_espece_vr=[]
        for c in liste_classe_over_threshold:
            if c not in liste_espece_vr:
                liste_espece_vr.append(c)
        liste_espece_vr_nom=[]
        for k in liste_classe_over_threshold:
            #print (k)
            liste_espece_vr_nom.append(dico_espece[int(k)])
        #on recup la liste des especes terrain
        liste_espece_vt=[]
        for box_1_vt in liste_box_vt:   
                debut_x_vt=box_1_vt.split("_")[0]
                debut_y_vt=box_1_vt.split("_")[1]
                fin_x_vt=box_1_vt.split("_")[2]
                fin_y_vt=box_1_vt.split("_")[3] 
                espece_vt=box_1_vt.split("_")[4]
                if box_1_vt.split("_").__len__()>5:
                	genre_vt_2 =box_1_vt.split("_")[5]
                	espece_vt=espece_vt+"_"+genre_vt_2


                if espece_vt not in liste_espece_vt:
                    liste_espece_vt.append (espece_vt)

        #print (liste_espece_vr)
        #print (liste_espece_vt)
        #print (set(liste_espece_vr_nom).intersection(liste_espece_vt))
        print (set(liste_espece_vr_nom).symmetric_difference(set(liste_espece_vt)))
        ####################################################################

        #####################TEST NOMBRE BOUNDING BOXES################
        nombre_boxes_reseau=liste_espece_vr.__len__()
        nombre_boxes_vt=liste_box_vt.__len__()

        diff_boxes=abs(nombre_boxes_reseau-nombre_boxes_vt)
        ###############################################################


        ###################TEST MAX N##################################

        for box_vr in liste_boxes_over_threshold:
                    debut_x_vr=int(box_vr[1]*im_width)
                    debut_y_vr=int(box_vr[0]*im_height)
                    fin_x_vr=int(box_vr[3]*im_width)
                    fin_y_vr=int(box_vr[2] *im_height)
                    draw.rectangle([(int(debut_x_vr), int(debut_y_vr)), (int(fin_x_vr), int(fin_y_vr))], fill=None, outline='red')

        ########test precision bounding boxes########
        for box_vt in liste_box_vt:   
                debut_x_vt=int(box_vt.split("_")[0])
                debut_y_vt=int(box_vt.split("_")[1])
                fin_x_vt=int(box_vt.split("_")[2])
                fin_y_vt=int(box_vt.split("_")[3] )
                espece_vt=box_vt.split("_")[4]
                if box_1_vt.split("_").__len__()>5:
                	genre_vt_2 =box_1_vt.split("_")[5]
                	espece_vt=espece_vt+"_"+genre_vt_2
                boxAArea = (int(fin_x_vt) - int(debut_x_vt) + 1) * (int(fin_y_vt) - int(debut_y_vt) + 1)# compute the area
                draw.rectangle([(int(debut_x_vt), int(debut_y_vt)), (int(fin_x_vt), int(fin_y_vt))], fill=None, outline='white')
                #fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
                draw.text((debut_x_vt+5,fin_y_vt+5), espece_vt, fill=(0,255,255,128))
                compteur_box_vr=0
                compteur_index_box=0
                for box_vr in liste_boxes_over_threshold:
                    debut_x_vr=int(box_vr[1]*im_width)
                    debut_y_vr=int(box_vr[0]*im_height)
                    fin_x_vr=int(box_vr[3]*im_width)
                    fin_y_vr=int(box_vr[2] *im_height)
                    espece_vr=liste_espece_vr_nom[compteur_box_vr]
                    #print (debut_x_vr,debut_y_vr,fin_x_vr,fin_y_vr)
                    #print (debut_x_vt,debut_y_vt,fin_x_vt,fin_y_vt)
                    #(left, right, top, bottom) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)
                    boxBArea = (int(fin_x_vr) - int(debut_x_vr) + 1) * (int(fin_y_vr) - int(debut_y_vr) + 1)# compute the area

                    # determine the (x, y)-coordinates of the intersection rectangle                    
                    xA = max(int(debut_x_vt), int(debut_x_vr))
                    yA = max(int(debut_y_vt), int(debut_y_vr))
                    xB = min(int(fin_x_vt), int(fin_x_vr))
                    yB = min(int(fin_y_vt), int(fin_y_vr))
                    #print (xA, yA, xB, yB)
                    #compute the area of intersection rectangle
                    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
                    #print (interArea)
                    #print (boxAArea)
                    #print (boxBArea)

                    iou = interArea / float(boxAArea + boxBArea - interArea)


                    if   iou >= 0.5:

                        if espece_vt==espece_vr:
                                            draw.rectangle([(int(debut_x_vr), int(debut_y_vr)), (int(fin_x_vr), int(fin_y_vr))], fill=None, outline='green')
                                            liste_boxes_over_threshold.remove(liste_boxes_over_threshold[compteur_index_box])
                                            #fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
                                            draw.text((debut_x_vr-5,debut_y_vt-5), espece_vt, fill=(0,0,255,128))
                        else:
                                            draw.rectangle([(int(debut_x_vr), int(debut_y_vr)), (int(fin_x_vr), int(fin_y_vr))], fill=None, outline='yellow')
                                            liste_boxes_over_threshold.remove(liste_boxes_over_threshold[compteur_index_box])
                                            #fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
                                            draw.text((debut_x_vr-5,debut_y_vt-5), espece_vr, fill=(0,0,255,128))

                    print (iou)
                    compteur_box_vr+=1
                    compteur_index_box+=1
        for kbox in  liste_boxes_over_threshold:
                draw.rectangle([(int(debut_x_vr), int(debut_y_vr)), (int(fin_x_vr), int(fin_y_vr))], fill=None, outline='red')

        image_dessin.save(dossier_cible+"/"+"dessin_"+image, "JPEG")

        ###################################################
if __name__ == '__main__':
        main()
