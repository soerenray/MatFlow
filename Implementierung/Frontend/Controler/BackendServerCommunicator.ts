class BackendServerCommunicator {
    private _singleBackendServerCommunicator: BackendServerCommunicator = null

    /**
     * Singelton pattern
     */
    private constructor() {}

    /**
     * Returns the onle object ob BackendServerCommunicator
     * @returns The single instance of BackendServerCommunicator
     */
    public returnBackendServerCommunicator(): BackendServerCommunicator { 
        if(this._singleBackendServerCommunicator === null) {
            this._singleBackendServerCommunicator = new BackendServerCommunicator()
        }
        return this._singleBackendServerCommunicator
      }

    public login(userName: string, userPassword: string): void { return  }
    public register(userName: string, userPassword: string): void { return  }
    public pullGraphForTemporaryTemplate(tempTemplate: Template): File { return }
    public pushCreateTemplate(template: Template): void { return  }
    public pushCreateWorkflowInstanceFromTemplate(templateName: string, workflowInstanceName: string, configFolder: File): void { return  }
    public pullTemplatesName(): string[] { return  }
    public pullTemplateWithName(templateName: string): Template { return  }
    public pullWorkflowInstancesNameAndConfigFilesName(): string[][] { return  }
    public pullConfigFileWithConfigFileNameWithWorkflowInstanceName(configFileName: string, workflowInstanceName: string): ConfigFile { return  }
    public pushConfigFilesWithWorkflowInstanceName(configFiles: ConfigFile[], workflowInstanceName: string): void { return  }
    public pullVersionsWithWorkflowInstanceName(workflowInstanceName: string): Version[] { return  }
    public pushReplaceActiveVersionOfWorkflowInstance(workflowInstanceName: string, versionNumber: string): void { return  }
    public pullUsers(): User[] { return  }
    public pushUser(user: User): void { return  }
    public pushDeleteUser(user: User): void { return  }
    public pullServers(): Server[] { return  }
    public pushServer(server: Server): void { return  }
}