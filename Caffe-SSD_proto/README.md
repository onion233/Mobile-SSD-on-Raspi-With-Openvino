# Install Caffe-SSD 
Follow my [wiki](https://github.com/onion233/Mobile-SSD-on-Raspi-With-Openvino/wiki/Caffe-SSD-Installation-on-Ubuntu16.04-CUDA9.0-with-Anaconda3) to install Caffe-SSD
# Prepare the Dataset
Use [LabelImg](https://github.com/tzutalin/labelImg) to annotate your dataset with xml format. Generally, the extension of the picture is .jpg. Pictures and annotations are in two different dir, eg:
```sh
$DATAROOT/MobileSSD/Annotations
$DATAROOT/MobileSSD/JPEGImages
```
Add all the training/val samples in 
```sh
$DATAROOT/MobileSSD/ImageSets/Main/trainval.txt
```
Add all the test samples in 
```sh
$DATAROOT/MobileSSD/ImageSets/Main/test.txt
```
The trainval.txt or test.txt are just plain files each line corresponds to the pictures. For example, I have dataset `1.jpg ... k.jpg` and here is my [test.txt](https://github.com/onion233/Mobile-SSD-on-Raspi-With-Openvino/blob/master/tools/text.txt) 

You can use my [tool](https://github.com/onion233/Mobile-SSD-on-Raspi-With-Openvino/blob/master/tools/gen_train_test.py) to generate these two files

# Create LMDB Files For Training 
Here we use VOC example to create our LMDB files.
```sh
$ cd $CAFFEROOT/data
$ mkdir MobileSSD
$ cp VOC0712/* MobileSSD/
```
Modify the `MobileSSD/create_list.sh` (you can replace MobileSSD with your datase name):
```sh
ln:3 root_dir=$DATAROOT
ln:13 for name in MobileSSD
```
Run `MobileSSD/create_list.sh` to generate `test_name_size.txt`, `test.txt`, and `trainval.txt` in `data/MobileSSD/`. These files contain the image and annotation path.

Rename the `labelmap_voc.prototxt` to `labelmap_MobileSSD.prototxt` and modify the class name and id according to your dataset.

Next, modify `MobileSSD/create_data.sh` 
```sh
ln:7 data_root_dir="$DATAROOT"
ln:8 dataset_name="MobileSSD"
ln:9 mapfile="$root_dir/data/$dataset_name/labelmap_MobileSSD.prototxt"
```
Then simply run `MobileSSD/create_data.sh`.
This will create LMDB database in `$DATAROOT/MobileSSD` and make a soft link in `$CAFFERPPT/examples/MobileSSD/`.
# Create Network Prototxt
Thanks to [@chuanqi](https://github.com/chuanqi305/MobileNet-SSD), we can use the `gen.py` to generate the `train.prototxt`, `test.prototxt` and `depoly.prototxt`. You may wish to modify some parameters like `input_size`, `aspect ratio`, `min_scale`, `top_k` and so on.

# Train the Network
```sh
$ ../../build/tools/caffe train -solver="solver_train.prototxt" \
-weights="mobilenet_iter_73000.caffemodel" \
-gpu 0 
```
And test the network with 
```sh
$ ../../build/tools/caffe train -solver="solver_test.prototxt" \
--weights=$latest \
-gpu 0
```