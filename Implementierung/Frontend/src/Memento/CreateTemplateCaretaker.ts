import CreateTemplateMemento from "./CreateTemplateMemento"

class CreateTemplateCaretaker {
    private _createTemplateMementoObject: CreateTemplateMemento[] = []

    public addCreateTemplateMementoObjectToArray(createTemplateMementoObject: CreateTemplateMemento) {
        this._createTemplateMementoObject.push(createTemplateMementoObject)
    }

    public get createTemplateMementoObject(): CreateTemplateMemento[] {
        return this._createTemplateMementoObject
    }
}

export default CreateTemplateCaretaker