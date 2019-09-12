# Test the pre-trained FishNet model on test images

1. Open `Catching-fish-presence-FishNet/object_detection/detection.py` with a text editor and check the following:
- line 12: NUM_CLASSES: the pre-trained model only have 1 class: "fish" so it should be set to "1"
- Edit PATH_TO_LABELS and PATH_TO_MODEL so they point respectively to `Catching-fish-presence-FishNet/object_detection/FishNet/data/object_detection.pbtxt` and `Catching-fish-presence-FishNet/object_detection/FishNet/model/pre-trained_model/frozen_inference_graph.pb`
- Path at line 21 must also point to `Catching-fish-presence-FishNet/object_detection/FishNet/model/pre-trained_model/frozen_inference_graph.pb`
- line 124: make sure the image format is the same as the images you have in your test set (.jpeg/ .jpg/ etc..) which are located in `Catching-fish-presence-FishNet/images/test_set`.


2. Run the following lines in your command prompt:
````bash
source venv/bin/activate
export PYTHONPATH=/path/to/models-master/slim:$PYTHONPATH
cd path/to/models-master/research/
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:'/path/to/models-master/research':'/path/to/models-master/research/slim'
````
- `models-master` is the folder you downloaded in the Prerequisites.


3. Run the following in the same command prompt:
````bash
python detection.py path/to/Catching-fish-presence-FishNet/images/test_set path/to/results/folder path/to/Catching-fish-presence-FishNet/object_detection/data/class_list.txt
````
