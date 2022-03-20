<template>
  <v-app class="ma-6">
    <div>
      <v-card>
        <v-table>
          <thead data-cy="tableHeader">
            <tr>
              <th v-for="header in tableHeaders" :key="header.value">
                {{ header.text }}
              </th>
            </tr>
          </thead>
          <tbody data-cy="tableBody">
            <tr v-for="server in servers" :key="server.name">
              <td>
                <v-text-field
                  variant="contained"
                  style="width: 200px"
                  v-model="server.serverName"
                ></v-text-field>
              </td>
              <td>
                <v-text-field
                  variant="contained"
                  style="width: 200px"
                  v-model="server.serverAddress"
                ></v-text-field>
              </td>
              <td>
                <v-text-field
                  variant="contained"
                  style="width: 150px"
                  v-model="server.serverStatus"
                ></v-text-field>
              </td>
              <td>
                <v-text-field
                  variant="contained"
                  style="width: 50px"
                  v-model="server.containerLimit"
                ></v-text-field>
              </td>
              <td>
                <v-checkbox
                  v-model="server.selectedForExecution"
                  disabled
                ></v-checkbox>
              </td>
              <td>
                <v-dialog
                  class="mx-auto mt-8"
                  width="700px"
                  v-model="resourcesDialog"
                >
                  <template v-slot:activator="{ props }">
                    <v-btn data-cy="serverResources" v-bind="props" icon>
                      <v-icon>mdi-memory</v-icon></v-btn
                    >
                  </template>
                  <v-table>
                    <thead>
                      <tr>
                        <th>
                          <v-btn variant="text" color="blue"> Key name </v-btn>
                        </th>
                        <th>
                          <v-btn variant="text" color="blue"> Value </v-btn>
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        data-cy="keyValuePairs"
                        v-for="(keyValuePair, index) in server.serverResources"
                        :key="index"
                      >
                        <td>
                          <v-text-field
                            v-model="keyValuePair[0]"
                            solo
                            variant="contained"
                            dense
                          ></v-text-field>
                        </td>
                        <td>
                          <v-text-field
                            v-model="keyValuePair[1]"
                            variant="contained"
                            dense
                          ></v-text-field>
                        </td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-dialog>
              </td>
              <td>
                <v-btn
                  data-cy="applyChanges"
                  @click="pushServerAndPullServers(server.serverName)"
                  color="green"
                  outlined
                  >apply changes</v-btn
                >
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card>
    </div>
  </v-app>
</template>
<script lang="ts">
// @ts-nocheck
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';
import ServerConfig from '@Model/ServerConfig';
import Server from '@Classes/Server';

export default {
  name: 'ServerConfig',
  data() {
    return {
      backendServerCommunicatorObject: new BackendServerCommunicator(),
      serverConfigObject: new ServerConfig(
        [
          { text: 'Server location name', value: 'serverName' },
          { text: 'Address', value: 'serverAddress' },
          { text: 'Status', value: 'serverStatus' },
          { text: 'Container limit', value: 'containerLimit' },
          {
            text: 'Select server for execution',
            value: 'selectedForExecution',
          },
          { text: 'Configurate server resources', value: 'serverResources' },
          { text: 'apply changes', value: 'apply' },
        ],
        [],
        false,
      ),
    };
  },
  methods: {
    pushServerAndPullServers(serverName: string) {
      this.pushServer(serverName);
      this.pullServers();
    },
    async pullServers() {
      this.servers = await this.backendServerCommunicatorObject.pullServers();
    },
    pushServer(serverName: string) {
      this.backendServerCommunicatorObject.pushServer(
        this.findServerByServerName(this.servers, serverName),
      );
    },
    findServerByServerName(servers: Server[], serverName: string): Server {
      const serverIndex = servers.findIndex((server: Server) => server.serverName === serverName);
      if (serverIndex === -1) {
        throw Error(`No server with the name ${serverName} was found`);
      }
      return servers[serverIndex];
    },
  },
  computed: {
    tableHeaders: {
      get(): object[] {
        return this.serverConfigObject.tableHeaders;
      },
      set(tableHeaders: object[]) {
        this.serverConfigObject.tableHeaders = tableHeaders;
      },
    },
    servers: {
      get(): Server[] {
        return this.serverConfigObject.servers;
      },
      set(servers: Server[]) {
        this.serverConfigObject.servers = servers;
      },
    },
    resourcesDialog: {
      get(): boolean {
        return this.serverConfigObject.resourcesDialog;
      },
      set(resourcesDialog: boolean) {
        this.serverConfigObject.resourcesDialog = resourcesDialog;
      },
    },
  },
  async created() {
    this.servers = await this.backendServerCommunicatorObject.pullServers();
  },
};
</script>
