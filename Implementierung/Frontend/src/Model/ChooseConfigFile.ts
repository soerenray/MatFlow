class ChooseConfigFile {
    private _workflowIntancesAndConfigFilesNames: string[][]
    private _selectedWorkflowInstance: string
    private _selectedConfigFile: string

    /**
    *
    * @param workflowIntancesAndConfigFilesNames The workflowIntancesAndConfigFilesNames
    * @param selectedWorkflowInstance The selectedWorkflowInstance
    * @param selectedConfigFile The selectedConfigFile
    */
    constructor(workflowIntancesAndConfigFilesNames: string[][], selectedWorkflowInstance: string, selectedConfigFile: string,) {
        this._workflowIntancesAndConfigFilesNames = workflowIntancesAndConfigFilesNames
        this._selectedWorkflowInstance = selectedWorkflowInstance
        this._selectedConfigFile = selectedConfigFile
    }

    /**
    * Gets the workflowIntancesAndConfigFilesNames
    * @returns _workflowIntancesAndConfigFilesNames
    */
    public get workflowIntancesAndConfigFilesNames(): string[][] {
        return this._workflowIntancesAndConfigFilesNames
    }

    /**
    * Gets the selectedWorkflowInstance
    * @returns _selectedWorkflowInstance
    */
    public get selectedWorkflowInstance(): string {
        return this._selectedWorkflowInstance
    }

    /**
    * Gets the selectedConfigFile
    * @returns _selectedConfigFile
    */
    public get selectedConfigFile(): string {
        return this._selectedConfigFile
    }


    /**
    * Sets the value of _workflowIntancesAndConfigFilesNames
    * @param workflowIntancesAndConfigFilesNames The new value of _workflowIntancesAndConfigFilesNames
    */
    public set workflowIntancesAndConfigFilesNames(workflowIntancesAndConfigFilesNames: string[][]) {
        this._workflowIntancesAndConfigFilesNames = workflowIntancesAndConfigFilesNames
    }

    /**
    * Sets the value of _selectedWorkflowInstance
    * @param selectedWorkflowInstance The new value of _selectedWorkflowInstance
    */
    public set selectedWorkflowInstance(selectedWorkflowInstance: string) {
        this._selectedWorkflowInstance = selectedWorkflowInstance
    }

    /**
    * Sets the value of _selectedConfigFile
    * @param selectedConfigFile The new value of _selectedConfigFile
    */
    public set selectedConfigFile(selectedConfigFile: string) {
        this._selectedConfigFile = selectedConfigFile
    }
}