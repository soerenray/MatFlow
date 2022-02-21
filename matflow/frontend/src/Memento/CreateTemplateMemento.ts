import CreateTemplate from "@Model/CreateTemplate"

class CreateTemplateMemento {
    private _createTemplateObject: CreateTemplate

    constructor(createTemplateObject: CreateTemplate) {
        this._createTemplateObject = createTemplateObject
    }

    /**
    * Gets the createtTemplateObject
    * @returns _createtTemplateObject
    */
    public get createtTemplateObject(): CreateTemplate {
        return this._createTemplateObject
    }
}

export default CreateTemplateMemento