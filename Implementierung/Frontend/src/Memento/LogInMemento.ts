import LogIn from "../Model/LogIn"

class LogInMemento {
    private _logInObject: LogIn

    constructor(logInObject: LogIn) {
        this._logInObject = logInObject
    }

    public get logInObject() {
        return this._logInObject
    }
}

export default LogInMemento