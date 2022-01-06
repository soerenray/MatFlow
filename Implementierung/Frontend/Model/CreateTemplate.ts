class CreateTemplate {
    private _templatesNames: string[]
    private _chosenTemplateName: string
    private _templateFolder: File
    private _dagFile: File

    /**
    *
    * @param templatesNames The templatesNames
    * @param chosenTemplateName The chosenTemplateName
    * @param templateFolder The templateFolder
    * @param dagFile The dagFile
    */
    constructor(templatesNames: string[], chosenTemplateName: string, templateFolder: File, dagFile: File,) {
        this._templatesNames = templatesNames
        this._chosenTemplateName = chosenTemplateName
        this._templateFolder = templateFolder
        this._dagFile = dagFile
    }

    /**
    * Gets the templatesNames
    * @returns _templatesNames
    */
    public get templatesNames(): string[] {
        return this._templatesNames
    }

    /**
    * Gets the chosenTemplateName
    * @returns _chosenTemplateName
    */
    public get chosenTemplateName(): string {
        return this._chosenTemplateName
    }

    /**
    * Gets the templateFolder
    * @returns _templateFolder
    */
    public get templateFolder(): File {
        return this._templateFolder
    }

    /**
    * Gets the dagFile
    * @returns _dagFile
    */
    public get dagFile(): File {
        return this._dagFile
    }


    /**
    * Sets the value of _templatesNames
    * @param templatesNames The new value of _templatesNames
    */
    public set templatesNames(templatesNames: string[]) {
        this._templatesNames = templatesNames
    }

    /**
    * Sets the value of _chosenTemplateName
    * @param chosenTemplateName The new value of _chosenTemplateName
    */
    public set chosenTemplateName(chosenTemplateName: string) {
        this._chosenTemplateName = chosenTemplateName
    }

    /**
    * Sets the value of _templateFolder
    * @param templateFolder The new value of _templateFolder
    */
    public set templateFolder(templateFolder: File) {
        this._templateFolder = templateFolder
    }

    /**
    * Sets the value of _dagFile
    * @param dagFile The new value of _dagFile
    */
    public set dagFile(dagFile: File) {
        this._dagFile = dagFile
    }
}