class Approval {
    private _approvalMessage: string

    /**
    *
    * @param approvalMessage The approvalMessage
    */
    constructor(approvalMessage: string,) {
        this._approvalMessage = approvalMessage
    }

    /**
    * Gets the approvalMessage
    * @returns _approvalMessage
    */
    public get approvalMessage(): string {
        return this._approvalMessage
    }

    /**
    * Sets the value of _approvalMessage
    * @param approvalMessage The new value of _approvalMessage
    */
    public set approvalMessage(approvalMessage: string) {
        this._approvalMessage = approvalMessage
    }
}