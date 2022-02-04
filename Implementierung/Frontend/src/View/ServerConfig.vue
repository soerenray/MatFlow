<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 20px">
      <v-card flat>
        <div style="padding-left: 20px">
          <v-row>
            <v-col>
              <v-text-field
                label="server-name"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                label="server-address"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <div style="padding-right: 50px; padding-top: 20px">
              <v-btn color="blue">Add new server</v-btn>
            </div>
          </v-row>
        </div>
      </v-card>
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
          ><v-btn color="red" icon><v-icon>delete</v-icon></v-btn></template
        >
        <template v-slot:[`item.apply`]="{}"
          ><v-btn color="green" outlined>apply changes</v-btn></template
        >
        <template v-slot:[`item.serverResources`]="{}"
          ><v-btn icon><v-icon>memory</v-icon> </v-btn></template
        >
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
        {
          name: "kit-informatik",
          address: "123.123.123.123",
          status: "maintance",
          limit: 12,
          dagLocation: "usr/admin/documents/airflow/dags",
        },
      ],
    };
  },
};
</script>