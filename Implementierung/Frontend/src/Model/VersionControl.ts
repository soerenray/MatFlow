import Version from '../Classes/Version'

class VersionControl {
    private _tableHeaders: object[]
    private _dialogKeyValuePairs: boolean
    private _selectedVersionObject: Version
    private _versions: Version[]
    private _workflowInstanceName: string
    private _workflowInstancesName: string[]

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param dialogKeyValuePairs True if the difference of the keyValuePairs should be displayed, false otherwise
    * @param selectedVersionObject The selectedVersionObject
    * @param versions The versions
    * @param workflowInstanceName The workflowInstanceName
    * @param workflowInstancesName The workflowInstancesName
    */
    constructor(tableHeaders: object[] = [], dialogKeyValuePairs: boolean = false, selectedVersionObject: Version = new Version(), versions: Version[] = [], workflowInstanceName: string = "", workflowInstancesName: string[] = []) {
        this._tableHeaders = tableHeaders
        this._dialogKeyValuePairs = dialogKeyValuePairs
        this._selectedVersionObject = selectedVersionObject
        this._versions = versions
        this._workflowInstanceName = workflowInstanceName
        this._workflowInstancesName = workflowInstancesName
    }

    /**
    * Gets the tableHeaders
    * @returns _tableHeaders
    */
    public get tableHeaders(): object[] {
        return this._tableHeaders
    }

    /**
    * Gets the dialogKeyValuePairs
    * @returns _dialogKeyValuePairs
    */
    public get dialogKeyValuePairs(): boolean {
        return this._dialogKeyValuePairs
    }

    /**
    * Gets the selectedVersionObject
    * @returns _selectedVersionObject
    */
    public get selectedVersionObject(): Version {
        return this._selectedVersionObject
    }

    /**
    * Gets the versions
    * @returns _versions
    */
    public get versions(): Version[] {
        return this._versions
    }

    /**
    * Gets the workflowInstanceName
    * @returns _workflowInstanceName
    */
    public get workflowInstanceName(): string {
        return this._workflowInstanceName
    }

    /**
    * Gets the workflowInstancesName
    * @returns _workflowInstancesName
    */
    public get workflowInstancesName(): string[] {
        return this._workflowInstancesName
    }

    /**
    * Sets the value of _tableHeaders
    * @param tableHeaders The new value of _tableHeaders
    */
    public set tableHeaders(tableHeaders: object[]) {
        this._tableHeaders = tableHeaders
    }

    /**
    * Sets the value of _dialogKeyValuePairs
    * @param dialogKeyValuePairs The new value of _dialogKeyValuePairs
    */
    public set dialogKeyValuePairs(dialogKeyValuePairs: boolean) {
        this._dialogKeyValuePairs = dialogKeyValuePairs
    }

    /**
    * Sets the value of _selectedVersionObject
    * @param selectedVersionObject The new value of _selectedVersionObject
    */
    public set selectedVersionObject(selectedVersionObject: Version) {
        this._selectedVersionObject = selectedVersionObject
    }

    /**
    * Sets the value of _versions
    * @param versions The new value of _versions
    */
    public set versions(versions: Version[]) {
        this._versions = versions
    }

    /**
    * Sets the value of _workflowInstanceName
    * @param workflowInstanceName The new value of _workflowInstanceName
    */
    public set workflowInstanceName(workflowInstanceName: string) {
        this._workflowInstanceName = workflowInstanceName
    }

    /**
    * Sets the value of _workflowInstancesName
    * @param workflowInstanceName The new value of _workflowInstancesName
    */
    public set workflowInstancesName(workflowInstancesName: string[]) {
        this._workflowInstancesName = workflowInstancesName
    }
}

export default VersionControl