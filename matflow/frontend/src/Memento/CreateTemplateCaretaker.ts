import CreateTemplateMemento from './CreateTemplateMemento';

class CreateTemplateCaretaker {
    private _createTemplateMementoObjects: CreateTemplateMemento[] = []

    public addCreateTemplateMementoObjectToArray(createTemplateMementoObject:
      CreateTemplateMemento) {
      this._createTemplateMementoObjects.push(createTemplateMementoObject);
    }

    public get createTemplateMementoObjects(): CreateTemplateMemento[] {
      return this._createTemplateMementoObjects;
    }
}

export default CreateTemplateCaretaker;
