<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 20px">
      <v-data-table
        :headers="tableHeaders"
        :items="servers"
        item-key="serverName"
      >// servers = [new Server(
        //                 "123.123.11.1",
        //                 "running",
        //                 5,
        //                 true,
        //                 "kit-materialwissenschaften",
        //                 [["cpu1", "50%"]]
        //             )]
        
        <template v-slot:[`item.containerLimit`]="{ item }"
          ><v-text-field v-model="item.containerLimit"></v-text-field
        ></template>
        <template v-slot:[`item.selectedForExecution`]="{}"
          ><v-checkbox disabled></v-checkbox
        ></template>
        <template v-slot:[`item.serverResources`]="{ item }">
          <v-dialog width="700px" v-model="resourcesDialog">
            <template v-slot:activator="{ on, attrs }">
              <v-btn v-on="on" v-bind="attrs" icon
                ><memory-icon></memory-icon
              ></v-btn>
            </template>
            <div style="width: 700px">
              <v-card>
                <v-row>
                  <v-col>
                    <v-row style="padding-top: 10px">
                      <div>
                        <v-btn text color="primary"> Key name </v-btn>
                      </div>
                      <v-spacer></v-spacer>
                      <div style="padding-right: 290px">
                        <v-btn text color="primary"> Value </v-btn>
                      </div>
                    </v-row>
                  </v-col>
                  <v-col>
                    <v-card
                      v-for="(keyValuePair, index) in item.serverResources"
                      :key="index"
                    >
                      <v-row>
                        <div style="padding-top: 15px; padding-left: 20px">
                          <v-text-field
                            v-model="keyValuePair[0]"
                            solo
                            dense
                          ></v-text-field>
                        </div>
                        <v-spacer></v-spacer>
                        <div style="padding-top: 15px; padding-right: 50px">
                          <v-text-field
                            v-model="keyValuePair[1]"
                            style="width: 400px"
                            dense
                          ></v-text-field>
                        </div>
                      </v-row>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card>
            </div>
          </v-dialog>
        </template>
        <template v-slot:[`item.apply`]="{ item }"
          ><v-btn
            @click="pushServerAndPullServers(item.serverName)"
            color="green"
            outlined
            >apply changes</v-btn
          ></template
        >
      </v-data-table>
    </div>
  </v-app>
</template>
<script lang="ts">
import Vue from "vue";
import BackendServerCommunicator from "@Controler/BackendServerCommunicator";
import ServerConfig from "@Model/ServerConfig";
import Server from "@Classes/Server";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const serverConfigObject = new ServerConfig(
  [
    { text: "Server location name", value: "serverName" },
    { text: "Address", value: "serverAddress" },
    { text: "Status", value: "serverStatus" },
    { text: "Container limit", value: "containerLimit" },
    { text: "Select server for execution", value: "selectedForExecution" },
    { text: "Configurate server resources", value: "serverResources" },
    { text: "apply changes", value: "apply" },
  ],
  [],
  false
);

export default {
  name: "ServerConfig",
  methods: {
    pushServerAndPullServers(serverName: string) {
      this.pushServer(serverName);
      this.pullServers();
    },
    pullServers() {
      this.servers = backendServerCommunicatorObject.pullServers();
    },
    pushServer(serverName: string) {
      backendServerCommunicatorObject.pushServer(
        this.findServerByServerName(this.servers, serverName)
      );
    },
    findServerByServerName(servers: Server[], serverName: string): Server {
      let serverIndex = servers.findIndex((server: Server) => {
        return server.serverName == serverName;
      });
      if (serverIndex == -1) {
        throw "No server with the name " + serverName + " was found";
      }
      return servers[serverIndex];
    },
  },
  computed: {
    tableHeaders: {
      get: function (): object[] {
        return serverConfigObject.tableHeaders;
      },
      set: function (tableHeaders: object[]) {
        serverConfigObject.tableHeaders = tableHeaders;
      },
    },
    servers: {
      get: function (): Server[] {
        return serverConfigObject.servers;
      },
      set: function (servers: Server[]) {
        serverConfigObject.servers = servers;
      },
    },
    resourcesDialog: {
      get: function (): boolean {
        return serverConfigObject.resourcesDialog;
      },
      set: function (resourcesDialog: boolean) {
        serverConfigObject.resourcesDialog = resourcesDialog;
      },
    },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(serverConfigObject);
  },
  created: async function () {
    this.servers = await backendServerCommunicatorObject.pullServers();
    console.log('frontend', this.servers)
  },
};
</script>