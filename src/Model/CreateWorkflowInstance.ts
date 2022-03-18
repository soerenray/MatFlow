import CreateWorkflowInstanceMemento from '@Memento/CreateWorkflowInstanceMemento';

class CreateWorkflowInstance {
    private _dropDownCreateOrImportWokflowInstance: string[]

    private _selectedDropDownItem: string

    private _templatesName: string[]

    private _configFiles: File[]

    private _workflowInstanceFolder: File

    private _selectedTemplateName: string

    private _workflowInstanceName: string

    private _areconfigFilesInBase64WithName: boolean

    private _configFilesInBase64WithName: [ArrayBuffer, string][]

    /**
    *
    * @param dropDownCreateOrImportWokflowInstance The dropDownCreateOrImportWokflowInstance
    * @param selectedDropDownItem The selectedDropDownItem
    * @param templatesName The templatesName
    * @param configFiles The configFiles
    * @param workflowInstanceFolder The workflowInstanceFolder
    * @param selectedTemplateName The selectedTemplateName
    * @param workflowInstanceName The workflowInstanceName
    * @param areconfigFilesInBase64WithName True if all configFiles are transformed to base64
    * @param configFilesInBase64WithName The configFiles as base64 and their names
    */
    constructor(
      dropDownCreateOrImportWokflowInstance: string[] = [],
      selectedDropDownItem = '',
      templatesName: string[] = [],
      configFiles: File[] = [],
      workflowInstanceFolder: File = new File([], 'emptyFile', { type: 'file' }),
      selectedTemplateName = '',
      workflowInstanceName = '',
      areconfigFilesInBase64WithName = false,
      configFilesInBase64WithName: [ArrayBuffer, string][] = [],
    ) {
      this._dropDownCreateOrImportWokflowInstance = dropDownCreateOrImportWokflowInstance;
      this._selectedDropDownItem = selectedDropDownItem;
      this._templatesName = templatesName;
      this._configFiles = configFiles;
      this._workflowInstanceFolder = workflowInstanceFolder;
      this._selectedTemplateName = selectedTemplateName;
      this._workflowInstanceName = workflowInstanceName;
      this._areconfigFilesInBase64WithName = areconfigFilesInBase64WithName;
      this._configFilesInBase64WithName = configFilesInBase64WithName;
    }

    /**
    * Gets the dropDownCreateOrImportWokflowInstance
    * @returns _dropDownCreateOrImportWokflowInstance
    */
    public get dropDownCreateOrImportWokflowInstance(): string[] {
      return this._dropDownCreateOrImportWokflowInstance;
    }

    /**
    * Sets the value of _dropDownCreateOrImportWokflowInstance
    * @param dropDownCreateOrImportWokflowInstance The new value
    *                                               of _dropDownCreateOrImportWokflowInstance
    */
    public set dropDownCreateOrImportWokflowInstance(dropDownCreateOrImportWokflowInstance:
      string[]) {
      this._dropDownCreateOrImportWokflowInstance = dropDownCreateOrImportWokflowInstance;
    }

    /**
    * Gets the selectedDropDownItem
    * @returns _selectedDropDownItem
    */
    public get selectedDropDownItem(): string {
      return this._selectedDropDownItem;
    }

    /**
    * Sets the value of _selectedDropDownItem
    * @param selectedDropDownItem The new value of _selectedDropDownItem
    */
    public set selectedDropDownItem(selectedDropDownItem: string) {
      this._selectedDropDownItem = selectedDropDownItem;
    }

    /**
    * Gets the templatesName
    * @returns _templatesName
    */
    public get templatesName(): string[] {
      return this._templatesName;
    }

    /**
    * Sets the value of _templatesName
    * @param templatesName The new value of _templatesName
    */
    public set templatesName(templatesName: string[]) {
      this._templatesName = templatesName;
    }

    /**
    * Gets the configFiles
    * @returns _configFiles
    */
    public get configFiles(): File[] {
      return this._configFiles;
    }

    /**
    * Sets the value of _configFiles
    * @param configFiles The new value of _configFiles
    */
    public set configFiles(configFiles: File[]) {
      this._configFiles = configFiles;
    }

    /**
    * Gets the workflowInstanceFolder
    * @returns _workflowInstanceFolder
    */
    public get workflowInstanceFolder(): File {
      return this._workflowInstanceFolder;
    }

    /**
    * Sets the value of _workflowInstanceFolder
    * @param workflowInstanceFolder The new value of _workflowInstanceFolder
    */
    public set workflowInstanceFolder(workflowInstanceFolder: File) {
      this._workflowInstanceFolder = workflowInstanceFolder;
    }

    /**
    * Gets the selectedTemplateName
    * @returns _selectedTemplateName
    */
    public get selectedTemplateName(): string {
      return this._selectedTemplateName;
    }

    /**
    * Sets the value of _selectedTemplateName
    * @param selectedTemplateName The new value of _selectedTemplateName
    */
    public set selectedTemplateName(selectedTemplateName: string) {
      this._selectedTemplateName = selectedTemplateName;
    }

    /**
    * Gets the workflowInstanceName
    * @returns _workflowInstanceName
    */
    public get workflowInstanceName(): string {
      return this._workflowInstanceName;
    }

    /**
    * Sets the value of _workflowInstanceName
    * @param workflowInstanceName The new value of _workflowInstanceName
    */
    public set workflowInstanceName(workflowInstanceName: string) {
      this._workflowInstanceName = workflowInstanceName;
    }

    /**
    * Gets the areconfigFilesInBase64WithName
    * @returns _areconfigFilesInBase64WithName
    */
    public get areconfigFilesInBase64WithName(): boolean {
      return this._areconfigFilesInBase64WithName;
    }

    /**
    * Sets the value of _areconfigFilesInBase64WithName
    * @param areconfigFilesInBase64WithName The new value of _areconfigFilesInBase64WithName
    */
    public set areconfigFilesInBase64WithName(areconfigFilesInBase64WithName: boolean) {
      this._areconfigFilesInBase64WithName = areconfigFilesInBase64WithName;
    }

    /**
    * Gets the configFilesInBase64WithName
    * @returns _configFilesInBase64WithName
    */
    public get configFilesInBase64WithName(): [ArrayBuffer, string][] {
      return this._configFilesInBase64WithName;
    }

    /**
    * Sets the value of _configFilesInBase64WithName
    * @param configFilesInBase64WithName The new value of _configFilesInBase64WithName
    */
    public set configFilesInBase64WithName(configFilesInBase64WithName: [ArrayBuffer, string][]) {
      this._configFilesInBase64WithName = configFilesInBase64WithName;
    }

    public setCreateWorkflowInstanceMemento(createWorkflowInstanceMemento:
       CreateWorkflowInstanceMemento): void {
      const tempCreateWorkflowInstanceObject = createWorkflowInstanceMemento
        .createWorkflowInstanceObject;
      this.dropDownCreateOrImportWokflowInstance = tempCreateWorkflowInstanceObject
        .dropDownCreateOrImportWokflowInstance;
      this.selectedDropDownItem = tempCreateWorkflowInstanceObject.selectedDropDownItem;
      this.templatesName = tempCreateWorkflowInstanceObject.templatesName;
      this.configFiles = tempCreateWorkflowInstanceObject.configFiles;
      this.workflowInstanceFolder = tempCreateWorkflowInstanceObject.workflowInstanceFolder;
      this.selectedTemplateName = tempCreateWorkflowInstanceObject.selectedTemplateName;
      this.workflowInstanceName = tempCreateWorkflowInstanceObject.workflowInstanceName;
      this.areconfigFilesInBase64WithName = tempCreateWorkflowInstanceObject
        .areconfigFilesInBase64WithName;
      this.configFilesInBase64WithName = tempCreateWorkflowInstanceObject
        .configFilesInBase64WithName;
    }

    public createWorkflowInstanceMemento(): CreateWorkflowInstanceMemento {
      return new CreateWorkflowInstanceMemento(new CreateWorkflowInstance(
        this.dropDownCreateOrImportWokflowInstance,
        this.selectedDropDownItem,
        this.templatesName,
        this.configFiles,
        this.workflowInstanceFolder,
        this.selectedTemplateName,
        this.workflowInstanceName,
        this.areconfigFilesInBase64WithName,
        this.configFilesInBase64WithName,
      ));
    }
}

export default CreateWorkflowInstance;
