import CreateTemplateMemento from '@Memento/CreateTemplateMemento';

class CreateTemplate {
    private _newTemplateName: string

    private _templatesName: string[]

    private _chosenTemplateName: string

    private _dagFile: File

    private _createFromEmptyFile: boolean

    /**
    *
    * @param newTemplateName The newTemplateName
    * @param templatesName The templatesName
    * @param chosenTemplateName The chosenTemplateName
    * @param dagFile The dagFile
    * @param createFromEmptyFile createFromEmptyFile
    */
    constructor(
      newTemplateName = '',
      templatesName: string[] = [],
      chosenTemplateName = '',
      dagFile: File = new File([], 'emptyFile', { type: 'file' }),
      createFromEmptyFile = false,
    ) {
      this._newTemplateName = newTemplateName;
      this._templatesName = templatesName;
      this._chosenTemplateName = chosenTemplateName;
      this._dagFile = dagFile;
      this._createFromEmptyFile = createFromEmptyFile;
    }

    /**
    * Gets the newTemplateName
    * @returns _newTemplateName
    */
    public get newTemplateName(): string {
      return this._newTemplateName;
    }

    /**
    * Sets the value of _newTemplateName
    * @param newTemplateName The new value of _newTemplateName
    */
    public set newTemplateName(newTemplateName: string) {
      this._newTemplateName = newTemplateName;
    }

    /**
    * Gets the templatesName
    * @returns _templatesName
    */
    public get templatesName(): string[] {
      return this._templatesName;
    }

    /**
    * Sets the value of _templatesName
    * @param templatesName The new value of _templatesName
    */
    public set templatesName(templatesName: string[]) {
      this._templatesName = templatesName;
    }

    /**
    * Gets the dagFile
    * @returns _dagFile
    */
    public get dagFile(): File {
      return this._dagFile;
    }

    /**
    * Sets the value of _dagFile
    * @param dagFile The new value of _dagFile
    */
    public set dagFile(dagFile: File) {
      this._dagFile = dagFile;
    }

    /**
    * Gets the chosenTemplateName
    * @returns _chosenTemplateName
    */
    public get chosenTemplateName(): string {
      return this._chosenTemplateName;
    }

    /**
    * Sets the value of _chosenTemplateName
    * @param chosenTemplateName The new value of _chosenTemplateName
    */
    public set chosenTemplateName(chosenTemplateName: string) {
      this._chosenTemplateName = chosenTemplateName;
    }

    /**
    * Gets the createFromEmptyFile
    * @returns _createFromEmptyFile
    */
    public get createFromEmptyFile(): boolean {
      return this._createFromEmptyFile;
    }

    /**
    * Sets the value of _createFromEmptyFile
    * @param createFromEmptyFile The new value of _createFromEmptyFile
    */
    public set createFromEmptyFile(createFromEmptyFile: boolean) {
      this._createFromEmptyFile = createFromEmptyFile;
    }

    public setCreateTemplateMemento(createTemplateMemento: CreateTemplateMemento) {
      const tempCreateTemplateMementoObject = createTemplateMemento.createtTemplateObject;
      this.newTemplateName = tempCreateTemplateMementoObject.newTemplateName;
      this.templatesName = tempCreateTemplateMementoObject.templatesName;
      this.chosenTemplateName = tempCreateTemplateMementoObject.chosenTemplateName;
      this.dagFile = tempCreateTemplateMementoObject.dagFile;
      this.createFromEmptyFile = tempCreateTemplateMementoObject.createFromEmptyFile;
    }

    public createTemplateMemento(): CreateTemplateMemento {
      return new CreateTemplateMemento(new CreateTemplate(
        this.newTemplateName,
        this.templatesName,
        this.chosenTemplateName,
        this.dagFile,
        this.createFromEmptyFile,
      ));
    }
}

export default CreateTemplate;
