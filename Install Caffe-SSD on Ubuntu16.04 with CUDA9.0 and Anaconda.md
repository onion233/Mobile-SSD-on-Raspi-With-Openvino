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

## [My Makefile.config](https://github.com/onion233/Mobile-SSD-on-Raspi-With-Openvino/blob/master/Install_Caffe-SSD/Makefile.config)

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

## [My Makefile]([http://coding.net](https://github.com/onion233/Mobile-SSD-on-Raspi-With-Openvino/blob/master/Install_Caffe-SSD/Makefile))
Add libraries to enable build with opencv, boost and hdf5
```sh
LIBRARIES +=glog gflags protobuf leveldb snappy \
  lmdb boost_system boost_filesystem hdf5_hl hdf5 m \
  opencv_core opencv_highgui opencv_imgproc opencv_imgcodecs opencv_videoio boost_regex
```
Update NVCC compiler flag
```sh
NVCCFLAGS += -D_FORCE_INLINES -ccbin=$(CXX) -Xcompiler -fPIC $(COMMON_FLAGS)
```

# Make Caffe

Beforing making, check there are no pre-distributed caffe files in dir:
```sh
/usr/local/lib
/urs/local/include
```
Make target
```sh
make all -j8
make test -j8
make runtest -8
make py
make pytest

```
## Add caffe python interface in the env

```sh
cd $ENV_PATH
mkdir -p ./etc/conda/activate.d
mkdir -p ./etc/conda/deactivate.d
touch ./etc/conda/activate.d/env_vars.sh
touch ./etc/conda/deactivate.d/env_vars.sh
```
Edit ./etc/conda/activate.d/env_vars.sh as follows:
```sh
export PYTHONPATH=$HOME/caffe/python:$PYTHONPATH
```

Edit ./etc/conda/deactivate.d/env_vars.sh as follows:
```sh
unset PYTHONPATH
```

Reload the current environment to reflect the variables
```sh
source activate caffe
```
Check our installation
```sh
# To check if Caffe build was successful
python -c 'import caffe; caffe.set_mode_gpu()' 2>/dev/null && echo "Success" || echo "Failure"
#=> Success
```
Now the Caffe-SSD is successfully installed. Distribute the header and lib by:
```sh
cd CAFFEDIR
make distribute
```
# Common Issue

## Official collected issues:
https://github.com/BVLC/caffe/wiki/Commonly-encountered-build-issues
## Undefined symbol error when importing caffe
```sh
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/home/cc/Downloads/caffe/python/caffe/__init__.py", line 1, in <module>
    from .pycaffe import Net, SGDSolver, NesterovSolver, AdaGradSolver, RMSPropSolver, AdaDeltaSolver, AdamSolver, NCCL, Timer
  File "/home/cc/Downloads/caffe/python/caffe/pycaffe.py", line 13, in <module>
    from ._caffe import Net, SGDSolver, NesterovSolver, AdaGradSolver, \
ImportError: /home/cc/Downloads/caffe/python/caffe/_caffe.so: undefined symbol: _ZN5boost6python6detail11init_moduleER11PyModuleDefPFvvE
```

*Solution*
Relinking libboost_python.so to libboost_python-py35.so and remake caffe. (python3.6 is compatible with this lib)
```sh
cd /usr/lib/x86_64-linux-gnu
sudo rm -rf libboost_python.so
sudo ln -s libboost_python-py35.so libboost_python.so
sudo ldconfig
```



# Reference 
* https://yangcha.github.io/Caffe-Conda/
* https://blog.csdn.net/DonatelloBZero/article/details/51304162
* https://github.com/BVLC/caffe/issues/5810
* https://blog.csdn.net/u014381600/article/details/52075539
* https://blog.csdn.net/zhuangwu116/article/details/81169700
* https://blog.csdn.net/yw80557674/article/details/80119264
* https://github.com/BVLC/caffe/wiki/GeForce-GTX-1080,---CUDA-8.0,---Ubuntu-16.04,---Caffe