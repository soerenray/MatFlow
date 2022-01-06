class User {
    private _userName: string
    private _userStatus: string
    private _userPrivilege: string

    /**
    *
    * @param userName The userName
    * @param userStatus The userStatus
    * @param userPrivilege The userPrivilege
    */
    constructor(userName: string, userStatus: string, userPrivilege: string,) {
        this._userName = userName
        this._userStatus = userStatus
        this._userPrivilege = userPrivilege
    }

    /**
    * Gets the userName
    * @returns _userName
    */
    public get userName(): string {
        return this._userName
    }

    /**
    * Gets the userStatus
    * @returns _userStatus
    */
    public get userStatus(): string {
        return this._userStatus
    }

    /**
    * Gets the userPrivilege
    * @returns _userPrivilege
    */
    public get userPrivilege(): string {
        return this._userPrivilege
    }


    /**
    * Sets the value of _userName
    * @param userName The new value of _userName
    */
    public set userName(userName: string) {
        this._userName = userName
    }

    /**
    * Sets the value of _userStatus
    * @param userStatus The new value of _userStatus
    */
    public set userStatus(userStatus: string) {
        this._userStatus = userStatus
    }

    /**
    * Sets the value of _userPrivilege
    * @param userPrivilege The new value of _userPrivilege
    */
    public set userPrivilege(userPrivilege: string) {
        this._userPrivilege = userPrivilege
    }
}