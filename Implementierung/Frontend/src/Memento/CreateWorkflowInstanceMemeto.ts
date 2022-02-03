import MementoInterface from './MementoInterface'
import CreateWorkflowInstance from '../Model/CreateWorkflowInstance'

class CreateWorkflowInstanceMemento implements MementoInterface {
    private _createWorkflowInstanceObject: CreateWorkflowInstance

    public setState(): void {

    }

    public getState(): CreateWorkflowInstance {
    }

    private set createWorkflowInstanceObject(createWorkflowInstanceObject: CreateWorkflowInstance) {
        this._createWorkflowInstanceObject = createWorkflowInstanceObject
    }

    private get createWorkflowInstanceObject(): CreateWorkflowInstance {
        return this._createWorkflowInstanceObject
    }
}

export default CreateWorkflowInstanceMemento