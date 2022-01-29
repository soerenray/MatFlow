import User from '../Classes/User'

class UserAdministration {
    private _tableHeaders: object[]
    private _searchedUser: string
    private _users: User[]

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param searchedUser The searchedUser
    * @param users The users
    */
    constructor(tableHeaders: object[], searchedUser: string, users: User[],) {
        this._tableHeaders = tableHeaders
        this._searchedUser = searchedUser
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
    * Gets the searchedUser
    * @returns _searchedUser
    */
    public get searchedUser(): string {
        return this._searchedUser
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
    * Sets the value of _searchedUser
    * @param searchedUser The new value of _searchedUser
    */
    public set searchedUser(searchedUser: string) {
        this._searchedUser = searchedUser
    }

    /**
    * Sets the value of users
    * @param tableHeaders The new value of users
    */
    public set users(users: User[]) {
        this._users = users
    }
}