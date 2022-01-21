import BackendServerCommunicator from "../Controler/BackendServerCommunicator"
import ConfigFile from "../Classes/ConfigFile"

class ChooseConfigFile {
    private _workflowIntancesAndConfigFilesNames: Array<[string, string[]]>
    private _chosenConfigFile: ConfigFile

    /**
    *
    * @param workflowIntancesAndConfigFilesNames The workflowIntancesAndConfigFilesNames
    * @param chosenConfigFile The chosenConfigFile
    */
    constructor(workflowIntancesAndConfigFilesNames: Array<[string, string[]]> = [], chosenConfigFile: ConfigFile = new ConfigFile('',[]),) {
        this._workflowIntancesAndConfigFilesNames = workflowIntancesAndConfigFilesNames
        this._chosenConfigFile = chosenConfigFile
    }

    /**
    * Gets the workflowIntancesAndConfigFilesNames
    * @returns _workflowIntancesAndConfigFilesNames
    */
    public get workflowIntancesAndConfigFilesNames(): Array<[string, string[]]> {
        this._workflowIntancesAndConfigFilesNames = BackendServerCommunicator.pullWorkflowInstancesNameAndConfigFilesName()
        return this._workflowIntancesAndConfigFilesNames
    }

    /**
    * Gets the chosenConfigFile
    * @returns _chosenConfigFile
    */
    public get chosenConfigFile(): ConfigFile {
        this._chosenConfigFile = BackendServerCommunicator.pullConfigFileWithConfigFileNameWithWorkflowInstanceName()
        return this._chosenConfigFile
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
}