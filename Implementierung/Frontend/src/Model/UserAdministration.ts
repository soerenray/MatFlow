class UserAdministration {
    private _tableHeaders: object[]
    private _searchedUser: string

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param searchedUser The searchedUser
    */
    constructor(tableHeaders: object[], searchedUser: string,) {
        this._tableHeaders = tableHeaders
        this._searchedUser = searchedUser
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
}