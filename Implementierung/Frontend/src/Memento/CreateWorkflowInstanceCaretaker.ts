import CreateWorkflowInstance from "../Model/CreateWorkflowInstance"

class CreateWorkflowInstanceCaretaker {
    private _createWorkflowInstanceObjects: CreateWorkflowInstance[] = []

    public addCreateWorkflowInstanceObjectToArray(createWorkflowInstanceObject: CreateWorkflowInstance) {
        this._createWorkflowInstanceObjects.push(createWorkflowInstanceObject)
    }

    public get createWorkflowInstanceObjectSet(): CreateWorkflowInstance[] {
        return this._createWorkflowInstanceObjects
    }
}

export default CreateWorkflowInstanceCaretaker