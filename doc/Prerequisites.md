# Prerequisites

1. Ubuntu or MacOS operating system, if you are on Windows install an Ubuntu partition: 
https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-ubuntu#0 
https://tutorials.ubuntu.com/tutorial/tutorial-install-ubuntu-desktop#0

2. Install Tensorflow on a virtual environment: https://www.tensorflow.org/install/pip

3. Run the following lines in your virtual environment to install the dependencies:
``` bash
sudo apt install protobuf-compiler (for Ubuntu)
brew install protobuf (for MacOS)
pip install Pillow
pip install pandas
pip install object_detection
pip install matplotlib
pip install tensorboard
pip install opencv-python
```

4. Import `Catching-fish-presence-FishNet/object_detection` and `Catching-fish-presence-FishNet/images` folders on your machine.

5. Dowload this folder https://github.com/tensorflow/models and place it wherever you want.
