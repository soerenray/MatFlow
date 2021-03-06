import Keys from './Keys';

class Version {
  private _versionNumber: string

  private _versionNote: string

  private _parameterChanges: Array<[string, string]>

  /**
  *
  * @param versionNumber The versionNumber
  * @param versionNote The versionNote
  * @param parameterChanges The parameterChanges
  */
  constructor(versionNumber = '', versionNote = '', parameterChanges: Array<[string, string]> = []) {
    this._versionNumber = versionNumber;
    this._versionNote = versionNote;
    this._parameterChanges = parameterChanges;
  }

  /**
  * Gets the versionNumber
  * @returns _versionNumber
  */
  public get versionNumber(): string {
    return this._versionNumber;
  }

  /**
  * Sets the value of _versionNumber
  * @param versionNumber The new value of _versionNumber
  */
  public set versionNumber(versionNumber: string) {
    this._versionNumber = versionNumber;
  }

  /**
  * Gets the versionNote
  * @returns _versionNote
  */
  public get versionNote(): string {
    return this._versionNote;
  }

  /**
  * Sets the value of _versionNote
  * @param versionNote The new value of _versionNote
  */
  public set versionNote(versionNote: string) {
    this._versionNote = versionNote;
  }

  /**
  * Gets the parameterChanges
  * @returns _parameterChanges
  */
  public get parameterChanges(): Array<[string, string]> {
    return this._parameterChanges;
  }

  /**
  * Sets the value of _parameterChanges
  * @param parameterChanges The new value of _parameterChanges
  */
  public set parameterChanges(parameterChanges: Array<[string, string]>) {
    this._parameterChanges = parameterChanges;
  }

  /**
  * extracts JSON to Version object
  * @param JSONObj The JSON encoded Version
  * @returns Version object
  * */
  public static createVersionObjectFromJSON(JSONObj: string): Version {
    const parsed = JSON.parse(JSONObj);
    return new Version(
      parsed[Keys.version_number_name],
      parsed[Keys.version_note_name],
      parsed[Keys.frontend_versions_changes],
    );
  }
}

export default Version;
