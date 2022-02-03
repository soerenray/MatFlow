import CreateWorkflowInstanceMemento from "./CreateWorkflowInstanceMemeto"

class CreateWorkflowInstanceCaretaker {
    private _createWorkflowInstanceMementoObjects: CreateWorkflowInstanceMemento[] = []

    public addCreateWorkflowInstanceMementoObjectToArray(createWorkflowInstanceMementoObject: CreateWorkflowInstanceMemento) {
        this._createWorkflowInstanceMementoObjects.push(createWorkflowInstanceMementoObject)
    }

    public get createWorkflowInstanceMementoObjects(): CreateWorkflowInstanceMemento[] {
        return this._createWorkflowInstanceMementoObjects
    }
}

export default CreateWorkflowInstanceCaretaker