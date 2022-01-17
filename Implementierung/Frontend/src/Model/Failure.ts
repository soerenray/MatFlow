class Failure {
    private _failureMessage: string

    /**
    *
    * @param failureMessage The failureMessage
    */
    constructor(failureMessage: string,) {
        this._failureMessage = failureMessage
    }

    /**
    * Gets the failureMessage
    * @returns _failureMessage
    */
    public get failureMessage(): string {
        return this._failureMessage
    }


    /**
    * Sets the value of _failureMessage
    * @param failureMessage The new value of _failureMessage
    */
    public set failureMessage(failureMessage: string) {
        this._failureMessage = failureMessage
    }
}