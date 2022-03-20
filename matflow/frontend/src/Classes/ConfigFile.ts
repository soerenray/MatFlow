import Keys from './Keys';

class ConfigFile {
  private _configFileName: string

  private _keyValuePairs: Array<[string, string]>

  /**
  *
  * @param configFileName The configFileName
  * @param keyValuePairs The keyValuePairs
  */
  constructor(configFileName = '', keyValuePairs: Array<[string, string]> = []) {
    this._configFileName = configFileName;
    this._keyValuePairs = keyValuePairs;
  }

  /**
  * Gets the configFileName
  * @returns _configFileName
  */
  public get configFileName(): string {
    return this._configFileName;
  }

  /**
      * Sets the value of _configFileName
      * @param configFileName The new value of _configFileName
      */
  public set configFileName(configFileName: string) {
    this._configFileName = configFileName;
  }

  /**
  * Gets the keyValuePairs
  * @returns _keyValuePairs
  */
  public get keyValuePairs(): Array<[string, string]> {
    return this._keyValuePairs;
  }

  /**
  * Sets the value of _keyValuePairs
  * @param keyValuePairs The new value of _keyValuePairs
  */
  public set keyValuePairs(keyValuePairs: Array<[string, string]>) {
    this._keyValuePairs = keyValuePairs;
  }

  /**
  * extracts JSON to ConfigFile object
  * @param JSONObj The JSON encoded ConfigFile
  * @returns ConfigFile object
  * */
  public static createConfigFileObjectFromJSON(JSONObj: string): ConfigFile {
    const parsed = JSON.parse(JSONObj);
    return new ConfigFile(parsed[Keys.config_file_name], parsed[Keys.key_value_pairs_name]);
  }
}

export default ConfigFile;
