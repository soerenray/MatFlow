class Template {
    private _dagDefinitionFile: File
    private _templateName: string

    /**
    *
    * @param dagDefinitionFile The dagDefinitionFile
    * @param templateName The templateName
    */
    constructor(dagDefinitionFile: File, templateName: string,) {
        this._dagDefinitionFile = dagDefinitionFile
        this._templateName = templateName
    }

    /**
    * Gets the dagDefinitionFile
    * @returns _dagDefinitionFile
    */
    public get dagDefinitionFile(): File {
        return this._dagDefinitionFile
    }

    /**
    * Gets the templateName
    * @returns _templateName
    */
    public get templateName(): string {
        return this._templateName
    }


    /**
    * Sets the value of _dagDefinitionFile
    * @param dagDefinitionFile The new value of _dagDefinitionFile
    */
    public set dagDefinitionFile(dagDefinitionFile: File) {
        this._dagDefinitionFile = dagDefinitionFile
    }

    /**
    * Sets the value of _templateName
    * @param templateName The new value of _templateName
    */
    public set templateName(templateName: string) {
        this._templateName = templateName
    }
}

export default Template