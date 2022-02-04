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
        <template v-slot:[`item.serverResources`]="{}"
          ><v-btn icon><memory-icon></memory-icon></v-btn
        ></template>
        <template v-slot:[`item.apply`]="{}"
          ><v-btn color="green" outlined>apply changes</v-btn></template
        >
      </v-data-table>
    </div>
  </v-app>
</template>
<script lang="ts">
import Vue from "vue";
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
  name: "ServerConfig",
  methods: {
    pushServerAndPullServers(server: Server) {
      this.pushServer(server);
      backendServerCommunicatorObject.pullServers();
    },
    pushServer(server: Server) {
      backendServerCommunicatorObject.pushServer(server);
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