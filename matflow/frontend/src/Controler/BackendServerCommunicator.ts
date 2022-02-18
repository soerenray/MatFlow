import ConfigFile from '../Classes/ConfigFile'
import User from '../Classes/User'
import Server from '../Classes/Server'
import Version from '../Classes/Version'
import Template from '../Classes/Template'

import { templateNames, workflowInstancesNameAndConfigFilesName, setWfConf, getWfConf, versions, users, deleteUser, updateUser, pullServers2, pushServer } from '../DummyData/DataInTypscript'
import WorkflowInstance from '../Classes/WorkflowInstance'

type workflowInstanceNameAsString = keyof typeof versions

class BackendServerCommunicator {
    public constructor() { }
    public pushLogIn(userName: string, userPassword: string): void { return }
    public pushSignUp(userName: string, userPassword: string, userPasswordRepeated: string): void { return }
    // public pullGraphForTemporaryTemplate(tempTemplate: Template): File { return }
    public pushCreateTemplate(template: Template): void { return }
    public pushCreateWorkflowInstanceFromTemplate(workflowInstanceObject: WorkflowInstance): void { return }
    public pushExistingWorkflowInstance(workflowInstanceAsZip: File): void { return }
    public pullTemplatesName(): string[] { return templateNames }
    // public pullTemplateWithName(templateName: string): Template { return }
    public pullWorkflowInstancesNameAndConfigFilesName(): Array<[string, string[]]> { return workflowInstancesNameAndConfigFilesName }
    public pullConfigFileWithConfigFileNameWithWorkflowInstanceName(workflowInstanceName: string, configFileName: string): ConfigFile {
        if (workflowInstanceName === "workflowInstance1") {
            if (configFileName === "conf1") {
                return getWfConf('wf1conf1')
            }
            return getWfConf('wf1conf2')
        } else if (workflowInstanceName === "workflowInstance2") {
            if (configFileName === "conf1") {
                return getWfConf('wf2conf1')
            } else if (configFileName === "conf2") {
                return getWfConf('wf2conf2')
            }
            return getWfConf('wf2conf3')
        }
        return new ConfigFile()
    }
    public pushConfigFilesWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void {
        if (workflowInstanceName === "workflowInstance1") {
            if (configFiles[0]) {
                setWfConf('wf1' + configFiles[0].configFileName, configFiles[0])
            }
            if (configFiles[1]) {
                setWfConf('wf1' + configFiles[1].configFileName, configFiles[1])
            }
        } else if (workflowInstanceName === "workflowInstance2") {
            if (configFiles[0]) {
                setWfConf('wf2' + configFiles[0].configFileName, configFiles[0])
            }
            if (configFiles[1]) {
                setWfConf('wf2' + configFiles[1].configFileName, configFiles[1])
            }
            if (configFiles[2]) {
                setWfConf('wf2' + configFiles[2].configFileName, configFiles[2])
            }
        }
    }
    public pullVersionsWithWorkflowInstanceName(workflowInstanceName: workflowInstanceNameAsString): Version[] { return versions[workflowInstanceName] }
    public pushReplaceActiveVersionOfWorkflowInstance(workflowInstanceName: string, versionNumber: string): void { return }
    public pullUsers(): User[] {
        let tempUsers: User[] = []
        users.forEach((user: User) => {
            tempUsers.push(new User(user.userName, user.userStatus, user.userPrivilege))
        })
        return tempUsers
    }
    public pushUser(user: User): void { updateUser(user) }
    public pushDeleteUser(user: User): void { deleteUser(user) }
    public pullServers(): Server[] { return pullServers2() }
    public pushServer(server: Server): void { pushServer(server) }
}

export default BackendServerCommunicator