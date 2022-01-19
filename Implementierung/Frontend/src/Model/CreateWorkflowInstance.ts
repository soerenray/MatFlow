import BackendServerCommunicator from "../Controler/BackendServerCommunicator"

class CreateWorkflowInstance {
    private _templatesName: string[]
    private _configFolder: File
    private _workflowInstanceFolder: File
    private _selectedTemplateName: string
    private _workflowInstanceName: string

    constructor() {}

    /**
    * Gets the templatesName
    * @returns _templatesName
    */
    public get templatesName(): string[] {
        this._templatesName = BackendServerCommunicator.pullTemplatesName()
        return this._templatesName
    }

    /**
    * Gets the configFolder
    * @returns _configFolder
    */
    public get configFolder(): File {
        return this._configFolder
    }

    /**
    * Gets the workflowInstanceFolder
    * @returns _workflowInstanceFolder
    */
    public get workflowInstanceFolder(): File {
        return this._workflowInstanceFolder
    }

    /**
    * Gets the selectedTemplateName
    * @returns _selectedTemplateName
    */
    public get selectedTemplateName(): string {
        return this._selectedTemplateName
    }

    /**
    * Gets the workflowInstanceName
    * @returns _workflowInstanceName
    */
    public get workflowInstanceName(): string {
        return this._workflowInstanceName
    }


    /**
    * Sets the value of _templatesName
    * @param templatesName The new value of _templatesName
    */
    public set templatesName(templatesName: string[]) {
        this._templatesName = templatesName
    }

    /**
    * Sets the value of _configFolder
    * @param configFolder The new value of _configFolder
    */
    public set configFolder(configFolder: File) {
        this._configFolder = configFolder
    }

    /**
    * Sets the value of _workflowInstanceFolder
    * @param workflowInstanceFolder The new value of _workflowInstanceFolder
    */
    public set workflowInstanceFolder(workflowInstanceFolder: File) {
        this._workflowInstanceFolder = workflowInstanceFolder
    }

    /**
    * Sets the value of _selectedTemplateName
    * @param selectedTemplateName The new value of _selectedTemplateName
    */
    public set selectedTemplateName(selectedTemplateName: string) {
        this._selectedTemplateName = selectedTemplateName
    }

    /**
    * Sets the value of _workflowInstanceName
    * @param workflowInstanceName The new value of _workflowInstanceName
    */
    public set workflowInstanceName(workflowInstanceName: string) {
        this._workflowInstanceName = workflowInstanceName
    }
}

export default CreateWorkflowInstance