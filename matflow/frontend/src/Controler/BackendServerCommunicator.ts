import ConfigFile from '@Classes/ConfigFile'
import User from '@Classes/User'
import Server from '@Classes/Server'
import Version from '@Classes/Version'
import Template from '@Classes/Template'
import {keys} from '@Controler/Keys';

import { templateNames, workflowInstancesNameAndConfigFilesName, setWfConf, getWfConf, versions, users, deleteUser, updateUser, pullServers2, pushServer } from '../DummyData/DataInTypscript'
import WorkflowInstance from '@Classes/WorkflowInstance'
import user from "@Classes/User";

const axios = require('axios').default;

type workflowInstanceNameAsString = keyof typeof versions

class BackendServerCommunicator {
    static serverAddress: string = 'http://127.0.0.1:5000/'

    public constructor() { }

    // (Florian) logIn of airflow is used
    // public pushLogIn(userName: string, userPassword: string): void { return }

    public pushSignUp(userName: string, userPassword: string, userPasswordRepeated: string): void {
        axios.post( BackendServerCommunicator.serverAddress + keys.registerUser, {
            [keys.userName]: userName,
            [keys.passwordName]: userPassword,
            [keys.repeatPasswordName]: userPasswordRepeated
        })
        .then(function (response) {
            switch (response.data[keys.statusCodeName]) {
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
        .catch(function (error) {
            // transfer error
        });
    }

    // public pullGraphForTemporaryTemplate(tempTemplate: Template): File { return }

    public pushCreateTemplate(template: Template): void {
        // encode the dag file
        let encoded_file = this.encode_file(template.dagDefinitionFile)
        axios.post( BackendServerCommunicator.serverAddress + keys.createTemplate, {
            [keys.templateName]: template.templateName,
            [keys.dagDefinitionName]: template.dagDefinitionFile.name,
            [keys.fileKey]: encoded_file
        })
        .then(function (response) {
            switch (response.data[keys.statusCodeName]) {
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
        .catch(function (error) {
            // transfer error
        });
    }

    // TODO the workflowInstance object doesn't contain the conf folder
    public pushCreateWorkflowInstanceFromTemplate(
        workflowInstanceName: string, templateName: string, zippedConfFiles: File): void {
        let encoded_zip_file = this.encode_file(new File([], "emptyFile"))
        axios.post( BackendServerCommunicator.serverAddress + keys.createWfInstance, {
            [keys.workflowInstanceName]: workflowInstanceName,
            [keys.templateName]: templateName,
            [keys.configFiles]: encoded_zip_file
        })
        .then(function (response) {
            switch (response.data[keys.statusCodeName]) {
                case 607:
                    // everything went fine
                    break;
                default:
                    // error -> can be
                    break;
            }
        })
    }

    // TODO Either unzip in frontend or create new api call
    public pushExistingWorkflowInstance(workflowInstanceAsZip: File): void { return }

    public async pullTemplatesName(): Promise<string[]> {
        let templateNames: string[] = []
        await axios.get(BackendServerCommunicator.serverAddress + keys.getAllTemplateNames)
        .then(function (response) {
            // console.log(response)
            // let data = response.data;
            if (response[keys.statusCodeName] == 607) {
                templateNames = response[keys.templateNames];
            } else {
                // error occurred
            }
        })
        console.log("hallo eine nachricht");
        console.log(templateNames);
        return templateNames;
        
    }

    // public pullTemplateWithName(templateName: string): Template { return }

    public async pullWorkflowInstancesNameAndConfigFilesName(): Promise<Array<[string, string[]]>> {
        let result: Array<[string, string[]]> = []
        await axios.get(BackendServerCommunicator.serverAddress + keys.getAllWfInstancesNamesAndConfigFileNames)
        .then(function (response) {
            // console.log(response)
            let data = response.data;
            if (data[keys.statusCodeName] == 607){
                for (let wf_name in data[keys.namesAndConfigs]) {
                    let conf_files = data[keys.namesAndConfigs][wf_name];
                    result.push([wf_name, conf_files]);
                }
            } else {
                // error occurred
            }
        })
        return result;
    }

    public async pullConfigFileWithConfigFileNameWithWorkflowInstanceName(workflowInstanceName: string, configFileName: string): Promise<ConfigFile> {
        let conf_file: ConfigFile = new ConfigFile(); // initialize variable as "empty" config file
        await axios.get(BackendServerCommunicator.serverAddress + keys.getConfigFromWfInstance)
        .then(function (response) {
            // console.log(response)
            let data = response.data;
            if (data[keys.statusCodeName] == 607) {
                conf_file = new ConfigFile(data[keys.configFileName], data[keys.keyValuePairsName]);
            } else {
                // error occurred
            }
        })
        return conf_file;
    }

    public pushConfigFilesWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void {
        let configDicts = [];
        for (let file of configFiles){
            configDicts.push({
                [keys.configFileName]: file.configFileName,
                [keys.keyValuePairsName]: file.keyValuePairs
            })
        }
        axios.post( BackendServerCommunicator.serverAddress + keys.createVersionOfWfInstance, {
            [keys.workflowInstanceName]: workflowInstanceName,
            [keys.versionNoteName]: "",
            [keys.configFiles]: configDicts
        })
        .then(function (response) {
            switch (response.data[keys.statusCodeName]) {
                case 607:
                    // everything went fine
                    break;
                default:
                    // error -> can be
                    break;
            }
        })
    }

    public async pullVersionsWithWorkflowInstanceName(workflowInstanceName: workflowInstanceNameAsString): Promise<Version[]> {
        let versions: Version[] = []
        await axios.get(BackendServerCommunicator.serverAddress + keys.getWfInstanceVersions)
        .then(function (response) {
            // console.log(response)
            let data = response.data;
            if (data[keys.statusCodeName] == 607) {
                for (let versionDict of data[keys.versionsName]){
                    let versionNum: string = versionDict[keys.versionNumberName];
                    let versionNote: string = versionDict[keys.versionNoteName];
                    let changes: Array<[string, string]> = [];
                    for (let change of versionDict[keys.frontendVersionsChanges]){
                        changes.push([change[keys.oldKey] + ": " +  change[keys.oldValue], change[keys.newKey] + ": " +  change[keys.newValue]]);
                    }
                    versions.push(new Version(versionNum, versionNote, changes));
                }
            } else {
                // error occurred
            }
        })
        return versions;
    }

    public pushReplaceActiveVersionOfWorkflowInstance(workflowInstanceName: string, versionNumber: string): void {
        axios.put( BackendServerCommunicator.serverAddress + keys.replaceWfInstanceVersion, {
            [keys.workflowInstanceName]: workflowInstanceName,
            [keys.versionNumberName]: versionNumber,
        })
        .then(function (response) {
            switch (response.data[keys.statusCodeName]) {
                case 607:
                    // everything went fine
                    break;
                default:
                    // error -> can be
                    break;
            }
        })
    }

    public pullUsers(): User[] {
        let tempUsers: User[] = []
        users.forEach((user: User) => {
            tempUsers.push(new User(user.userName, user.userStatus, user.userPrivilege))
        })
        return tempUsers
    }

    public pushUser(user: User): void { updateUser(user) }
    public pushDeleteUser(user: User): void { deleteUser(user) }
    public async pullServers(): Promise<Server[]> {
        let servers: Server[] = []
        await axios.get('http://localhost:5000/get_server_details')
        .then(function (response) {
            console.log(response)
            const data = response.data
            servers = [new Server(data.serverAddress, 'running', data.containerLimit, data.selectedForExecution, data.serverName, [["cpu1", "50%"]])]
        })
        return servers
        // funktioniert. Es sind aber dummy daten
        // return pullServers2()
    }
    public pushServer(server: Server): void { pushServer(server) }

    private encode_file(file: File): string {return ""} // TODO
}

export default BackendServerCommunicator