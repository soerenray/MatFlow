import User from '../Classes/User'

class UserAdministration {
    private _tableHeaders: object[]
    private _users: User[]
    private _selectStatuses: string[]
    private _selectPrivileges: string[]

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param users The users
    * @param selectStatues The selectStatuses
    * @param selectPriviliges The selectPrivliges
    */
    constructor(tableHeaders: object[] = [], users: User[] = [], selectStatuses: string[] = [], selectPrivileges: string[] = [],) {
        this._tableHeaders = tableHeaders
        this._users = users
        this._selectStatuses = selectStatuses
        this._selectPrivileges = selectPrivileges
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
    * Gets the selectStatuses
    * @returns _selectStatuses
    */
    public get selectStatuses(): string[] {
        return this._selectStatuses
    }

    /**
    * Gets the selectPrivileges
    * @returns _selectPrivileges
    */
    public get selectPrivileges(): string[] {
        return this._selectPrivileges
    }

    /**
    * Sets the value of _tableHeaders
    * @param tableHeaders The new value of _tableHeaders
    */
    public set tableHeaders(tableHeaders: object[]) {
        this._tableHeaders = tableHeaders
    }

    /**
    * Sets the value of _users
    * @param users The new value of users
    */
    public set users(users: User[]) {
        this._users = users
    }

    /**
    * Sets the value of _selectStatuses
    * @param selectStatuses The new value of _selectStatuses
    */
    public set selectStatuses(selectStatuses: string[]) {
        this._selectStatuses = selectStatuses
    }

    /**
    * Sets the value of _selectPrivileges
    * @param selectPrivileges The new value of selectPrivileges
    */
    public set selectPrivileges(selectPrivileges: string[]) {
        this._selectPrivileges = selectPrivileges
    }
}

export default UserAdministration