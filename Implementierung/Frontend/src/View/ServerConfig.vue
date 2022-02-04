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
      >
        <template v-slot:[`item.containerLimit`]="{ item }"
          ><v-text-field v-model="item.containerLimit"></v-text-field
        ></template>
        <template v-slot:[`item.selectedForExecution`]="{}"
          ><v-checkbox disabled></v-checkbox
        ></template>
        <template v-slot:[`item.serverResources`]="{ item }">
          <v-dialog width="700px" v-model="dialog">
            <template v-slot:activator="{ on, attrs }">
              <v-btn v-on="on" v-bind="attrs" icon
                ><memory-icon></memory-icon
              ></v-btn>
            </template>
            <edit-key-value-pairs
              v-on:changeAllKeyValuePairs="changeAllKeyValuePairs"
              v-on:push="pushServer"
              v-on:reset="pullServers"
              :fileName="item.serverName"
              :keyValuePairsFromParent="item.serverResources"
            ></edit-key-value-pairs>
          </v-dialog>
        </template>
        <template v-slot:[`item.apply`]="{ item }"
          ><v-btn @click="pushServerAndPullServers(item)" color="green" outlined
            >apply changes</v-btn
          ></template
        >
      </v-data-table>
    </div>
  </v-app>
</template>
<script lang="ts">
import Vue from "vue";
import EditKeyValuePairs from "../View/EditKeyValuePairs.vue";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";
import ServerConfig from "../Model/ServerConfig";
import Server from "../Classes/Server";

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
  []
);

export default {
  components: { EditKeyValuePairs },
  name: "ServerConfig",
  data: function () {
    return {
      dialog: false,
    };
  },
  methods: {
    pushServerAndPullServers() {
      this.pushServer();
      this.pullServers();
    },
    pullServers() {
      this.servers = backendServerCommunicatorObject.pullServers();
    },
    pushServer() {
      backendServerCommunicatorObject.pushServer(this.servers[0]);
    },
    changeAllKeyValuePairs(newKeyValuePairs: Array<[string, string]>) {
      this.servers[0].serverResources.forEach(
        (keyValuePair: [string, string], index: number) => {
          keyValuePair[0] = newKeyValuePairs[index][0];
          keyValuePair[1] = newKeyValuePairs[index][1];
        }
      );
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
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(serverConfigObject);
  },
  created: function () {
    this.servers = backendServerCommunicatorObject.pullServers();
  },
};
</script>