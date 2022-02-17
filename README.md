# MatFlow software

MatFlow is an application that automates and organizizes material simulations and postprocessing.
It enables Machine Learning engineers to automate their workflow. See more about [airflow](https://airflow.apache.org). <br/>
This software extends Apache Airflow by adding hardware and software administration and an in-browser code editor. 
MatFlow is a very strong option if your machine learning process is very iterative and you need an all-in-one solution:
You can code, develop and run your workflows in MatFlow and benefit from the seamless integration with Apache Airflow.



## Technolgies used

This project is built using
* Python
    * Flask
    * Apache Airflow
* TypeScript
* MySQL
* Nomad 
* Docker



## Installation
MatFlow is implemented as a client-server application, thus having two seperate installation guides.
You need to have npm and python(more specifically, pip) installed.

**Client application**
Install client application dependencies:
```
npm install
```
Run client application:
```
npm run serve
```

**Server application**
Install server application dependencies:
```
pip install -r requirements.txt
```
Run server application:
```
nomad job run matflow_nomad.hcl
```



## Credits
MatFlow was developed for the Karlsruher Institut für Technolgie by Florian Küfner, Soeren Raymond, Alessandro Santospirito, Lukas Wilhelm and Nils Wolters.

