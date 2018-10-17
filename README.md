# database_GUI

A project that builds a NoSQL database from CSV or Excel files and dynamically creates a GUI to filter, visualise and interact with the database contents.

  - Automate the read of data from CSV, text, JSON or Excel files.
  - Create a searchable NoSQL databases that can be distributed to the cloud for accessibility and scalability.
  - Launch an interactive GUI that dynamically adapts to the fields and contents of your database.
  - Filter the contents of your database and produce interactive visualisations of the contents of your database.

A short presentation on the design of the database_GUI is avaialbe [here].



### Tech
* [React.js] - A JavaScript library for building user interfaces
* [Plotly] - Modern Visualization for the Data Era
* [MongoDB] - NoSQL database with JSON-like documents
* [Python] - Programming that lets you work quickly and easily integrate systems  

### Installation

You will need to install MongoDB by following their instructions https://docs.mongodb.com/manual/administration/install-community/

Then NPM, react and python libraries will all need installing. Here are the required commands for Ubuntu.


```

git clone https://github.com/Shimwell/database_GUI.git

cd database_GUI

$ curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -

$ sudo apt-get install -y nodejs

sudo apt-get install -y build-essential

npm install
npm install bootstrap --save
npm install --save reactstrap react react-dom
npm install react-table
npm install react-select
npm install reactstrap
npm install react-plotly.js plotly.js
npm install --save rc-slider

pip install -r requirements

```

### Getting started

Launch the MongoDB client

```
sudo mongodb
```


Create a demonstration database, the create_database.py file shows you how to make a database using them dummy data provided in this repository.

```
cd  database_creation_tools
python create_database.py

```

Launch the RESTfull API which allows the GUI to interact with the database.

```
python rest_api_database_functions.py
```

Launch the database GUI using npm from the root folder of the repository

```
cd ..
npm start
```

At this stage your web browser should load and you should be able to use and interact with the GUI. If not try navigating to http://localhost:3000/


[here]: <https://slides.com/shimwell/database_gui#/>
