import CreateTemplateMemento from '@Memento/CreateTemplateMemento';

class CreateTemplate {
    private _newTemplateName: string

    private _templatesName: string[]

    private _chosenTemplateName: string

    private _dagFile: File

    private _openEdit: boolean

    private _tempTextFile: string

    /**
    *
    * @param newTemplateName The newTemplateName
    * @param templatesName The templatesName
    * @param chosenTemplateName The chosenTemplateName
    * @param dagFile The dagFile
    * @param openEdit openEdit
    * @param tempTextFile Is need to write text from the dagFile temporary
    */
    constructor(
      newTemplateName = '',
      templatesName: string[] = [],
      chosenTemplateName = '',
      dagFile: File = new File([], 'emptyFile', { type: 'file' }),
      openEdit = false,
      tempTextFile = '',
    ) {
      this._newTemplateName = newTemplateName;
      this._templatesName = templatesName;
      this._chosenTemplateName = chosenTemplateName;
      this._dagFile = dagFile;
      this._openEdit = openEdit;
      this._tempTextFile = tempTextFile;
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
    * Gets the openEdit
    * @returns _openEdit
    */
    public get openEdit(): boolean {
      return this._openEdit;
    }

    /**
    * Sets the value of _openEdit
    * @param openEdit The new value of _openEdit
    */
    public set openEdit(openEdit: boolean) {
      this._openEdit = openEdit;
    }

    /**
    * Gets the tempTextFile
    * @returns _tempTextFile
    */
    public get tempTextFile(): string {
      return this._tempTextFile;
    }

    /**
    * Sets the value of _tempTextFile
    * @param tempTextFile The new value of _tempTextFile
    */
    public set tempTextFile(tempTextFile: string) {
      this._tempTextFile = tempTextFile;
    }

    public setCreateTemplateMemento(createTemplateMemento: CreateTemplateMemento) {
      const tempCreateTemplateMementoObject = createTemplateMemento.createtTemplateObject;
      this.newTemplateName = tempCreateTemplateMementoObject.newTemplateName;
      this.templatesName = tempCreateTemplateMementoObject.templatesName;
      this.chosenTemplateName = tempCreateTemplateMementoObject.chosenTemplateName;
      this.dagFile = tempCreateTemplateMementoObject.dagFile;
      this.openEdit = tempCreateTemplateMementoObject.openEdit;
      this.tempTextFile = tempCreateTemplateMementoObject.tempTextFile;
    }

    public createTemplateMemento(): CreateTemplateMemento {
      return new CreateTemplateMemento(new CreateTemplate(
        this.newTemplateName,
        this.templatesName,
        this.chosenTemplateName,
        this.dagFile,
        this.openEdit,
        this.tempTextFile,
      ));
    }
}

export default CreateTemplate;
