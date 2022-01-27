import Server from '../Classes/Server'

class ServerConfig {
    private _tableHeaders: object[]
    private _servers: Server[]
    private _serverName: string
    private _serverAddres: string

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param servers The servers
    * @param serverName The serverName
    * @param serverAddres The serverAddres
    */
    constructor(tableHeaders: object[], servers: Server[], serverName: string, serverAddres: string,) {
        this._tableHeaders = tableHeaders
        this._servers = servers
        this._serverName = serverName
        this._serverAddres = serverAddres
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
    * Gets the serverName
    * @returns _serverName
    */
    public get serverName(): string {
        return this._serverName
    }

    /**
    * Gets the serverAddres
    * @returns _serverAddres
    */
    public get serverAddres(): string {
        return this._serverAddres
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

    /**
    * Sets the value of _serverName
    * @param serverName The new value of _serverName
    */
    public set serverName(serverName: string) {
        this._serverName = serverName
    }

    /**
    * Sets the value of _serverAddres
    * @param serverAddres The new value of _serverAddres
    */
    public set serverAddres(serverAddres: string) {
        this._serverAddres = serverAddres
    }
}