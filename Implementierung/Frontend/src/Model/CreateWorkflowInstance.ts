class CreateWorkflowInstance {
    private _templatesNames: string[]
    private _configFolder: File
    private _workflowInstanceFolder: File
    private _selectedTemplateName: string
    private _workflowInstanceName: string

    /**
    *
    * @param templatesNames The templatesNames
    * @param configFolder The configFolder
    * @param workflowInstanceFolder The workflowInstanceFolder
    * @param selectedTemplateName The selectedTemplateName
    * @param workflowInstanceName The workflowInstanceName
    */
    constructor(templatesNames: string[], configFolder: File, workflowInstanceFolder: File, selectedTemplateName: string, workflowInstanceName: string,) {
        this._templatesNames = templatesNames
        this._configFolder = configFolder
        this._workflowInstanceFolder = workflowInstanceFolder
        this._selectedTemplateName = selectedTemplateName
        this._workflowInstanceName = workflowInstanceName
    }

    /**
    * Gets the templatesNames
    * @returns _templatesNames
    */
    public get templatesNames(): string[] {
        return this._templatesNames
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
    * Sets the value of _templatesNames
    * @param templatesNames The new value of _templatesNames
    */
    public set templatesNames(templatesNames: string[]) {
        this._templatesNames = templatesNames
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