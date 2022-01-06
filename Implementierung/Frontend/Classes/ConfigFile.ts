class ConfigFile {
    private _configFileName: string
    private _keyValuePairs: [string, string]

    /**
    *
    * @param configFileName The configFileName
    * @param keyValuePairs The keyValuePairs
    */
    constructor(configFileName: string, keyValuePairs: [string, string],) {
        this._configFileName = configFileName
        this._keyValuePairs = keyValuePairs
    }

    /**
    * Gets the configFileName
    * @returns _configFileName
    */
    public get configFileName(): string {
        return this._configFileName
    }

    /**
    * Gets the keyValuePairs
    * @returns _keyValuePairs
    */
    public get keyValuePairs(): [string, string] {
        return this._keyValuePairs
    }


    /**
    * Sets the value of _configFileName
    * @param configFileName The new value of _configFileName
    */
    public set configFileName(configFileName: string) {
        this._configFileName = configFileName
    }

    /**
    * Sets the value of _keyValuePairs
    * @param keyValuePairs The new value of _keyValuePairs
    */
    public set keyValuePairs(keyValuePairs: [string, string]) {
        this._keyValuePairs = keyValuePairs
    }
}