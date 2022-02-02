class KeyValuePairs {
    private _headers: object[]

    /**
    *
    * @param headers The headers
    */
    constructor(headers: object[],) {
        this._headers = headers
    }

    /**
    * Gets the headers
    * @returns _headers
    */
    public get headers(): object[] {
        return this._headers
    }


    /**
    * Sets the value of _headers
    * @param headers The new value of _headers
    */
    public set headers(headers: object[]) {
        this._headers = headers
    }
}

export default KeyValuePairs