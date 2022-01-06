class SignUp {
    private _userName: string
    private _userPassword: string

    /**
    *
    * @param userName The userName
    * @param userPassword The userPassword
    */
    constructor(userName: string, userPassword: string,) {
        this._userName = userName
        this._userPassword = userPassword
    }

    /**
    * Gets the userName
    * @returns _userName
    */
    public get userName(): string {
        return this._userName
    }

    /**
    * Gets the userPassword
    * @returns _userPassword
    */
    public get userPassword(): string {
        return this._userPassword
    }


    /**
    * Sets the value of _userName
    * @param userName The new value of _userName
    */
    public set userName(userName: string) {
        this._userName = userName
    }

    /**
    * Sets the value of _userPassword
    * @param userPassword The new value of _userPassword
    */
    public set userPassword(userPassword: string) {
        this._userPassword = userPassword
    }
}