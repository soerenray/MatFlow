import CreateTemplateMemento from "./CreateTemplateMemento"

class CreateTemplateCaretaker {
    private _createTemplateMementoObject: CreateTemplateMemento[] = []

    public addCreateTemplateMementoObjectToArray(createTemplateMementoObject: CreateTemplateMemento) {
        this._createTemplateMementoObject.push(createTemplateMementoObject)
    }
}

export default CreateTemplateCaretaker