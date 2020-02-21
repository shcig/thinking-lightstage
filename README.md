# Thinking Lightstage
## About
This is an implementation of the neural network proposed in [Learning Efficient Illumination Multiplexing for Joint Capture of Reflectance and Shape](http://www.cad.zju.edu.cn/home/hwu/publications/jointcap/project.html).

## Usage
### System Requirements
- Windows or Linux(The codes are validated on Win10, Ubuntu 18.04 and Ubuntu 16.04)
- Python>=3.6
- tensorflow>=1.11.0
- numpy
- opencv-python

Note: Since the training data (sampled points with BRDF parameters and position) are generated by an exe module, you may need a windows platform to generate training data.

### Training
Windows: 
1. move to siga19_source 
2. run train.bat  
  
Linux: 
1. move to siga19_source 
2. change DATA_ROOT in train.sh to the path of training data. 
3. run train.sh

**About Synthetic Data Genration**:

A lumitexel is generated from parameters of a sampled point, including BRDF parameters(normal, tangent, axay, rhod, rhos) and position. The exe module is for generating sampled points, which will be stored in the training data path.(claimed in the train.bat) So you need to generate sampled points on windows first. With a tensorflow implemented rendering module, the lumitexels will be rendered on the fly using the parameters. You can find the module in siga19_source/auxiliary/tf_ggx_render_newparam/tf_ggx_render.py. The configuration of setup(lights,cameras...) is passed to this module when constructing a renderer. It worth noting that you also need to make a uniformly sampled light configuration of the setup to avoid the drawback of real setup as we noted in the paper.

### Training Log & Model
When training is started, a log folder will be generated. You may run tensorboard to check training logs.  
The test sample will be shown in the images tab in the order of:  
input lumitexel, predicted diffuse lumitexel, ground truth diffuse lumitexel, ground truth specular lumitexel, predicted specular lumitexel  
Trained lighting pattern can also be found in the images tab.  
Trained model will be save in the created save folder.  

## License

Our source code is released under the GPL-3.0 license for acadmic purposes. The only requirement for using the code in your research is to cite our paper:

    @article{Kang:2019:JOINT,
    author = {Kang, Kaizhang and Xie, Cihui and He, Chengan and Yi, Mingqi and Gu, Minyi and Chen, Zimin and Zhou, Kun and Wu, Hongzhi},
    title = {Learning Efficient Illumination Multiplexing for Joint Capture of Reflectance and Shape},
    journal = {ACM Trans. Graph.},
    issue_date = {November 2019},
    volume = {38},
    number = {6},
    month = nov,
    year = {2019},
    issn = {0730-0301},
    pages = {165:1--165:12},
    articleno = {165},
    numpages = {12},
    url = {http://doi.acm.org/10.1145/3355089.3356492},
    doi = {10.1145/3355089.3356492},
    acmid = {3356492},
    publisher = {ACM},
    address = {New York, NY, USA},
    keywords = {SVBRDF, lighting patterns, multi-view stereo, optimal sampling},
    } 

For commercial licensing options, please email hwu at acm.org.   
See COPYING for the open source license.
