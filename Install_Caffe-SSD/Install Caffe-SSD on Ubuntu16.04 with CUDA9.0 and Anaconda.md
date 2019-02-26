# Environment Specific
```
OS: Ubuntu 16.04
Prerequisite: Anaconda3, CUDA 9.0, CUDNN 7.0, G++ 5.4
```

# Installing Caffe General Dependencies
```sh
sudo apt update
sudo apt upgrade
sudo apt install libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler libopenblas-dev
sudo apt install --no-install-recommends libboost-all-dev
```

Be careful we are installing opencv3 lib with libopencv-dev. Please make sure there are no other opencv version installed in your environment. Otherwise the compiler may be confused with different opencv lib later.

# Fecth Caffe-SSD Source Code
Prepare your caffe dir. My working dir is:
```sh
$ pwd   
/root
```
So my caffe dir will be:
```sh
/root/caffe
```
However, it's not recommend for most user to run in a root mode, so your dir can be:
```sh
/home/YOURHOSTNAME/caffe
```
Clone a set of resource:
```sh
git clone https://github.com/weiliu89/caffe.git
git checkout SSD
``` 
In the following, CAFFEDIR refers to your absolute caffe path.


# Setting Up Python3 Virtual Env
```sh
source create caffe python=3.6 pip
source activate caffe
cd CAFFEDIR/python
for req in $(cat requirements.txt); do pip install $req --upgrade; done
```

# Modify Make Configurations

Be careful about _@ CHANGE HERE_ in the script. First, we modify the Makefile.config by:
```sh
cd CAFFEDIR
cp Makefile.config.example Makefile.config
vim Makefile.config
```

## My Makefile.config

Enable CUDNN
```sh
# cuDNN acceleration switch (uncomment to build with cuDNN).
USE_CUDNN := 1
```
Enable opencv3
```sh
# Uncomment if you're using OpenCV 3
OPENCV_VERSION := 3
```
For CUDA 9.0,  remove arch below 30 since they are not supported
```sh
# CUDA architecture setting: going with all of them.
# For CUDA < 6.0, comment the lines after *_35 for compatibility.
CUDA_ARCH := -gencode arch=compute_30,code=sm_30 \
             -gencode arch=compute_35,code=sm_35 \
             -gencode arch=compute_50,code=sm_50 \
             -gencode arch=compute_52,code=sm_52 \
             -gencode arch=compute_61,code=sm_61
```
Use openblas
```sh
BLAS := open
```
Comment python2 path since we are using anaconda
```sh
#PYTHON_INCLUDE := /usr/include/python2.7 \
		/usr/lib/python2.7/dist-packages/numpy/core/include
```
Specific anaconda python include
```sh
# Anaconda Python distribution is quite popular. Include path:
# Verify anaconda location, sometimes it's in root.
ANACONDA_HOME := /root/Anacondas/anaconda3/envs/caffe
PYTHON_INCLUDE := $(ANACONDA_HOME)/include \
		$(ANACONDA_HOME)/include/python3.6m \
		$(ANACONDA_HOME)/lib/python3.6/site-packages/numpy/core/include 
```
Declare python lib 
```sh
# We need to be able to find libpythonX.X.so or .dylib.
PYTHON_LIBRARIES := boost_python3 python3.6m
PYTHON_LIB := $(ANACONDA_HOME)/lib
```

Enable python layers
```sh
# Uncomment to support layers written in Python (will link against Python libs)
WITH_PYTHON_LAYER := 1
```