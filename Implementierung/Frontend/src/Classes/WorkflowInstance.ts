import Template from "./Template"

class WorkflowInstance extends Template {
    private _versionsNumbers: string[]
    private _activeVersionNumber: string

    /**
    *
    * @param dagDefinitionFile The dagDefinitionFile
    * @param templateName The templateName
    * @param versionsNumbers The versionsNumbers
    * @param activeVersionNumber The activeVersionNumber
    */
    constructor(dagDefinitionFile: File = new File([], "emptyFile", { type: 'application/zip' }), templateName: string = '', versionsNumbers: string[] = [], activeVersionNumber: string = '',) {
        super(dagDefinitionFile, templateName)
        this._versionsNumbers = versionsNumbers
        this._activeVersionNumber = activeVersionNumber
    }

    /**
    * Gets the versionsNumbers
    * @returns _versionsNumbers
    */
    public get versionsNumbers(): string[] {
        return this._versionsNumbers
    }

    /**
    * Gets the activeVersionNumber
    * @returns _activeVersionNumber
    */
    public get activeVersionNumber(): string {
        return this._activeVersionNumber
    }


    /**
    * Sets the value of _versionsNumbers
    * @param versionsNumbers The new value of _versionsNumbers
    */
    public set versionsNumbers(versionsNumbers: string[]) {
        this._versionsNumbers = versionsNumbers
    }

    /**
    * Sets the value of _activeVersionNumber
    * @param activeVersionNumber The new value of _activeVersionNumber
    */
    public set activeVersionNumber(activeVersionNumber: string) {
        this._activeVersionNumber = activeVersionNumber
    }
}

export default WorkflowInstance