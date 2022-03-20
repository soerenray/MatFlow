import { dataURLtoFileNoMime } from './base64Utility';
import Keys from './Keys';

class Template {
  private _dagDefinitionFileInBase64: File

  private _templateName: string

  /**
  *
  * @param dagDefinitionFileInBase64 The dagDefinitionFileInBase64
  * @param templateName The templateName
  */
  constructor(dagDefinitionFileInBase64: File, templateName: string) {
    this._dagDefinitionFileInBase64 = dagDefinitionFileInBase64;
    this._templateName = templateName;
  }

  /**
  * Gets the dagDefinitionFileInBase64
  * @returns _dagDefinitionFileInBase64
  */
  public get dagDefinitionFileInBase64(): File {
    return this._dagDefinitionFileInBase64;
  }

  /**
  * Sets the value of _dagDefinitionFileInBase64
  * @param dagDefinitionFileInBase64 The new value of _dagDefinitionFileInBase64
  */
  public set dagDefinitionFileInBase64(dagDefinitionFileInBase64: File) {
    this._dagDefinitionFileInBase64 = dagDefinitionFileInBase64;
  }

  /**
  * Sets the value of _templateName
  * @param templateName The new value of _templateName
  */
  public set templateName(templateName: string) {
    this._templateName = templateName;
  }

  /**
  * Gets the templateName
  * @returns _templateName
  */
  public get templateName(): string {
    return this._templateName;
  }

  /**
  * extracts JSON to Template object
  * @param JSONObj The JSON encoded Template
  * @returns Template object
  */
  public static createTemplateObjectFromJSON(JSONObj: string): Template {
    const parsed = JSON.parse(JSONObj);
    const decodedFile = dataURLtoFileNoMime(
      parsed[Keys.dag_definition_name],
      parsed[Keys.dag_save_path],
    );
    return new Template(decodedFile, parsed[Keys.template_name]);
  }
}

export default Template;
