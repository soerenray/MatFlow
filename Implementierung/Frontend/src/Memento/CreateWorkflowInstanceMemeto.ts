import MementoInterface from './MementoInterface'
import CreateWorkflowInstance from '../Model/CreateWorkflowInstance'

class CreateWorkflowInstanceMemento implements MementoInterface {
    private _createWorkflowInstanceObject: CreateWorkflowInstance

    /**
    * Gets the createWorkflowInstanceObject
    * @returns _createWorkflowInstanceObject
    */
    public get createWorkflowInstanceObject(): CreateWorkflowInstance {
        return this._createWorkflowInstanceObject
    }
}

export default CreateWorkflowInstanceMemento