class UserData {
    private _userName: string;

    private _userPassword: string;

    constructor(userName: string, userPassword: string) {
      this._userName = userName;
      this._userPassword = userPassword;
    }

    public get userName(): string {
      return this._userName;
    }

    public set userName(userName: string) {
      this._userName = userName;
    }

    public get userPassword(): string {
      return this._userPassword;
    }

    public set userPassword(userPassword: string) {
      this._userPassword = userPassword;
    }
}

export default UserData;
