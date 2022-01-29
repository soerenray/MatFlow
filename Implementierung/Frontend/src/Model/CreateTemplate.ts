class CreateTemplate {
    private _templatesName: string[]
    private _chosenTemplateName: string
    private _templateFolder: File
    private _dagFile: File

    /**
    *
    * @param templatesName The templatesName
    * @param chosenTemplateName The chosenTemplateName
    * @param templateFolder The templateFolder
    * @param dagFile The dagFile
    */
    constructor(templatesName: string[] = [], chosenTemplateName: string = '', templateFolder: File = new File([], "emptyFile", { type: 'application/zip' }), dagFile: File = new File([], "emptyFile", { type: 'application/zip' }),) {
        this._templatesName = templatesName
        this._chosenTemplateName = chosenTemplateName
        this._templateFolder = templateFolder
        this._dagFile = dagFile
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

    /**
     * set's the default values of the class (the values that will be used, if the constructor is called with no input)
     */
    public setDefaultValues() {
        this._templatesName = []
        this._chosenTemplateName = ''
        this._templateFolder = new File([], "emptyFile", { type: 'application/zip' })
        this._dagFile = new File([], "emptyFile", { type: 'application/zip' })
    }
}

export default CreateTemplate