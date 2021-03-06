USE mysql;
GRANT ALL PRIVILEGES ON matflowDatabase.* TO 'matflowUser'@'%';
USE matflowDatabase;
CREATE TABLE IF NOT EXISTS Server (
   ip varchar(50) NOT NULL,
   name varchar(255) NOT NULL,
   PRIMARY KEY (ip)
);

CREATE TABLE IF NOT EXISTS WorkflowTemplate (
   template_ID INTEGER AUTO_INCREMENT,
   name varchar(255),
   dag varchar(255),
   PRIMARY KEY (template_ID)
);

CREATE TABLE IF NOT EXISTS Workflow (
   name varchar(255),
   dag varchar(255) NOT NULL,
   PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS FolderFile (
   wfName varchar(255),
   fileID INTEGER AUTO_INCREMENT,
   file varchar(255),
   PRIMARY KEY (fileID),
   FOREIGN KEY (wfname) REFERENCES Workflow(name)
);

CREATE TABLE IF NOT EXISTS Version (
   ID INTEGER AUTO_INCREMENT,
   wfName varchar(255) NOT NULL,
   version varchar(127) NOT NULL,
   note varchar(1000),
   PRIMARY KEY (ID),
   FOREIGN KEY (wfName) REFERENCES Workflow(name)
);

CREATE TABLE IF NOT EXISTS ActiveVersion (
   wfName varchar(255),
   version varchar(127) NOT NULL,
   PRIMARY KEY (wfName),
   FOREIGN KEY (wfName) REFERENCES Workflow(name)
);

CREATE TABLE IF NOT EXISTS ConfFile (
   confKey INTEGER NOT NULL AUTO_INCREMENT,
   file varchar(255) NOT NULL,
   PRIMARY KEY (confKey)
);

CREATE TABLE IF NOT EXISTS VersionFile (
   versionID INTEGER,
   filename varchar(255),
   confKey INTEGER NOT NULL,
   PRIMARY KEY (versionID, filename),
   FOREIGN KEY (versionID) REFERENCES Version(ID),
   FOREIGN KEY (confKey) REFERENCES ConfFile(confKey)
);

CREATE TABLE IF NOT EXISTS ResultFile (
   fileID INTEGER NOT NULL AUTO_INCREMENT,
   versionID INTEGER,
   file varchar(255),
   PRIMARY KEY (fileID),
   FOREIGN KEY (versionID) REFERENCES Version(ID)
);