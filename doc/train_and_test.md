!! Make sure you have gone through all the <a href='Prerequisites.md'>Prerequisites</a> !!<br>

## A. Train the FishNet model

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
- In the same command prompt, run the following line to create `annotations.csv` in `Catching-fish-presence-FishNet/object_detection/FishNet/data/`: (Paths to be configured)
```bash
python txt_to_csv.py /path/to/Catching-fish-presence-FishNet/images/training_set path/to/Catching-fish-presence-FishNet/object_detection/FishNet/data/annotations.csv
```
<br>

2. Creating a .record file from the .csv file:
- In the same command prompt that you left open since step A.1., run the following line to create `train.recrod` in `Catching-fish-presence-FishNet/object_detection/FishNet/data/`: (Paths to be configured)
```bash
python generate_tfrecord.py path/to/Catching-fish-presence-FishNet/object_detection/FishNet/data/annotations.csv path/to/Catching-fish-presence-FishNet/object_detection/FishNet/data/train.record
```
<br>

3. Open `Catching-fish-presence-FishNet/object_detection/FishNet/data/pipeline.config` with a text editor and check the following:
- line 3: num_classes: the number of classes in your dataset, if you're using the training image set provided in this git then there is only 1 class: "fish".
- line 107: fine_tune_checkpoint: the path must lead to `Catching-fish-presence-FishNet/object_detection/FishNet/model/pre-trained_model/model.ckpt`
- line 109 and 118: num_steps and num_examples must be set to ??? and ??? if you are using the training image set provided in this git.
- line 112 and 123: label_map_path: the path must lead to `Catching-fish-presence-FishNet/object_detection/FishNet/data/object_detection.pbtxt`
- line 114 and 127: input path: the path must lead to `Catching-fish-presence-FishNet/object_detection/FishNet/data/train.record`
<br>

4. Start the training:
- In the same command prompt that you left open since step A.1., run the following line to start the training: (Paths to be configured)
```bash
python3 train.py --logtostderr --train_dir=path/to/Catching-fish-presence-FishNet/object_detection/FishNet/model/train --pipeline_config_path=path/to/Catching-fish-presence-FishNet/object_detection/FishNet/data/pipeline.config
```
- If the training is interrupted and you must redo it, move or delete every file in `Catching-fish-presence-FishNet/object_detection/FishNet/model/train` before doing so.
<br>

5. Once the training is done (it will take some time), export the trained model:
- In the same command prompt that you left open since step A.1., run the following line to export the newly trained model into the folder `Catching-fish-presence-FishNet/object_detection/FishNet/model/fine_tuned_model`: (Paths to be configured)
```bash
python export_inference_graph.py --input_type image_tensor --pipeline_config_path path/to/Catching-fish-presence-FishNet/object_detection/FishNet/data/pipeline.config --trained_checkpoint_prefix path/to/Catching-fish-presence-FishNet/object_detection/FishNet/model/train/model.ckpt-123456 --output_directory path/to/Catching-fish-presence-FishNet/object_detection/FishNet/model/fine_tuned_model
```
- In `--trained_checkpoint_prefix path/to/model/train/model.ckpt-123456`.
"123456" is given as an example, replace this number with the number of steps you indicated at step A.3.
<br>

## B. Test the newly trained FishNet model

1. Open `Catching-fish-presence-FishNet/object_detection/detection.py` with a text editor and check the following:
- line 12: NUM_CLASSES: the number of classes in your dataset, if you're using the training image set provided in this git then there is only 1 class: "fish".
- line 11 & 15: Edit PATH_TO_LABELS and PATH_TO_MODEL so they point respectively to `Catching-fish-presence-FishNet/object_detection/FishNet/data/object_detection.pbtxt` and `Catching-fish-presence-FishNet/object_detection/FishNet/model/fine_tuned_model/frozen_inference_graph.pb`
- Path at line 19 must also point to `Catching-fish-presence-FishNet/object_detection/FishNet/model/fine_tuned_model/frozen_inference_graph.pb`
- line 119: make sure the image format at the end of the line is the same as the images you have in your test set (.jpeg/ .jpg/ etc..) which are located in `Catching-fish-presence-FishNet/images/test_set`.
<br>

2. Open `Catching-fish-presence-FishNet/object_detection/FishNet/data/object_detection.pbtxt` with a text editor and make sure that for each class in your dataset you have: (if you are using the training image set provided in this git, there is only one class: "fish")
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

3.Open `Catching-fish-presence-FishNet/object_detection/FishNet/data/class_list.txt` with a text editor and make sure that for each class in your dataset you have: (if you are using the training image set provided in this git, there is only one class: "fish")
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

6. You can also make your own set of annotated images that you can test or train the model on. You can do that using apps like <a href='https://github.com/tzutalin/labelImg'>LabelIMG</a> <br>
Make sure that the images and their associated .txt files are organized the same way than the images given in `Catching-fish-presence-FishNet/images`.
