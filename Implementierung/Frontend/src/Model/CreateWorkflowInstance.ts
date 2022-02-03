class CreateWorkflowInstance {
    private _dropDownCreateOrImportWokflowInstance: string[]
    private _selectedDropDownItem: string
    private _templatesName: string[]
    private _configFolder: File
    private _workflowInstanceFolder: File
    private _selectedTemplateName: string
    private _workflowInstanceName: string

    /**
    *
    * @param dropDownCreateOrImportWokflowInstance The dropDownCreateOrImportWokflowInstance
    * @param selectedDropDownItem The selectedDropDownItem
    * @param templatesName The templatesName
    * @param configFolder The configFolder
    * @param workflowInstanceFolder The workflowInstanceFolder
    * @param selectedTemplateName The selectedTemplateName
    * @param workflowInstanceName The workflowInstanceName
    */
    constructor(dropDownCreateOrImportWokflowInstance: string[] = [], selectedDropDownItem: string = '', templatesName: string[] = [], configFolder: File = new File([], "emptyFile", { type: 'application/zip' }), workflowInstanceFolder: File = new File([], "emptyFile", { type: 'application/zip' }), selectedTemplateName: string = '', workflowInstanceName: string = '',) {
        this._dropDownCreateOrImportWokflowInstance = dropDownCreateOrImportWokflowInstance
        this._selectedDropDownItem = selectedDropDownItem
        this._templatesName = templatesName
        this._configFolder = configFolder
        this._workflowInstanceFolder = workflowInstanceFolder
        this._selectedTemplateName = selectedTemplateName
        this._workflowInstanceName = workflowInstanceName
    }

    /**
    * Gets the dropDownCreateOrImportWokflowInstance
    * @returns _dropDownCreateOrImportWokflowInstance
    */
    public get dropDownCreateOrImportWokflowInstance(): string[] {
        return this._dropDownCreateOrImportWokflowInstance
    }

    /**
    * Gets the selectedDropDownItem
    * @returns _selectedDropDownItem
    */
    public get selectedDropDownItem(): string {
        return this._selectedDropDownItem
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
    * Sets the value of _dropDownCreateOrImportWokflowInstance
    * @param dropDownCreateOrImportWokflowInstance The new value of _dropDownCreateOrImportWokflowInstance
    */
    public set dropDownCreateOrImportWokflowInstance(dropDownCreateOrImportWokflowInstance: string[]) {
        this._dropDownCreateOrImportWokflowInstance = dropDownCreateOrImportWokflowInstance
    }

    /**
    * Sets the value of _selectedDropDownItem
    * @param selectedDropDownItem The new value of _selectedDropDownItem
    */
    public set selectedDropDownItem(selectedDropDownItem: string) {
        this._selectedDropDownItem = selectedDropDownItem
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

    public setCreateWorkflowInstanceMemento() {

    }

    public createWorkflowInstanceMemento() {

    }
}

export default CreateWorkflowInstance