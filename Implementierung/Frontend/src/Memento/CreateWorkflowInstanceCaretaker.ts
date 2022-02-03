import CreateWorkflowInstance from "../Model/CreateWorkflowInstance"

class CreateWorkflowInstanceCaretaker {
    private _createWorkflowInstanceObjects: CreateWorkflowInstance[] = []

    public addCreateWorkflowInstanceObjectToArray(createWorkflowInstanceObject: CreateWorkflowInstance) {
        this._createWorkflowInstanceObjects.push(createWorkflowInstanceObject)
    }

    public get createWorkflowInstanceObjects(): CreateWorkflowInstance[] {
        return this._createWorkflowInstanceObjects
    }
}

export default CreateWorkflowInstanceCaretaker