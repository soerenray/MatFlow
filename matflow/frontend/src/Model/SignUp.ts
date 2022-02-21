import SignUpMemento from "@Memento/SignUpMemento"

class SignUp {
    private _userName: string
    private _userPassword: string
    private _userPasswordRepeated: string
    private _showPassword: boolean
    private _showPasswordRepeated: boolean

    /**
    *
    * @param userName The userName
    * @param userPassword The userPassword
    * @param userPasswordRepeated The userPasswordRepeated
    * @param showPassword True if the password should be displayed in plain text otherwise false
    * @param showPasswordRepeated True if the repeated password should be displayed in plain text otherwise false
    */
    constructor(userName: string = '', userPassword: string = '', userPasswordRepeated: string = '', showPassword: boolean = false, showPasswordRepeated: boolean = false,) {
        this._userName = userName
        this._userPassword = userPassword
        this._userPasswordRepeated = userPasswordRepeated
        this._showPassword = showPassword
        this._showPasswordRepeated = showPasswordRepeated
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
    * Gets the showPassword
    * @returns _showPassword
    */
    public get showPassword(): boolean {
        return this._showPassword
    }

    /**
    * Gets the showPasswordRepeated
    * @returns _showPasswordRepeated
    */
    public get showPasswordRepeated(): boolean {
        return this._showPasswordRepeated
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
    * @param userPasswordRepeated The new value of _userPasswordRepeated
    */
    public set userPasswordRepeated(userPasswordRepeated: string) {
        this._userPasswordRepeated = userPasswordRepeated
    }

    /**
    * Sets the value of _showPassword
    * @param showPassword The new value of _showPassword
    */
    public set showPassword(showPassword: boolean) {
        this._showPassword = showPassword
    }

    /**
    * Sets the value of _showPasswordRepeated
    * @param showPasswordRepeated The new value of _showPasswordRepeated
    */
    public set showPasswordRepeated(showPasswordRepeated: boolean) {
        this._showPasswordRepeated = showPasswordRepeated
    }

    public setSignUpMemento(signUpMemento: SignUpMemento) {
        let tempSignUpObject = signUpMemento.signUpObject
        this.userName = tempSignUpObject.userName
        this.userPassword = tempSignUpObject.userPassword
        this.userPasswordRepeated = tempSignUpObject.userPasswordRepeated
    }

    public createSignUpMemento(): SignUpMemento {
        return new SignUpMemento(new SignUp(this.userName, this.userPassword, this.userPasswordRepeated))
    }
}

export default SignUp