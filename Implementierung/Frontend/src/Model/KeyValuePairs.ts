class KeyValuePairs {
    private _headers: string[]

    /**
    *
    * @param headers The headers
    */
    constructor(headers: string[],) {
        this._headers = headers
    }

    /**
    * Gets the headers
    * @returns _headers
    */
    public get headers(): string[] {
        return this._headers
    }


    /**
    * Sets the value of _headers
    * @param headers The new value of _headers
    */
    public set headers(headers: string[]) {
        this._headers = headers
    }
}

export default KeyValuePairs