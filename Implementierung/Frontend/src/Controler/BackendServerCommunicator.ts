import ConfigFile from '../Classes/ConfigFile'
import User from '../Classes/User'
import Server from '../Classes/Server'
import Version from '../Classes/Version'
import Template from '../Classes/Template'

import {templateNames, workflowInstancesNameAndConfigFilesName, workflowInstancesName, conf1, versions, users} from '../DummyData/DataInTypscript'

class BackendServerCommunicator {
    public constructor() {}

    public static login(userName: string, userPassword: string): void { return  }
    public static register(userName: string, userPassword: string): void { return  }
    public static pullGraphForTemporaryTemplate(tempTemplate: Template): File { return }
    public static pushCreateTemplate(template: Template): void { return  }
    public static pushCreateWorkflowInstanceFromTemplate(templateName: string, workflowInstanceName: string, configFolder: File): void { return  }
    public static pullTemplatesName(): string[] { return templateNames }
    public static pullTemplateWithName(templateName: string): Template { return  }
    public static pullWorkflowInstancesNameAndConfigFilesName(): Array<[string, string[]]> { return workflowInstancesNameAndConfigFilesName }
    public static pullWorkflowInstancesName(): string[] {return workflowInstancesName }
    public static pullConfigFileWithConfigFileNameWithWorkflowInstanceName(configFileName: string, workflowInstanceName: string): ConfigFile { return conf1 }
    public static pushConfigFilesWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void { return }
    public static pullVersionsWithWorkflowInstanceName(workflowInstanceName: string): Version[] { return versions }
    public static pushReplaceActiveVersionOfWorkflowInstance(workflowInstanceName: string, versionNumber: string): void { return  }
    public static pullUsers(): User[] { return users }
    public static pushUser(user: User): void { return  }
    public static pushDeleteUser(user: User): void { return  }
    public static pullServers(): Server[] { return  }
    public static pushServer(server: Server): void { return  }
}

export default BackendServerCommunicator