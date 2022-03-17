/* eslint-disable */
import ConfigFile from '@Classes/ConfigFile';
import User from '@Classes/User';
import Server from '@Classes/Server';
import Version from '@Classes/Version';
import Template from '@Classes/Template';
import { fileToDataURL, dataURLtoFile } from '@Classes/base64Utility';
import Keys from '@Controler/Keys';
import UserData from '@Classes/UserData';
import WorkflowInstance from '@Classes/WorkflowInstance';
import user from '@Classes/User';
import {
  templateNames, workflowInstancesNameAndConfigFilesName, setWfConf, getWfConf, versions, users, deleteUser, updateUser, pullServers2, pushServer,
} from '../DummyData/DataInTypscript';

const axios = require('axios').default;
const userDataObject = new UserData('','')

type workflowInstanceNameAsString = keyof typeof versions

class BackendServerCommunicator {
    static serverAddress = 'http://127.0.0.1:8082/'

    public constructor() { }

    // (Florian) logIn of airflow is used
    // public pushLogIn(userName: string, userPassword: string): void { return }

    public pushSignUp(userName: string, userPassword: string, userPasswordRepeated: string): void {
      axios.post(BackendServerCommunicator.serverAddress + Keys.registerUser, {
        [Keys.userName]: userName,
        [Keys.passwordName]: userPassword,
        [Keys.repeatPasswordName]: userPasswordRepeated,
      }, {auth: {
        username: userDataObject.userName,
        password: userDataObject.userPassword
      }})
        .then((response) => {
          console.log('sign up resp: ', response);
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

    //TODO pullTemplateByName
    public async pullDagFileByTemplateName(worflowInstanceName: string): Promise<File>{
      return dataURLtoFile("", ""); //dummy
    }

    // TODO the workflowInstance object doesn't contain the conf folder
    public pushCreateWorkflowInstanceFromTemplate(
      workflowInstanceName: string,
      templateName: string,
      confFiles: File[],
    ): void {
      const confFilesDummy: File[] = [new File([], 'emptyFile.conf')];
      const confDict: Array<Object> = [];
      for (const file of confFilesDummy) {
        confDict.push({
          [Keys.configFileName]: file.name,
          [Keys.fileKey]: fileToDataURL(file),
        });
      }
      axios.post(BackendServerCommunicator.serverAddress + Keys.createWfInstance, {
        [Keys.workflowInstanceName]: workflowInstanceName,
        [Keys.templateName]: templateName,
        [Keys.configFiles]: confDict,
      })
        .then((response) => {
          console.log('createInstanceResp', response);
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
          console.log('pullTempNames', response);
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
          console.log('pullInstancesAndConf', response);
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
      let confFile: ConfigFile = new ConfigFile(); // initialize variable as "empty" config file
      const data = {
        [Keys.workflowInstanceName]: workflowInstanceName,
        [Keys.configFileName]: configFileName,
      };
      await axios.post(BackendServerCommunicator.serverAddress + Keys.getConfigFromWfInstance, data)
        .then((response) => {
          console.log('pullConfResp', response);
          const { data } = response;
          if (data[Keys.statusCodeName] == 607) {
            confFile = new ConfigFile(data[Keys.configFileName], data[Keys.keyValuePairsName]);
          } else {
            // error occurred
          }
        })
        .catch((error) => {
          console.log(error);
        });
      return confFile;
    }

    public pushConfigFilesWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void {
      const configDicts: Array<Object> = [];
      configFiles.forEach((file) => {
        configDicts.push({
          [Keys.configFileName]: file.configFileName,
          [Keys.keyValuePairsName]: file.keyValuePairs,
        });
      });
      axios.post(BackendServerCommunicator.serverAddress + Keys.createVersionOfWfInstance, {
        [Keys.workflowInstanceName]: workflowInstanceName,
        [Keys.versionNoteName]: '',
        [Keys.configFiles]: configDicts,
      })
        .then((response) => {
            console.log("createVersionResp", response);
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

    public async pullVersionsWithWorkflowInstanceName(workflowInstanceName: string): Promise<Version[]> {
      const versions: Version[] = [];
      await axios.post(BackendServerCommunicator.serverAddress + Keys.getWfInstanceVersions, {[Keys.workflowInstanceName]: workflowInstanceName})
        .then((response) => {
          console.log('pullversions', response);
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
            console.log("pushReplVersionResp", response);
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
      console.log("userDataObj", userDataObject)
      await axios.get(BackendServerCommunicator.serverAddress + Keys.getAllUsersAndDetails, {auth: {
        username: userDataObject.userName,
        password: userDataObject.userPassword
      }})
        .then((response) => {
          console.log('get_users_resp', response);
          const { data } = response;
          if (data[Keys.statusCodeName] == 607) {
            const user_dicts = data[Keys.allUsers];
            for (const dict of user_dicts) {
              tempUsers.push(new User(dict[Keys.userName], dict[Keys.userStatusName], dict[Keys.userPrivilegeName]));
            }
          } else {
            // error occurred
          }
        });
      return tempUsers;
    }

    public pushUser(user: User): void {
      axios.put(BackendServerCommunicator.serverAddress + Keys.setUserDetails, {
        [Keys.userName]: user.userName,
        [Keys.userStatusName]: user.userStatus,
        [Keys.userPrivilegeName]: user.userPrivilege,
        [Keys.passwordName]: 'airflow', // dummy_password
      }, {auth: {
        username: userDataObject.userName,
        password: userDataObject.userPassword
      }})
        .then((response) => {
          console.log('setUserResp:', response);
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

    public pushDeleteUser(user: User): void {
      const config = {
        headers: {
          'Content-Type': 'application/json',
        },
        data: {
          [Keys.userName]: user.userName,
          [Keys.userStatusName]: user.userStatus,
          [Keys.userPrivilegeName]: user.userPrivilege,
          [Keys.passwordName]: 'airflow', // dummy_password
        },
        auth: {
          username: userDataObject.userName,
          password: userDataObject.userPassword
        },
      };
      axios.delete(BackendServerCommunicator.serverAddress + Keys.deleteUser, config)
        .then((response) => {
          console.log('deleteUserResp:', response);
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

    public async pullServers(): Promise<Server[]> {
      let servers: Server[] = [];
      console.log("userDataObj", userDataObject)
      await axios.get(BackendServerCommunicator.serverAddress + Keys.getServerDetails, {auth: {
        username: userDataObject.userName,
        password: userDataObject.userPassword
      }})
        .then((response) => {
          console.log("PullServerResp", response);
          const { data } = response;
          let status: string;
          if (data[Keys.serverStatusName]) {
            status = 'running';
          } else {
            status = 'inactive';
          }
          servers = [new Server(data[Keys.serverAddressName], status, data[Keys.containerLimitName], data[Keys.selectedForExecutionName], data[Keys.serverName], [data[Keys.serverResourcesName]])];
          // servers = [new Server(data.serverAddress, 'running', data.containerLimit, data.selectedForExecution, data.serverName, [["cpu1", "50%"]])]
        });
      return servers;
      // funktioniert. Es sind aber dummy daten
      // return pullServers2()
    }

    public pushServer(server: Server): void {
      const data = {
        [Keys.serverName]: server.serverName,
        [Keys.serverAddressName]: server.serverAddress,
        [Keys.serverStatusName]: server.serverStatus,
        [Keys.containerLimitName]: server.containerLimit,
        [Keys.serverResourcesName]: server.serverResources[0],
        [Keys.selectedForExecutionName]: server.selectedForExecution,
        };
      axios.put(BackendServerCommunicator.serverAddress + Keys.setServerDetails, data, {auth: {
        username: userDataObject.userName,
        password: userDataObject.userPassword
      }})
        .then((response) => {
          console.log('pushServerResp:', response);
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

      public pushLogIn(userName: string, userPassword: string) {
        userDataObject.userName = userName
        userDataObject.userPassword = userPassword
        console.log("LoginResp", userName, userPassword)
      }
}

export default BackendServerCommunicator;
