# Sentinel Image Merger

## Requirements
- Python 3.x
- Virtual Environment

## Run 

```
$ (env) pip install -r requirements.txt
$ (env) python run.py
```

### Install GDAL in linux:


```
sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt-get install libgdal-dev
sudo apt-get install python-dev
sudo apt-get install gdal-bin python-gdal python3-gdal
pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
```

### Install GDAL in Windows:

![](https://media.tenor.com/images/99604b5b517a368cbffcecaeaf9546a0/tenor.gif)