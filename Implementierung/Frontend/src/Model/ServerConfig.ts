import Server from '../Classes/Server'

class ServerConfig {
    private _tableHeaders: object[]
    private _servers: Server[]

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param servers The servers
    */
    constructor(tableHeaders: object[], servers: Server[],) {
        this._tableHeaders = tableHeaders
        this._servers = servers
    }

    /**
    * Gets the tableHeaders
    * @returns _tableHeaders
    */
    public get tableHeaders(): object[] {
        return this._tableHeaders
    }

    /**
    * Gets the servers
    * @returns _servers
    */
    public get servers(): Server[] {
        return this._servers
    }


    /**
    * Sets the value of _tableHeaders
    * @param tableHeaders The new value of _tableHeaders
    */
    public set tableHeaders(tableHeaders: object[]) {
        this._tableHeaders = tableHeaders
    }

    /**
    * Sets the value of _servers
    * @param servers The new value of _servers
    */
    public set servers(servers: Server[]) {
        this._servers = servers
    }
}