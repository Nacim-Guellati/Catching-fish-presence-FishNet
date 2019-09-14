!! Make sure you have gone through all the <a href='Prerequisites.md'>Prerequisites</a> !!<br>

## A. Train the model

1. Creating a .csv file that gathers all the annotations: <br>
- Open `Catching-fish-presence-FishNet/object_detection/txt_to_csv.py` with a text editor and check that on lines 29 and 43 you have the same image format than the images in your training set (.jpg / .jpeg / etc.)
- Run the following lines in a command prompt and leave it open untill the end of the tutorial: (Paths to be configured)<br>
(`models-master` is the folder you downloaded in the <a href='Prerequisites.md'>Prerequisites</a>.)
```bash
source venv/bin/activate #activate your virtual environment
export PYTHONPATH=/path/to/models-master/slim:$PYTHONPATH
cd path/to/models-master/research/
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:'/path/to/models-master/research':'/path/to/models-master/research/slim'
```
- In the same command prompt, run the following line to create annotations.csv and place it in `Catching-fish-presence-FishNet/object_detection/FishNet/data/`:
```bash
python txt_to_csv.py /path/to/Catching-fish-presence-FishNet/images/training_set path/to/Catching-fish-presence-FishNet/object_detection/FishNet/data/annotations.csv
```

2.


## B. Test the model you just trained

1. Open `Catching-fish-presence-FishNet/object_detection/detection.py` with a text editor and check the following:
- line 12: NUM_CLASSES: the number of classes in your dataset, if you're using the training image set provided in this git then there is only 1 class: "fish".
- line 11 & 15: Edit PATH_TO_LABELS and PATH_TO_MODEL so they point respectively to `Catching-fish-presence-FishNet/object_detection/FishNet/data/object_detection.pbtxt` and `Catching-fish-presence-FishNet/object_detection/FishNet/model/fine_tuned_model/frozen_inference_graph.pb`
- Path at line 19 must also point to `Catching-fish-presence-FishNet/object_detection/FishNet/model/fine_tuned_model/frozen_inference_graph.pb`
- line 119: make sure the image format at the end of the line is the same as the images you have in your test set (.jpeg/ .jpg/ etc..) which are located in `Catching-fish-presence-FishNet/images/test_set`.
<br>

2. Open `Catching-fish-presence-FishNet/object_detection/FishNet/data/object_detection.pbtxt` with a text editor and make sure that for each class in your dataset you have:
````bash
item {
  id: 1
  name: 'class_1'
}
item {
  id: 2
  name: 'class_2'
}
etc..
````
<br>

3.Open `Catching-fish-presence-FishNet/object_detection/FishNet/data/class_list.txt` with a text editor and make sure that for each class in your dataset you have:
```bash
1:class_1
2:class_2
etc..
```
<br>

5. Run the following in the command prompt that you left open at step A.1.: (Paths to be configured)
```bash
python detection.py path/to/Catching-fish-presence-FishNet/images/test_set path/to/results/folder path/to/Catching-fish-presence-FishNet/object_detection/data/class_list.txt
```
- This command will run the object detection on your test images and make result images from this set. In those images, boxes will show where he algorithm sees the different objects and it will associate to each of these boxes a score in % that represents degree of certainty in its detection. These results give you an idea on how the pre-trained model performs at detecting fishes.
- the second path in this command: `path/to/results/folder` points to the folder, that you must create, where you want the results to be saved.
<br>

6. You can also make your own set of annotated images on which you can run `detection.py`. You can do that using apps like <a href='https://github.com/tzutalin/labelImg'>LabelIMG</a> <br>
Make sure that the images and their associated .txt files are organized the same way than the images given in `Catching-fish-presence-FishNet/images`.
