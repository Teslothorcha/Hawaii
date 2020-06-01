#  Hawaii challenge!

This REST api wast build with **flask-restful**. This api serves information about specific stations that gather information about precipitation data on Hawaii, 


# Installation

clone this repo 

$ <code>git clone https://github.com/Teslothorcha/Hawaii.git</code>

Enter hawaii dir

$ <code>cd hawaii</code>

create a virtaual-env

$ <code>virtualenv hawaii-env</code>

Activate virtualenv

$ <code>source hawaii-env/bin/activate</code>

You will see your terminal like this

<code>(hawaii-env)$ </code>

Install all the requirements

<code>(hawaii-env)$pip install -r requirements.txt </code>

Set env variables

<code>(hawaii-env)$export FLASK\_DEBUG=1 </code>

<code>(hawaii-env)$export FLASK_APP=run.py </code>

Run it
<code>(hawaii-env)$flask run </code>

# Routes

/api/v1.0/precipitation

/api/v1.0/stations

/api/v1.0/tobs

/api/v1.0/{start}/

/api/v1.0/{start}/{end}

/pandas

/api/v1.0/api/spec.html

# Optional

Los retos opcionales fueron solucionados con jupyter-noteboook y pandas, se encuentran en el archivo

<code>hawaii_precipitation.ipynb </code>

Juan David Marin Bernal