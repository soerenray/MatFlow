class SignUp {
    private _userName: string
    private _userPassword: string
    private _userPasswordRepeated: string

    /**
    *
    * @param userName The userName
    * @param userPassword The userPassword
    * @param userPasswordRepeated The userPasswordRepeated
    */
    constructor(userName: string = '', userPassword: string = '', userPasswordRepeated: string = '',) {
        this._userName = userName
        this._userPassword = userPassword
        this._userPasswordRepeated = userPasswordRepeated
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
    * Gets the userPasswordRepeated
    * @returns _userPasswordRepeated
    */
     public get userPasswordRepeated(): string {
        return this._userPasswordRepeated
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

    /**
    * Sets the value of _userPasswordRepeated
    * @param userPassword The new value of _userPasswordRepeated
    */
     public set userPasswordRepeated(userPasswordRepeated: string) {
        this._userPasswordRepeated = userPasswordRepeated
    }
}

export default SignUp