import Version from '../Classes/Version'

class VersionControl {
    private _tableHeaders: object[]
    private _versions: Version[]
    private _workflowInstanceName: string
    private _workflowInstancesName: string[]

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param versions The versions
    * @param workflowInstanceName The workflowInstanceName
    * @param workflowInstancesName The workflowInstancesName
    */
    constructor(tableHeaders: object[] = [], versions: Version[] = [], workflowInstanceName: string = "", workflowInstancesName: string[] = []) {
        this._tableHeaders = tableHeaders
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