# IstoryA-project- Annual project ESGI 5IABD
This project is a school project for ESGI (Paris).

The aim of this project, is to create a website where user can generate a story, then generate images from this story and finaly build a Storyboard with text and image.

This project is hosted on an Html/Css Website, and available on AWS at this adress :  http://13.37.83.253/

## Architecture & Code :
This repo contains Website source code, datasets, exploration notebooks and flask server root config 

#### Fonctionnal Application :

 
![](img/Functional_Scheme.png)
***********************************


#### Technical Local Architecture :


![](img/Technical_Local_Architecture.png)
***********************************


#### Technical Cloud Architecture


![](img/Technical_Cloud_Architecture.png )
***********************************

## How to run :

### Website environment & text generation (Django)

> After downloading the repository, it is important to create a **python environment** to the root project: ```python3 -m venv .venv```.

> **Update** your python package manager (pip): ```pip install --upgrade pip```

> Download all the Django **requirements** with the following: ```pip install -r /IstoryA-project/IstoryA-Frontend/requirements.txt```

> After installing the NLP library NLTK, you have to download the **necessaries packages**: ```python -m nltk.downloader popular```

> Then you have to set up the **SQlite database**: ```python manage.py makemigrations main``` and finish by creating the database: ```python manage.py migrate```

> Please check that your local IP or your server IP is in the ALLOWED_HOSTS in the file: ```/IstoryA-project/IstoryA-Frontend/IstoryA/settings.py```

> To launch Django server you just have to enter the following command: ```python manage.py runserver 0.0.0.0:80```

### Image generation (Flask)

> Download all the front **requirements** with the following: ```pip install -r IstoryA-project/Image-generator-server/requirements.txt```

> Expose to PATH environment Flask app: ```export FLASK_APP=flask-server.py```

> To launch Flask server you just have to enter the following command: ```flask run --host=0.0.0.0```

## Authors : 
<p>Clément Delaunay (https://github.com/Koneko76)</p>
<p>Florian Bergeron (https://github.com/FlorianBergeron)</p>
<p>Clément Depraz (https://github.com/clement-depraz)</p>
<p>Mathias Gianotti (https://github.com/Mathiris)</p>
