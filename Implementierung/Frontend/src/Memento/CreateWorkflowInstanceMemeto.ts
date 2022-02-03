import CreateWorkflowInstance from '../Model/CreateWorkflowInstance'

class CreateWorkflowInstanceMemento {
    private _createWorkflowInstanceObject: CreateWorkflowInstance

    constructor(createWorkflowInstanceObject: CreateWorkflowInstance) {
        this._createWorkflowInstanceObject = createWorkflowInstanceObject
    }

    /**
    * Gets the createWorkflowInstanceObject
    * @returns _createWorkflowInstanceObject
    */
    public get createWorkflowInstanceObject(): CreateWorkflowInstance {
        return this._createWorkflowInstanceObject
    }
}

export default CreateWorkflowInstanceMemento