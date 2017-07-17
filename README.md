# Exoviz

   Exoviz is a 2.7 python program, which creates sql lite database and fills it with data from the Open Exoplanet Catalogue. https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue. It preserves relations between the bodies in systems by separating system, star , binary, planet data in 4 tables related with foreign keys.
   The Exoviz a Flask application and a web front-end interface to provide a visualisation for each planet system . File "models.py" contains all the tags for each model and you can freely remove some of them or add yours then build your own database with data you need for the specific calculations, a game  or a personal web page.

![alt tag](http://i63.tinypic.com/2elggmd.jpg)


###Used python modules:
  - lxml
  - peewee
  - flask
  - apscheduler
  - logging


### Version
0.1.3 (Alpha)

### Issues
-  Update issue (sometimes flask app crashes while autoupdating) 


### Installation

Tested with Ubuntu 14.4

Before launching this program please make sure you have done the following preparations:

1) Install python 2.7 on your system . https://www.python.org/downloads/

2) Exoscanner is a python 2.7 code. It uses some modules which are not included in the standart python package. You have to install them manualy with pip.

```sh
$ sudo apt-get install python-pip 
```

```sh
$ pip install peewee
$ pip install lxml
$ pip install flask
$ pip install apscheduler


```
3) Download Exoviz folder or clone it with git on your computer. 


4) Download data from The OEC and build the sql lite database :
	go to EXOVIZ folder in the terminal and type : 
```sh
$ python control.py 
```
chose "create database" option
Wait ubntil it is done and exits then launch the main app


```sh
$ python flask1.py 
```

5) Check it out in your browser by typing http:/localhost:8080

### Development

- better update algoritm (in progress)
- advanced logging  (in progress)



**Contacts**

- [Yury Milto]  ymilto@gmail.com
