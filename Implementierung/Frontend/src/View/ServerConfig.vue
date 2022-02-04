<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 20px">
      <v-data-table :headers="header" :items="items" item-key="name">
        <template v-slot:[`item.name`]="{ item }"
          ><v-text-field v-model="item.name"></v-text-field
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
          ><v-checkbox></v-checkbox
        ></template>
      </v-data-table>
    </div>
  </v-app>
</template>
<script>
export default {
  data: function () {
    return {
      header: [
        { text: "Server location name", value: "name" },
        { text: "Address", value: "address" },
        { text: "Status", value: "status" },
        { text: "Container limit", value: "limit" },
        { text: "Select server for execution", value: "server" },
        { text: "dag-folder location", value: "dagLocation" },
        { text: "Configurate server resources", value: "serverResources" },
        { text: "apply changes", value: "apply" },
        { text: "delete server", value: "delete" },
      ],
      items: [
        {
          name: "kit-materialwissenschaften",
          address: "123.123.11.1",
          status: "running",
          limit: 5,
          dagLocation: "home/airflow/dags",
        },
      ],
    };
  },
};
</script>