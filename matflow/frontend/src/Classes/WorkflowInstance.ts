import { dataURLtoFileNoMime } from './base64Utility';
import Keys from './Keys';
import Template from './Template';

class WorkflowInstance extends Template {
    private _versionsNumbers: string[]

    private _activeVersionNumber: string

    /**
    *
    * @param dagDefinitionFile The dagDefinitionFile
    * @param templateName The templateName
    * @param versionsNumbers The versionsNumbers
    * @param activeVersionNumber The activeVersionNumber
    */
    constructor(dagDefinitionFile: File = new File([], 'emptyFile', { type: 'application/zip' }), templateName = '', versionsNumbers: string[] = [], activeVersionNumber = '') {
      super(dagDefinitionFile, templateName);
      this._versionsNumbers = versionsNumbers;
      this._activeVersionNumber = activeVersionNumber;
    }

    /**
    * Gets the versionsNumbers
    * @returns _versionsNumbers
    */
    public get versionsNumbers(): string[] {
      return this._versionsNumbers;
    }

    /**
    * Sets the value of _versionsNumbers
    * @param versionsNumbers The new value of _versionsNumbers
    */
    public set versionsNumbers(versionsNumbers: string[]) {
      this._versionsNumbers = versionsNumbers;
    }

    /**
    * Gets the activeVersionNumber
    * @returns _activeVersionNumber
    */
    public get activeVersionNumber(): string {
      return this._activeVersionNumber;
    }

    /**
    * Sets the value of _activeVersionNumber
    * @param activeVersionNumber The new value of _activeVersionNumber
    */
    public set activeVersionNumber(activeVersionNumber: string) {
      this._activeVersionNumber = activeVersionNumber;
    }

    /**
    * extracts JSON to User object
    * @param JSONObj The JSON encoded User
    * @returns User object
    * */
    public static createWorkflowInstanceObjectFromJSON(JSONObj: string): WorkflowInstance {
      const parsed = JSON.parse(JSONObj);
      const dagFile: File = dataURLtoFileNoMime(
        parsed[Keys.dag_definition_name],
        parsed[Keys.dag_save_path],
      );
      return new WorkflowInstance(
        dagFile,
        parsed[Keys.template_name],
        parsed[Keys.versions_name],
        parsed[Keys.version_number_name],
      );
    }
}

export default WorkflowInstance;
