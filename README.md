# AdMetricks Test Technical UF web-scraping
This project was developed with the purpose of demonstrating the technical knowledge acquired during my work experience. To this aim, I have developed a API REST in [Django Rest Framework](http://www.django-rest-framework.org/), which allows to obtain the value of the daily UF, through the use of scraping techniques from the website of the [central bank](http://www.bcentral.cl/).


## Prerequisiter
Before install this project, you need install some software:

* [PIP](https://pypi.python.org/pypi/pip)
* [VIRTUALENV](https://virtualenv.pypa.io/en/stable/)
* [QT](https://www.qt.io)
* [lxml](http://lxml.de)
* [xvfb_](/)(nescessary only if no X server is available)


On Ubuntu you can install with the next command
```
$ sudo apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
$ sudo pip install virtualenv
```

On Mac OS X, you can use Homebrew to install QT and easy_install to pip.
```
$ brew install qt
$ easy_install pip
$ pip install virtualenv
```
 
On other operating systems, you can use pip to install lxml.
 
## Installing

First, you get a copy of project using Git:
```
$ git clone https://github.com/Jkaiser001/AdMetricks_Test_Technical_Uf_web-scraping.git Admetricks_test_technical
$ cd Admetricks_test_technical
```

After, create a new virtual environment, using [virtualenv](https://pypi.python.org/pypi/virtualenv)

```
$ virtualenv env
$ source env/bin/activate
```

Now, you need install requirements of project by using pip.

```
$ pip install -r requirements.txt
```
### Docker Instructions

Ensure Docker is installed on your system

First, you get opy of project using Git:
```
$ git clone https://github.com/Jkaiser001/AdMetricks_Test_Technical_Uf_web-scraping.git Admetricks_test_technical
$ cd Admetricks_test_technical
```

Give execute permission to file run.sh and execute:
```
$ chmod +x run.sh
$ sh run.sh
```

The initial run may take several minutes to build. Once complete, the application will be available at http://localhost:8080


## Getting Started

For start de project you need activate the virtualenv and execute manage with runserver.


```
$ source env/bin/activate
$ python manage.py runserver
```

Then, on your local machine, the server will be available at url http://127.0.0.1:8000/, where you can see a documentation simple in [Swagger](https://swagger.io/).


## Deployment

### Built With

* [DjangoRestFramework](http://www.django-rest-framework.org/) - The web framework 
* [VirtualEnv](https://pypi.python.org/pypi/virtualenv) - Virtual enveroment
* [Dryscrape](http://dryscrape.readthedocs.io/en/latest/index.html) - For scraping


## Author

* **José Orellana** - [Jkaiser001](https://github.com/Jkaiser001)
