# MatFlow software

MatFlow is a very strong option if your machine learning process is very iterative and you need an all-in-one solution to automate your machine learning workflows and profit off of clever add-ons. It is built on top of [Apache Airflow](https://airflow.apache.org). <br/>
You can code up your DAGs for airflow in the browser and can create templates of these DAGs to increase usability. This makes sense if you have a general workflow without specific data and want to reuse trhat construct. <br/>If you wish to actually run these DAGs with config files, you can create workflow instances of your template DAG. That way, you can run workflows without having to manually upload the desired config files with the push of a button. <br/> If you now wish to experiment and finetune your workflows, e.g. experiment with a certain parameter, you can use Matflow's version control. This works just like Git and enables you to revisit older states of your config files and load them into your current workflow instance. A key advantage of this is being able to efficiently experiment with your DAGs without having to worry about "losing" past progress or backing up old data. <br/>
Another massive advantage is that you can collaboratively work on the same DAGs and projects because all templates and workflow instances are kept in a shared database on the server and can be accessed by every eligible team member. You can also upload local files into the system to make them available to your team members. <br/>
MatFlow also extends the admin's abilities by adding a hardware administration for the server and an extended user administration to what airflow already provides.<br/>
For some machine learning tasks, DAGs might not be the best way to go. That's why we are providing a custom operator called the AlternatingOperator. This operator executes a given amount of tasks in a LOOP for either a set amount of times or until a certain condition is met, e.g. machine learning model has > 0.9 performance on a validation set.




## Technolgies used

This project is built using
* Python
    * Flask
    * Apache Airflow
* TypeScript
* MySQL
* Docker



## Installation
MatFlow is implemented as a client-server application.On the server, you need to have npm, Docker and python(more specifically, pip) installed.

**Client application**<br>
Run client application:
```
http://<Server IP>:8080
```

**Server application** <br>
Install server application dependencies:
```
pip install -r requirements.txt
npm install
```
This creates a virtualenv environment. If you want to use a pipenv environment instead, replace pip with pipenv in the commands above.  <br><br/>
Run server application:
```
npm run serve -- --port 8081
docker-compose up
python3 -m matflow.main
```

## Testing
**Client application**<br>
Run unit-tests:
```
npm run test:unit
```

## Credits
MatFlow was developed for the Karlsruher Institut für Technolgie by Florian Küfner, Soeren Raymond, Alessandro Santospirito, Lukas Wilhelm and Nils Wolters. If you wish to further develop this project, please be so kind as to mention us. Thanks!

