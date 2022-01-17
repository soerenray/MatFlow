import Version from '../Classes/Version'

class VersionControl {
    private _tableHeaders: object[]
    private _versions: Version[]

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param versions The versions
    */
    constructor(tableHeaders: object[], versions: Version[],) {
        this._tableHeaders = tableHeaders
        this._versions = versions
    }

    /**
    * Gets the tableHeaders
    * @returns _tableHeaders
    */
    public get tableHeaders(): object[] {
        return this._tableHeaders
    }

    /**
    * Gets the versions
    * @returns _versions
    */
    public get versions(): Version[] {
        return this._versions
    }


    /**
    * Sets the value of _tableHeaders
    * @param tableHeaders The new value of _tableHeaders
    */
    public set tableHeaders(tableHeaders: object[]) {
        this._tableHeaders = tableHeaders
    }

    /**
    * Sets the value of _versions
    * @param versions The new value of _versions
    */
    public set versions(versions: Version[]) {
        this._versions = versions
    }
}