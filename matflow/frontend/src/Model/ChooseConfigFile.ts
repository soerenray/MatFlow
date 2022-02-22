import ConfigFile from "@Classes/ConfigFile"

class ChooseConfigFile {
    private _workflowIntancesAndConfigFilesNames: Array<[string, string[]]>
    private _chosenConfigFile: ConfigFile
    private _updatedConfigFiles: ConfigFile[]
    private _selectedWorkflowInstanceName: string
    private _selectedConfigFileName: string

    /**
    *
    * @param workflowIntancesAndConfigFilesNames The workflowIntancesAndConfigFilesNames
    * @param chosenConfigFile The chosenConfigFile
    * @param updatedConfigFiles The updatedConfigFiles
    * @param selectedWorkflowInstanceName The selectedWorkflowInstanceName
    * @param selectedConfigFileName The selectedConfigFileName
    */
    constructor(workflowIntancesAndConfigFilesNames: Array<[string, string[]]> = [], chosenConfigFile: ConfigFile = new ConfigFile(), updatedConfigFiles: ConfigFile[] = [], selectedWorkflowInstanceName: string = '', selectedConfigFileName: string = '',) {
        this._workflowIntancesAndConfigFilesNames = workflowIntancesAndConfigFilesNames
        this._chosenConfigFile = chosenConfigFile
        this._updatedConfigFiles = updatedConfigFiles
        this._selectedWorkflowInstanceName = selectedWorkflowInstanceName
        this._selectedConfigFileName = selectedConfigFileName
    }

    /**
    * Gets the workflowIntancesAndConfigFilesNames
    * @returns _workflowIntancesAndConfigFilesNames
    */
    public get workflowIntancesAndConfigFilesNames(): Array<[string, string[]]> {
        return this._workflowIntancesAndConfigFilesNames
    }

    /**
    * Gets the chosenConfigFile
    * @returns _chosenConfigFile
    */
    public get chosenConfigFile(): ConfigFile {
        return this._chosenConfigFile
    }

    /**
    * Gets the updatedConfigFiles
    * @returns _updatedConfigFiles
    */
    public get updatedConfigFiles(): ConfigFile[] {
        return this._updatedConfigFiles
    }

    /**
    * Gets the selectedWorkflowInstanceName
    * @returns _selectedWorkflowInstanceName
    */
    public get selectedWorkflowInstanceName(): string {
        return this._selectedWorkflowInstanceName
    }

    /**
    * Gets the selectedConfigFileName
    * @returns _selectedConfigFileName
    */
    public get selectedConfigFileName(): string {
        return this._selectedConfigFileName
    }

    /**
    * Sets the value of _workflowIntancesAndConfigFilesNames
    * @param workflowIntancesAndConfigFilesNames The new value of _workflowIntancesAndConfigFilesNames
    */
    public set workflowIntancesAndConfigFilesNames(workflowIntancesAndConfigFilesNames: Array<[string, string[]]>) {
        this._workflowIntancesAndConfigFilesNames = workflowIntancesAndConfigFilesNames
    }

    /**
    * Sets the value of _chosenConfigFile
    * @param chosenConfigFile The new value of _chosenConfigFile
    */
    public set chosenConfigFile(chosenConfigFile: ConfigFile) {
        this._chosenConfigFile = chosenConfigFile
    }

    /**
    * Sets the value of _updatedConfigFiles
    * @param updatedConfigFiles The new value of _updatedConfigFiles
    */
    public set updatedConfigFiles(updatedConfigFiles: ConfigFile[]) {
        this._updatedConfigFiles = updatedConfigFiles
    }

    /**
    * Sets the value of _selectedWorkflowInstanceName
    * @param selectedWorkflowInstanceName The new value of _selectedWorkflowInstanceName
    */
    public set selectedWorkflowInstanceName(selectedWorkflowInstanceName: string) {
        this._selectedWorkflowInstanceName = selectedWorkflowInstanceName
    }

    /**
    * Sets the value of _selectedConfigFileName
    * @param selectedConfigFileName The new value of _selectedConfigFileName
    */
    public set selectedConfigFileName(selectedConfigFileName: string) {
        this._selectedConfigFileName = selectedConfigFileName
    }
}

export default ChooseConfigFile