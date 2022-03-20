import Keys from '@Classes/Keys';

class User {
  private _userName: string

  private _userStatus: boolean

  private _userPrivilege: string

  /**
  *
  * @param userName The userName
  * @param userStatus The userStatus
  * @param userPrivilege The userPrivilege
  */
  constructor(userName: string, userStatus: boolean, userPrivilege: string) {
    this._userName = userName;
    this._userStatus = userStatus;
    this._userPrivilege = userPrivilege;
  }

  /**
  * Gets the userName
  * @returns _userName
  */
  public get userName(): string {
    return this._userName;
  }

  /**
  * Sets the value of _userName
  * @param userName The new value of _userName
  */
  public set userName(userName: string) {
    this._userName = userName;
  }

  /**
  * Gets the userStatus
  * @returns _userStatus
  */
  public get userStatus(): boolean {
    return this._userStatus;
  }

  /**
  * Sets the value of _userStatus
  * @param userStatus The new value of _userStatus
  */
  public set userStatus(userStatus: boolean) {
    this._userStatus = userStatus;
  }

  /**
  * Gets the userPrivilege
  * @returns _userPrivilege
  */
  public get userPrivilege(): string {
    return this._userPrivilege;
  }

  /**
  * Sets the value of _userPrivilege
  * @param userPrivilege The new value of _userPrivilege
  */
  public set userPrivilege(userPrivilege: string) {
    this._userPrivilege = userPrivilege;
  }

  /**
  * extracts JSON to User object
  * @param JSONObj The JSON encoded User
  * @returns User object
  * */
  public static createUserObjectFromJSON(JSONObj: string): User {
    const parsed = JSON.parse(JSONObj);
    return new User(
      parsed[Keys.user_name],
      parsed[Keys.user_status_name],
      parsed[Keys.user_privilege_name],
    );
  }
}

export default User;
