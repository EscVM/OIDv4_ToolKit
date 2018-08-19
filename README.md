# OIDv4 ToolKit for Object Detection

Do you want to build your personal object detector but you don't have enough images to train your model? Have you already discovered [Open Images Dataset v4](https://storage.googleapis.com/openimages/web/index.html) that has [600](https://storage.googleapis.com/openimages/2018_04/bbox_labels_600_hierarchy_visualizer/circle.html) classes and more than 1,700,000 images ready to use? Do you want to exploit it for your projects but you don't want to download 18 TB of data?

With this repository we can help you to get the best of this dataset with less effort as possible.
In particular, with this practical toolkit written in Python3 we give you the following options:

* download any class of the dataset individually, taking care of creating the related bounding boxes for each downloaded image
* download multiple classes at the same time creating separated folder and bounding boxes for each of them
* download multiple classes and creating a common folder for all of them with a unique annotation file of each image
* download a single class or multiple classes with the desired [attributes](https://storage.googleapis.com/openimages/web/download.html)
* use the practical visualizer to inspect the donwloaded classes

The code is quite documented and designed to be easy to extend and improve. 
Me and [Angelo](https://github.com/keldrom) are pleased if our little bit of code can help you with your project and research. Enjoy ;)

![Snippet of the OIDv4 available classes](images/classes.png)

# Open Image Dataset v4
All the information related to this huge dataset can be found [here](https://storage.googleapis.com/openimages/web/index.html)
In these few lines are simply summarized some statistics and important tips.

<table>
    <tr><td></td><td><b>Train<b></td><td><b>Validation<b></td><td><b>Test<b></td><td><b>#Classes<b></td></tr>
    <tr><td>Images</td><td>1,743,042</td><td>41,620	</td><td>125,436</td><td>-</td></tr>
    <tr><td>Boxes</td><td>14,610,229</td><td>204,621</td><td>625,282</td><td>600</td></tr>
</table>

As it's possible to observe from the previous table we can have access to images from free different groups: train, validation and test.
The toolkit provides a way to select only a specific group where to search.
It's important to underline that some annotations has been done as a group. It means that a single bounding box groups more than one istance. As mentioned by the creator of the dataset:
- **IsGroupOf**: Indicates that the box spans a group of objects (e.g., a bed of flowers or a crowd of people). We asked annotators to use this tag for cases with more than 5 instances which are heavily occluding each other and are physically touching.
That's again an option of the toolkit that can be used to only grasp the desired images. 

Finally, it's interesting to notice that not all annotations has been produced by humans, but the creator also exploited an enhanced version of the method shown here reported [1](#reference)

# Getting Started

## Installation

Python3 is required.

1. Clone this repository
   ```bash
   git clone https://github.com/EscVM/OIDv4_ToolKit.git
   ```
2. Install the required packages
   ```bash
   pip3 install -r requirements.txt
   ```
Peek inside the requirements file if you have everything already installed. Most of the dependencies are common libraries.

## Launch the toolkit to check the available options
First of all, if you simply want a quick reminder of al the possible options given by the script, you can simply launch, from your console of choice, the [main.py](main.py). Remember to point always at the main directory of the project
   ```bash
   python3 main.py
   ```
or in the following way to get more information
   ```bash
   python3 main.py -h
   ```
   
# Use the Toolkit to download
The toolkit permit the download of your dataset in the folder you want (`Dataset`as default). The folder can be imposed with the argument 
`--Dataset` so you can make different dataset with different options inside. Note: for class that is composed by different
words please use the `_` instead of the space; example: `Polar_bear`.
As previously mentioned, there are different available options that can be exploited. Let's see some of them.

## Download different classes in separated folders
Firstly, the toolkit can be used to download classes in separated folders. The argument `--classes` accepts a list of classes. We'd recommend you to set `--threads` to increase download speed.

Let's for example download Apples and Oranges from the validation set. In this case we have to use the following command.
  ```bash
   python3 main.py download --classes Apple Orange --type_csv validation --threads 50
   ```
The algorith will take care to download all the necessary files and build the directory structure like this:

```
main_folder 
│   main.py   
│
└───OID
    │   file011.txt
    │   file012.txt
    │
    └───csv_folder
    |    │   class-descriptions-boxable.csv
    |    │   validation-annotations-bbox.csv
    | 
    └───Dataset
        |   
        └─── test
        | 
        └─── train
        | 
        └─── validation
             | 
             └───Apple
             |     |
             |     |0fdea8a716155a8e.jpg
             |     |2fe4f21e409f0a56.jpg
             |     |...
             |     └───Labels
             |            |
             |            |0fdea8a716155a8e.txt
             |            |2fe4f21e409f0a56.txt
             |            |...
             | 
             └───Orange
                   |
                   |0b6f22bf3b586889.jpg
                   |0baea327f06f8afb.jpg
                   |...
                   └───Labels
                          |
                          |0b6f22bf3b586889.txt
                          |0baea327f06f8afb.txt
                          |...
```
If you have already downloaded the different csv files you can simply put them in the `csv_folder`. The script takes automatically care of the download of these files, but if you want to manually download them for whatever reason [here](https://storage.googleapis.com/openimages/web/download.html) you can find them.

If you interupt the downloading script `ctrl+d` you can always restart it from the last image downloaded.

### Annotations
In the original dataset the coordinates of the bounding boxes are made in the following way:

**XMin**, **XMax**, **YMin**, **YMax**: coordinates of the box, in normalized image coordinates. XMin is in [0,1], where 0 is the leftmost pixel, and 1 is the rightmost pixel in the image. Y coordinates go from the top pixel (0) to the bottom pixel (1).

However, in order to accomodate a more intuitive representation and give the maximum flexibility, every `.txt` annotation is made like:

`name_of_the_class    left    top     right     bottom`

### Optional Arguments
The annotations of the dataset has been marked with a bunch of boolean values. This attributes are reported below:
- **IsOccluded**: Indicates that the object is occluded by another object in the image.
- **IsTruncated**: Indicates that the object extends beyond the boundary of the image.
- **IsGroupOf**: Indicates that the box spans a group of objects (e.g., a bed of flowers or a crowd of people). We asked annotators to use this tag for cases with more than 5 instances which are heavily occluding each other and are physically touching.
- **IsDepiction**: Indicates that the object is a depiction (e.g., a cartoon or drawing of the object, not a real physical instance).
- **IsInside**: Indicates a picture taken from the inside of the object (e.g., a car interior or inside of a building).

Naturally, the toolkit provides the same options as paramenters in order to filter the downloaded images.
For example, with:
  ```bash
   python3 main.py download --classes Apple Orange --type_csv validation --image_IsGroupOf 0
   ```
only images without group annotations are downloaded.

## Download multiple classes in a common folder
This option allows to download more classes, but in a common folder. Also the related notations are mixed together with
 the already explained format (the first element is always the name of the single class). In this way, with a simple 
 dictionary it's easy to parse the generated label to get the desired format.

Again if we want to download Apple and Oranges, but in a common folder
  ```bash
   python3 main.py download --classes Apple Orange --type_csv validation --multiclasses 1
   ```
#Use the toolkit to visualize the labeled images
The toolkit is useful also for visualize the downloaded images with the respective labels.
```bash
   python3 main.py visualize 
   ```
  In this way the default `Dataset` folder will be pointed to search the images and labels automatically. To point
  another folder it's possible to use `--Dataset` optional argument.
```bash
   python3 main.py visualize --Dataset desired_folder 
   ```
Then the system will ask you what folder visualize (train, validation or test) and the class.
Hence with `d` (next), `a` (previous) and `w` (exit) you will be able to explore all the images.
## Citation
Use this bibtex if you want to cite this repository:
```
@misc{OIDv4_ToolKit,
  title={Toolkit to download and visualize single or multiple classes from the huge Open Images v4 dataset},
  author={Vittorio, Angelo},
  year={2018},
  publisher={Github},
  journal={GitHub repository},
  howpublished={\url{https://github.com/EscVM/OIDv4_ToolKit}},
}
```

# Reference
"[We don't need no bounding-boxes: Training object class detectors using only human verification](https://arxiv.org/abs/1602.08405)"Papadopolous et al., CVPR 2016.
