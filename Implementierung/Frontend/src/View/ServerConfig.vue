<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 20px">
      <v-data-table :headers="tableHeaders" :items="items" item-key="name">
        <template v-slot:[`item.name`]="{ item }"
          ><v-text-field disabled v-model="item.name"></v-text-field
        ></template>
        <template v-slot:[`item.limit`]="{ item }"
          ><v-text-field v-model="item.limit"></v-text-field
        ></template>
        <template v-slot:[`item.dagLocation`]="{ item }"
          ><v-text-field v-model="item.dagLocation"></v-text-field
        ></template>
        <template v-slot:[`item.delete`]="{}"
          ><v-btn color="red" icon><delete-icon></delete-icon></v-btn
        ></template>
        <template v-slot:[`item.apply`]="{}"
          ><v-btn color="green" outlined>apply changes</v-btn></template
        >
        <template v-slot:[`item.serverResources`]="{}"
          ><v-btn icon><memory-icon></memory-icon></v-btn
        ></template>
        <template v-slot:[`item.server`]="{}"
          ><v-checkbox disabled></v-checkbox
        ></template>
      </v-data-table>
    </div>
  </v-app>
</template>
<script lang="ts">
import ServerConfig from "../Model/ServerConfig";
import Server from "../Classes/Server";

const serverConfigObject = new ServerConfig(
  [
    { text: "Server location name", value: "name" },
    { text: "Address", value: "address" },
    { text: "Status", value: "status" },
    { text: "Container limit", value: "limit" },
    { text: "Select server for execution", value: "server" },
    { text: "Configurate server resources", value: "serverResources" },
    { text: "apply changes", value: "apply" },
    { text: "delete server", value: "delete" },
  ],
  [
    new Server(
      "123.123.11.1",
      "running",
      5,
      true,
      "kit-materialwissenschaften",
      [["cpu1", '50%']]
    ),
  ]
);

export default {
  name: "ServerConfig",
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
      get: function(): Server[] {
        return serverConfigObject.servers
      },
      set: function(servers: Server[]) {
        serverConfigObject.servers = servers
      }
    }
  },
};
</script>