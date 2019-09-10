"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import sys
import os
import io
import pandas as pd
import tensorflow as tf
from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_dir', '', 'Path to images')
FLAGS = flags.FLAGS


# TO-DO replace this with label map
def class_text_to_int(row_label):
	dico_classe={}
	lelz = open('PATH TO BECONFIGURED')
	lignes = lelz.readlines()
	for l in lignes:
		dico_classe[l.split(":")[1].replace("\n","",69)]=l.split(":")[0]
	''' if row_label == 'Siganus_rivulatus':
		return 1
	elif row_label == 'Zebrasoma_desjardinii':
		return 2
	elif row_label == 'Zebrasoma_xanthurum':
		return 3
	elif row_label == 'Diplodus_sargus':
		return 4
	elif row_label == 'Chaetodon_lunula':
		return 5
	elif row_label == 'Scaridae':
		return 6
	elif row_label == 'Arothron_diadematus':
		return 7
	elif row_label == 'unknown_fish':
		return 8
	elif row_label == 'Acanthuridae':
		return 9
	elif row_label == 'Abudefduf_vaigiensis':
		return 10
	elif row_label == 'Coris_julis':
		return 11'''
	'''if row_label == 'fish':
        	return 1
	else:
        	return  None'''
	print(dico_classe)
	return int(dico_classe[row_label])
def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    print (group.filename)
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []


    classes_text = []
    classes = []
    print (filename)
    for index, row in group.object.iterrows():

        xmins.append(float(row['xmin']) / width)

        xmaxs.append(float(row['xmax']) / width)
        ymins.append(float(row['ymin']) / height)
        ymaxs.append(float(row['ymax']) / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))
    print (classes_text)
    print (classes)
    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    csv_input = sys.argv[1] #path to th .csv file containing the annotations
    output_path = sys.argv[2] #path to where the .record file will be created


    print (output_path)

    writer = tf.python_io.TFRecordWriter(output_path)

    path = os.path.join(FLAGS.image_dir)
    examples = pd.read_csv(csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()

    print('Successfully created the TFRecords: {}')


if __name__ == '__main__':
    tf.app.run()
