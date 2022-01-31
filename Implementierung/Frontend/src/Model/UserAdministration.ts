import User from '../Classes/User'

class UserAdministration {
    private _tableHeaders: object[]
    private _users: User[]

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param users The users
    */
    constructor(tableHeaders: object[] = [], users: User[] = [],) {
        this._tableHeaders = tableHeaders
        this._users = users
    }

    /**
    * Gets the tableHeaders
    * @returns _tableHeaders
    */
    public get tableHeaders(): object[] {
        return this._tableHeaders
    }

    /**
    * Gets the users
    * @returns _users
    */
    public get users(): User[] {
        return this._users
    }

    /**
    * Sets the value of _tableHeaders
    * @param tableHeaders The new value of _tableHeaders
    */
    public set tableHeaders(tableHeaders: object[]) {
        this._tableHeaders = tableHeaders
    }

    /**
    * Sets the value of users
    * @param tableHeaders The new value of users
    */
    public set users(users: User[]) {
        this._users = users
    }
}

export default UserAdministration