import Version from '../Classes/Version'
import BackendServerCommunicator from "../Controler/BackendServerCommunicator"

class VersionControl {
    private _tableHeaders: object[]
    private _versions: Version[]
    private _workflowInstanceName: string

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param versions The versions
    * @param workflowInstanceName The workflowInstanceName
    */
    constructor(tableHeaders: object[], versions: Version[], workflowInstanceName: string) {
        this._tableHeaders = tableHeaders
        this._versions = versions
        this._workflowInstanceName = workflowInstanceName
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
        this._versions = BackendServerCommunicator.pullVersionsWithWorkflowInstanceName(this._workflowInstanceName)
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
    * Sets the value of _workflowInstanceName
    * @param workflowInstanceName The new value of _workflowInstanceName
    */
    public set workflowInstanceName(workflowInstanceName: string) {
        this._workflowInstanceName = workflowInstanceName
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
}