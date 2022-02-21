import LogInMemento from "@Memento/LogInMemento"

class LogIn {
    private _userName: string
    private _userPassword: string
    private _showPassword: boolean

    /**
    *
    * @param userName The userName
    * @param userPassword The userPassword
    * @param showPassword true if password should be shown, otherwise false
    */
    constructor(userName: string = '', userPassword: string = '', showPassword: boolean = false) {
        this._userName = userName
        this._userPassword = userPassword
        this._showPassword = showPassword
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
    * Gets the showPassword
    * @returns _showPassword
    */
    public get showPassword(): boolean {
        return this._showPassword
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
    * Sets the value of _showPassword
    * @param showPassword The new value of _showPassword
    */
    public set showPassword(showPassword: boolean) {
        this._showPassword = showPassword
    }

    public setLogInMemento(logInMemento: LogInMemento) {
        let tempLogInObject = logInMemento.logInObject
        this.userName = tempLogInObject.userName
        this.userPassword = tempLogInObject.userPassword
        this.showPassword = tempLogInObject.showPassword
    }

    public createLogInMemento(): LogInMemento {
        return new LogInMemento(new LogIn(this.userName, this.userPassword, this.showPassword))
    }
}

export default LogIn