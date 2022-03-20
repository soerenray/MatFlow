import Keys from './Keys';

class Server {
    private _serverAddress: string

    private _serverStatus: string

    private _containerLimit: number

    private _selectedForExecution: boolean

    private _serverName: string

    private _serverResources: Array<[string, string]>

    /**
    *
    * @param serverAddress The serverAddress
    * @param serverStatus The serverStatus
    * @param containerLimit The containerLimit
    * @param selectedForExecution The selectedForExecution
    * @param serverName The serverName
    * @param serverResources The serverResources
    */
    constructor(
      serverAddress: string,
      serverStatus: string,
      containerLimit: number,
      selectedForExecution: boolean,
      serverName: string,
      serverResources: Array<[string, string]>,
    ) {
      this._serverAddress = serverAddress;
      this._serverStatus = serverStatus;
      this._containerLimit = containerLimit;
      this._selectedForExecution = selectedForExecution;
      this._serverName = serverName;
      this._serverResources = serverResources;
    }

    /**
    * Gets the serverAddress
    * @returns _serverAddress
    */
    public get serverAddress(): string {
      return this._serverAddress;
    }

    /**
    * Sets the value of _serverAddress
    * @param serverAddress The new value of _serverAddress
    */
    public set serverAddress(serverAddress: string) {
      this._serverAddress = serverAddress;
    }

    /**
    * Gets the serverStatus
    * @returns _serverStatus
    */
    public get serverStatus(): string {
      return this._serverStatus;
    }

    /**
    * Sets the value of _serverStatus
    * @param serverStatus The new value of _serverStatus
    */
    public set serverStatus(serverStatus: string) {
      this._serverStatus = serverStatus;
    }

    /**
    * Gets the containerLimit
    * @returns _containerLimit
    */
    public get containerLimit(): number {
      return this._containerLimit;
    }

    /**
    * Sets the value of _containerLimit
    * @param containerLimit The new value of _containerLimit
    */
    public set containerLimit(containerLimit: number) {
      this._containerLimit = containerLimit;
    }

    /**
    * Gets the selectedForExecution
    * @returns _selectedForExecution
    */
    public get selectedForExecution(): boolean {
      return this._selectedForExecution;
    }

    /**
    * Sets the value of _selectedForExecution
    * @param selectedForExecution The new value of _selectedForExecution
    */
    public set selectedForExecution(selectedForExecution: boolean) {
      this._selectedForExecution = selectedForExecution;
    }

    /**
    * Gets the serverName
    * @returns _serverName
    */
    public get serverName(): string {
      return this._serverName;
    }

    /**
    * Gets the serverResources
    * @returns _serverResources
    */
    public get serverResources(): Array<[string, string]> {
      return this._serverResources;
    }

    /**
    * Sets the value of _serverResources
    * @param serverResources The new value of _serverResources
    */
    public set serverResources(serverResources: Array<[string, string]>) {
      this._serverResources = serverResources;
    }

    /**
    * extracts JSON to Server object
    * @param JSONObj The JSON encoded server
    * @returns Server object
    */
    public static createServerObjectFromJSON(JSONObj: string): Server {
      const parsed = JSON.parse(JSONObj);
      return new Server(
        parsed.server_address_name,
        parsed[Keys.server_status_name],
        parsed[Keys.container_limit_name],
        parsed[Keys.selected_for_execution_name],
        parsed[Keys.server_name],
        parsed[Keys.server_resources_name],
      );
    }
}

export default Server;
