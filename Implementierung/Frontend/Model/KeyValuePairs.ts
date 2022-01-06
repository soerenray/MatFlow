class KeyValuePairs {
    private _keyValuePairs: string[][]

    /**
    *
    * @param keyValuePairs The keyValuePairs
    */
    constructor(keyValuePairs: string[][],) {
        this._keyValuePairs = keyValuePairs
    }

    /**
    * Gets the keyValuePairs
    * @returns _keyValuePairs
    */
    public get keyValuePairs(): string[][] {
        return this._keyValuePairs
    }


    /**
    * Sets the value of _keyValuePairs
    * @param keyValuePairs The new value of _keyValuePairs
    */
    public set keyValuePairs(keyValuePairs: string[][]) {
        this._keyValuePairs = keyValuePairs
    }
}