class CreateWorkflowInstance {
    private _templatesName: string[]
    private _configFolder: File
    private _workflowInstanceFolder: File
    private _selectedTemplateName: string
    private _workflowInstanceName: string

    /**
    *
    * @param templatesName The templatesName
    * @param configFolder The configFolder
    * @param workflowInstanceFolder The workflowInstanceFolder
    * @param selectedTemplateName The selectedTemplateName
    * @param workflowInstanceName The workflowInstanceName
    */
    constructor(templatesName: string[] = [], configFolder: File = new File([], "emptyFile", { type: 'application/zip' }), workflowInstanceFolder: File = new File([], "emptyFile", { type: 'application/zip' }), selectedTemplateName: string = '', workflowInstanceName: string = '',) {
        this._templatesName = templatesName
        this._configFolder = configFolder
        this._workflowInstanceFolder = workflowInstanceFolder
        this._selectedTemplateName = selectedTemplateName
        this._workflowInstanceName = workflowInstanceName
    }


    /**
    * Gets the templatesName
    * @returns _templatesName
    */
    public get templatesName(): string[] {
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

    /**
    * sets the default values of the class to the instance (the values that will be used, if the constructor is called with no input)
    */
    public setObjectToDefaultValues() {
        this._templatesName = []
        this._configFolder = new File([], "emptyFile", { type: 'application/zip' })
        this._workflowInstanceFolder = new File([], "emptyFile", { type: 'application/zip' })
        this.selectedTemplateName = ''
        this._workflowInstanceName = ''
    }
}

export default CreateWorkflowInstance