import ConfigFile from '@Classes/ConfigFile';
import User from '@Classes/User';
import Server from '@Classes/Server';
import Version from '@Classes/Version';
import Template from '@Classes/Template';
import { fileToDataURL } from '@Classes/base64Utility';
import Keys from '@Controler/Keys';

/* eslint-disable */

import {
  versions, users, deleteUser, updateUser, pushServer,
} from '../DummyData/DataInTypscript';

const axios = require('axios').default;

type workflowInstanceNameAsString = keyof typeof versions

class BackendServerCommunicator {
    static serverAddress = 'http://127.0.0.1:5000/'

    // (Florian) logIn of airflow is used
    // public pushLogIn(userName: string, userPassword: string): void { return }

    public pushSignUp(userName: string, userPassword: string, userPasswordRepeated: string): void {
      axios.post(BackendServerCommunicator.serverAddress + Keys.registerUser, {
        [Keys.userName]: userName,
        [Keys.passwordName]: userPassword,
        [Keys.repeatPasswordName]: userPasswordRepeated,
      })
        .then((response) => {
          switch (response.data[Keys.statusCodeName]) {
            case 607:
              // everything went fine
              break;
            case 601:
              // username already exists
              break;
            case 610:
              // sign up exception - i don't really know what that means
              break;
            case 611:
              // converter in backend failed
              break;
            case 612:
              // airflow connection exception
              break;
            case 666:
              // something went wrong in the backend internally
              break;
            default:
              // should not occur, maybe print status code
              break;
          }
        })
        .catch((error) => {
          // transfer error
        });
    }

    // public pullGraphForTemporaryTemplate(tempTemplate: Template): File { return }

    public pushCreateTemplate(template: Template): void {
      // encode the dag file
      const encoded_file: string = fileToDataURL(new File([], 'emptyFile.py')); // TODO dummy file
      const config = {
        headers: {
          'Content-Type': 'application/json',
        },
      };
      const data = {
        [Keys.templateName]: template.templateName,
        [Keys.dagDefinitionName]: 'dummyName.py', // TODO dummy file name
        [Keys.fileKey]: encoded_file,
      };

      axios.post(BackendServerCommunicator.serverAddress + Keys.createTemplate, data, config)
        .then((response) => {
          console.log('pushTemplateResp', response);
          switch (response.data[Keys.statusCodeName]) {
            case 607:
              // everything went fine
              break;
            case 602:
              // template name already exists
              break;
            case 603:
              // invalid dag file
              break;
            case 611:
              // converter in backend failed
              break;
            case 666:
              // something went wrong in the backend internally
              break;
            default:
              // should not occur, maybe print status code
              break;
          }
        })
        .catch((error) => {
          // transfer error
        });
    }

    // TODO the workflowInstance object doesn't contain the conf folder
    public pushCreateWorkflowInstanceFromTemplate(workflowInstanceName: string, templateName: string, zippedConfFiles: File): void {
      const encoded_zip_file = fileToDataURL(new File([], 'emptyFile.py'));
      axios.post(BackendServerCommunicator.serverAddress + Keys.createWfInstance, {
        [Keys.workflowInstanceName]: workflowInstanceName,
        [Keys.templateName]: templateName,
        [Keys.configFiles]: encoded_zip_file,
      })
        .then((response) => {
          switch (response.data[Keys.statusCodeName]) {
            case 607:
              // everything went fine
              break;
            default:
              // error -> can be
              break;
          }
        });
    }

    // TODO Either unzip in frontend or create new api call
    public pushExistingWorkflowInstance(workflowInstanceAsZip: File): void { }

    public async pullTemplatesName(): Promise<string[]> {
      let templateNames: string[] = [];
      await axios.get(BackendServerCommunicator.serverAddress + Keys.getAllTemplateNames)
        .then((response) => {
          const { data } = response;
          if (data[Keys.statusCodeName] == 607) {
            templateNames = data[Keys.templateNames];
          } else {
            // error occurred
          }
        });
      return templateNames;
    }

    // public pullTemplateWithName(templateName: string): Template { return }

    public async pullWorkflowInstancesNameAndConfigFilesName(): Promise<Array<[string, string[]]>> {
      const result: Array<[string, string[]]> = [];
      await axios.get(BackendServerCommunicator.serverAddress + Keys.getAllWfInstancesNamesAndConfigFileNames)
        .then((response) => {
          // console.log(response)
          const { data } = response;
          if (data[Keys.statusCodeName] == 607) {
            for (const wf_name in data[Keys.namesAndConfigs]) {
              const conf_files = data[Keys.namesAndConfigs][wf_name];
              result.push([wf_name, conf_files]);
            }
          } else {
            // error occurred
          }
        });
      return result;
    }

    public async pullConfigFileWithConfigFileNameWithWorkflowInstanceName(workflowInstanceName: string, configFileName: string): Promise<ConfigFile> {
      let conf_file: ConfigFile = new ConfigFile(); // initialize variable as "empty" config file
      await axios.get(BackendServerCommunicator.serverAddress + Keys.getConfigFromWfInstance)
        .then((response) => {
          // console.log(response)
          const { data } = response;
          if (data[Keys.statusCodeName] == 607) {
            conf_file = new ConfigFile(data[Keys.configFileName], data[Keys.keyValuePairsName]);
          } else {
            // error occurred
          }
        });
      return conf_file;
    }

    public pushConfigFilesWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void {
      const configDicts: Array<Object> = [];
      configFiles.forEach(file => {
        configDicts.push({
          [Keys.configFileName]: file.configFileName,
          [Keys.keyValuePairsName]: file.keyValuePairs,
        });
      })
      axios.post(BackendServerCommunicator.serverAddress + Keys.createVersionOfWfInstance, {
        [Keys.workflowInstanceName]: workflowInstanceName,
        [Keys.versionNoteName]: '',
        [Keys.configFiles]: configDicts,
      })
        .then((response) => {
          switch (response.data[Keys.statusCodeName]) {
            case 607:
              // everything went fine
              break;
            default:
              // error -> can be
              break;
          }
        });
    }

    public async pullVersionsWithWorkflowInstanceName(workflowInstanceName: workflowInstanceNameAsString): Promise<Version[]> {
      const versions: Version[] = [];
      await axios.get(BackendServerCommunicator.serverAddress + Keys.getWfInstanceVersions)
        .then((response) => {
          // console.log(response)
          const { data } = response;
          if (data[Keys.statusCodeName] == 607) {
            for (const versionDict of data[Keys.versionsName]) {
              const versionNum: string = versionDict[Keys.versionNumberName];
              const versionNote: string = versionDict[Keys.versionNoteName];
              const changes: Array<[string, string]> = [];
              for (const change of versionDict[Keys.frontendVersionsChanges]) {
                changes.push([`${change[Keys.oldKey]}: ${change[Keys.oldValue]}`, `${change[Keys.newKey]}: ${change[Keys.newValue]}`]);
              }
              versions.push(new Version(versionNum, versionNote, changes));
            }
          } else {
            // error occurred
          }
        });
      return versions;
    }

    public pushReplaceActiveVersionOfWorkflowInstance(workflowInstanceName: string, versionNumber: string): void {
      axios.put(BackendServerCommunicator.serverAddress + Keys.replaceWfInstanceVersion, {
        [Keys.workflowInstanceName]: workflowInstanceName,
        [Keys.versionNumberName]: versionNumber,
      })
        .then((response) => {
          switch (response.data[Keys.statusCodeName]) {
            case 607:
              // everything went fine
              break;
            default:
              // error -> can be
              break;
          }
        });
    }

    public async pullUsers(): Promise<User[]> {
      const tempUsers: User[] = [];
      users.forEach((user: User) => {
        tempUsers.push(new User(user.userName, user.userStatus, user.userPrivilege));
      });
      return new Promise((res, rej) => res([new User('name1', 'suspended', 'administrator')]))
      // return tempUsers;
    }

    public pushUser(user: User): void { updateUser(user); }

    public pushDeleteUser(user: User): void { deleteUser(user); }

    public async pullServers(): Promise<Server[]> {
      let servers: Server[] = [];
      await axios.get('http://localhost:5000/get_server_details')
        .then((response) => {
          console.log(response);
          const { data } = response;
          servers = [new Server(data.serverAddress, 'running', data.containerLimit, data.selectedForExecution, data.serverName, [['cpu1', '50%']])];
        });
      return servers;
      // funktioniert. Es sind aber dummy daten
      // return pullServers2()
    }

    public pushServer(server: Server): void { pushServer(server); }

    private encode_file(file: File): string { return ''; } // TODO
}

export default BackendServerCommunicator;
