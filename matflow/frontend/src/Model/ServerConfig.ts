import Server from '@Classes/Server';

class ServerConfig {
    private _tableHeaders: object[]

    private _servers: Server[]

    private _resourcesDialog: boolean

    /**
    *
    * @param tableHeaders The tableHeaders
    * @param servers The servers
    * @param resourcesDialog The resourcesDialog
    */
    constructor(tableHeaders: object[], servers: Server[], resourcesDialog: boolean) {
      this._tableHeaders = tableHeaders;
      this._servers = servers;
      this._resourcesDialog = resourcesDialog;
    }

    /**
    * Gets the tableHeaders
    * @returns _tableHeaders
    */
    public get tableHeaders(): object[] {
      return this._tableHeaders;
    }

    /**
    * Sets the value of _tableHeaders
    * @param tableHeaders The new value of _tableHeaders
    */
    public set tableHeaders(tableHeaders: object[]) {
      this._tableHeaders = tableHeaders;
    }

    /**
    * Gets the servers
    * @returns _servers
        */
    public get servers(): Server[] {
      return this._servers;
    }

    /**
    * Sets the value of _servers
    * @param servers The new value of _servers
    */
    public set servers(servers: Server[]) {
      this._servers = servers;
    }

    /**
    * Gets the resourcesDialog
    * @returns _resourcesDialog
    */
    public get resourcesDialog(): boolean {
      return this._resourcesDialog;
    }

    /**
    * Sets the value of _resourcesDialog
    * @param resourcesDialog The new value of _resourcesDialog
    */
    public set resourcesDialog(resourcesDialog: boolean) {
      this._resourcesDialog = resourcesDialog;
    }
}

export default ServerConfig;
