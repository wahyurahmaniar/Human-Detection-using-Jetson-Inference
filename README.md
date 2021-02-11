# Human-Detection-using-Jetson-Inference
Jetson inference is realtime DNN vision library for NVIDIA Jetson Nano/TX1/TX2/Xavier NX/AGX Xavier.

For human detection, we can use some models such as pednet, multiped, SSD MobileNet-V1, SSD MobileNet-V1, and SSD Inception-V2.


# Installation
Install Jetson Inference
```bash
$ sudo apt-get update
$ sudo apt-get install git cmake libpython3-dev python3-numpy
$ git clone --recursive https://github.com/dusty-nv/jetson-inference
$ cd jetson-inference
$ mkdir build
$ cd build
$ cmake ../
$ make -j$(nproc)
$ sudo make install
$ sudo ldconfig
```

<img src="https://raw.githubusercontent.com/dusty-nv/jetson-inference/python/docs/images/download-models.jpg" width="650">

Select model:
* Ped-100
* Multi-500
* SSD-MobileNet-V1
* SSD-MobileNet-V2
* SSD-Inception-V2

More about Jetson Inference: https://github.com/dusty-nv/jetson-inference

# Human Detection Comparison Results
Real-Time Human Detection Using Deep Learning on Embedded Platforms: A Review

https://journal.umy.ac.id/index.php/jrc/article/view/10558
