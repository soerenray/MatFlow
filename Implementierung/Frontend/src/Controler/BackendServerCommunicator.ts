import ConfigFile from '../Classes/ConfigFile'
import User from '../Classes/User'
import Server from '../Classes/Server'
import Version from '../Classes/Version'
import Template from '../Classes/Template'

import { templateNames, workflowInstancesNameAndConfigFilesName, setWfConf, getWfConf, versions, users, } from '../DummyData/DataInTypscript'

class BackendServerCommunicator {
    public constructor() { }
    public static login(userName: string, userPassword: string): void { return }
    public static register(userName: string, userPassword: string): void { return }
    public static pullGraphForTemporaryTemplate(tempTemplate: Template): File { return }
    public static pushCreateTemplate(template: Template): void { return }
    public static pushCreateWorkflowInstanceFromTemplate(templateName: string, workflowInstanceName: string, configFolder: File): void { return }
    public static pullTemplatesName(): string[] { return templateNames }
    public static pullTemplateWithName(templateName: string): Template { return }
    public static pullWorkflowInstancesNameAndConfigFilesName(): Array<[string, string[]]> { return workflowInstancesNameAndConfigFilesName }
    public static pullConfigFileWithConfigFileNameWithWorkflowInstanceName(workflowInstanceName: string, configFileName: string): ConfigFile {
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
    public static pushConfigFilesWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void {
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
    public static pullVersionsWithWorkflowInstanceName(workflowInstanceName: string): Version[] { return versions }
    public static pushReplaceActiveVersionOfWorkflowInstance(workflowInstanceName: string, versionNumber: string): void { return }
    public static pullUsers(): User[] { return users }
    public static pushUser(user: User): void { return }
    public static pushDeleteUser(user: User): void { return }
    public static pullServers(): Server[] { return }
    public static pushServer(server: Server): void { return }
}

export default BackendServerCommunicator