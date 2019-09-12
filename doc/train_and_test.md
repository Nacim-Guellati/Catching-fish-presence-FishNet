0. Make sure you have gone through all the <a href='doc/Prerequisites.md'>Prerequisites</a><br>

## Test the model you just trained

1. Open `Catching-fish-presence-FishNet/object_detection/detection.py` with a text editor and check the following:
- line 12: NUM_CLASSES: the number of classes in your annotations.
- line 11 & 15: Edit PATH_TO_LABELS and PATH_TO_MODEL so they point respectively to `Catching-fish-presence-FishNet/object_detection/FishNet/data/object_detection.pbtxt` and `Catching-fish-presence-FishNet/object_detection/FishNet/model/fine_tuned_model/frozen_inference_graph.pb`
- Path at line 19 must also point to `Catching-fish-presence-FishNet/object_detection/FishNet/model/fine_tuned_model/frozen_inference_graph.pb`
- line 119: make sure the image format at the end of the line is the same as the images you have in your test set (.jpeg/ .jpg/ etc..) which are located in `Catching-fish-presence-FishNet/images/test_set`.


2. Open `Catching-fish-presence-FishNet/object_detection/FishNet/data/object_detection.pbtxt` with a text editor and make sure that for each class you have:
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


3.Open `Catching-fish-presence-FishNet/object_detection/FishNet/data/class_list.txt` with a text editor and make sure that for each class you have:
```bash
1:class_1
2:class_2
etc..
```


4. Run the following lines in your command prompt: (Paths are to be configured)
```bash
source venv/bin/activate #activate your virtual environment
export PYTHONPATH=/path/to/models-master/slim:$PYTHONPATH
cd path/to/models-master/research/
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:'/path/to/models-master/research':'/path/to/models-master/research/slim'
```
- `models-master` is the folder you downloaded in the <a href='doc/Prerequisites.md'>Prerequisites</a>.


5. Run the following in the same command prompt: (Paths are to be configured)
```bash
python detection.py path/to/Catching-fish-presence-FishNet/images/test_set path/to/results/folder path/to/Catching-fish-presence-FishNet/object_detection/data/class_list.txt
```
- This command will run the object detection on your test images and make result images from this set. In those images, boxes will show where he algorithm sees the different objects and it will associate to each of these boxes a score in % that represents degree of certainty in its detection. These results give you an idea on how the pre-trained model performs at detecting fishes.
- the second path in this command: `path/to/results/folder` points to a folder, that you must create, where you want the results to be saved.

6. You can also make your own set of annotated images on which you can run `detection.py`. You can do that using apps like <a href='https://github.com/tzutalin/labelImg'>LabelIMG</a> <br>
Make sure that they are organized the same way than the images given in `Catching-fish-presence-FishNet/images`
