# AdMetricks Test Technical Uf web-scraping
This project was developed with the purpose of demonstrating the technical knowledge acquired during my work experience. To this end, I have developed a API REST in [DRF](), which allows to obtain the value of the daily UF, through the use of scraping techniques from the website of the [central bank]()

##Getting Started

### Prerequisiter
Before install this project, you need install some software:

On Ubuntu you can install with the next command
```
$ sudo apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
```

On Mac OS X, you can use Homebrew to install QT and easy_install to pip.
```
# brew install qt
# easy_install pip
```
 
 
On other operating systems, you can use pip to install lxml.
 
### Installing
First, you get a copy of project using Git:

```
$ git clone https://github.com/Jkaiser001/AdMetricks_Test_Technical_Uf_web-scraping.git Admetricks_test_technical
$ cd Admetricks_test_technical
```
After, create a new virtual environment, using [virtualenv]()

```
virtualenv env
source env/bin/activate
```

Now, you need install requirements of project by using pip.
```
pip install -r requirements.txt
```

## Deployment

## Built With

* [DjangoRestFramework]() - The web framework used
* [](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Author

* **José Orellana** - [Jkaiser001](https://github.com/Jkaiser001)
