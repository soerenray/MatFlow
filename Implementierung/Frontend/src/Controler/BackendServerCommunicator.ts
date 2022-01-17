import ConfigFile from '../Classes/ConfigFile'
import User from '../Classes/User'
import Server from '../Classes/Server'
import Version from '../Classes/Version'
import Template from '../Classes/Template'
import WorkflowInstance from '../Classes/WorkflowInstance'

import {templateNames, workflowInstancesNameAndConfigFilesName, conf1, versions, users} from '../DummyData/DataInTypscript'

class BackendServerCommunicator {
    public constructor() {}

    public login(userName: string, userPassword: string): void { return  }
    public register(userName: string, userPassword: string): void { return  }
    public pullGraphForTemporaryTemplate(tempTemplate: Template): File { return }
    public pushCreateTemplate(template: Template): void { return  }
    public pushCreateWorkflowInstanceFromTemplate(templateName: string, workflowInstanceName: string, configFolder: File): void { return  }
    public pullTemplatesName(): string[] { return templateNames }
    public pullTemplateWithName(templateName: string): Template { return  }
    public pullWorkflowInstancesNameAndConfigFilesName(): Array<[string, string[]]> { return workflowInstancesNameAndConfigFilesName }
    public pullConfigFileWithConfigFileNameWithWorkflowInstanceName(configFileName: string, workflowInstanceName: string): ConfigFile { return conf1 }
    public pushConfigFilesWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void { return }
    public pullVersionsWithWorkflowInstanceName(workflowInstanceName: string): Version[] { return versions }
    public pushReplaceActiveVersionOfWorkflowInstance(workflowInstanceName: string, versionNumber: string): void { return  }
    public pullUsers(): User[] { return users }
    public pushUser(user: User): void { return  }
    public pushDeleteUser(user: User): void { return  }
    public pullServers(): Server[] { return  }
    public pushServer(server: Server): void { return  }
}
