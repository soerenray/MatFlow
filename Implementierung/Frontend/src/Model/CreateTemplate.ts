class CreateTemplate {
    private _newTemplateName: string
    private _templatesName: string[]
    private _chosenTemplateName: string
    private _templateFolder: File
    private _dagFile: File

    /**
    *
    * @param newTemplateName The newTemplateName
    * @param templatesName The templatesName
    * @param chosenTemplateName The chosenTemplateName
    * @param templateFolder The templateFolder
    * @param dagFile The dagFile
    */
    constructor(newTemplateName: string = '', templatesName: string[] = [], chosenTemplateName: string = '', templateFolder: File = new File([], "emptyFile", { type: 'application/zip' }), dagFile: File = new File([], "emptyFile", { type: 'application/zip' }),) {
        this._newTemplateName = newTemplateName
        this._templatesName = templatesName
        this._chosenTemplateName = chosenTemplateName
        this._templateFolder = templateFolder
        this._dagFile = dagFile
    }


    /**
    * Gets the newTemplateName
    * @returns _newTemplateName
    */
     public get newTemplateName(): string {
        return this._newTemplateName
    }
    
    /**
    * Gets the templatesName
    * @returns _templatesName
    */
    public get templatesName(): string[] {
        return this._templatesName
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
    * Sets the value of _newTemplateName
    * @param newTemplateName The new value of _newTemplateName
    */
     public set newTemplateName(newTemplateName: string) {
        this._newTemplateName = newTemplateName
    }

    /**
    * Sets the value of _templatesName
    * @param templatesName The new value of _templatesName
    */
    public set templatesName(templatesName: string[]) {
        this._templatesName = templatesName
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

export default CreateTemplate