import MementoInterface from './MementoInterface'
import CreateWorkflowInstance from '../Model/CreateWorkflowInstance'

class CreateWorkflowInstanceMemento implements MementoInterface {
    private _createWorkflowInstanceObject: CreateWorkflowInstance

    /**
    * Gets the createWorkflowInstanceObject
    * @returns _createWorkflowInstanceObject
    */
    private get createWorkflowInstanceObject(): CreateWorkflowInstance {
        return this._createWorkflowInstanceObject
    }

    /**
    * Sets the value of _createWorkflowInstanceObject
    * @param createWorkflowInstanceObject The new value of _createWorkflowInstanceObject
    */
    private set createWorkflowInstanceObject(createWorkflowInstanceObject: CreateWorkflowInstance) {
        this._createWorkflowInstanceObject = createWorkflowInstanceObject
    }
}

export default CreateWorkflowInstanceMemento