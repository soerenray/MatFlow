import SignUp from "@Model/SignUp";

class SignUpMemento {
    private _signUpObject: SignUp

    constructor(signUpObject: SignUp) {
        this._signUpObject = signUpObject
    }

    public get signUpObject(): SignUp {
        return this._signUpObject
    }
}

export default SignUpMemento