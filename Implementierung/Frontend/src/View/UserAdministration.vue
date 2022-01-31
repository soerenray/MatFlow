<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 20px">
      <v-card>
        <v-data-table :headers="tableHeaders" :items="users" :item-key="users.name">
          <template v-slot:[`item.name`]="{ item }"
            ><v-text-field :value="item.name"></v-text-field
          ></template>
          <template v-slot:[`item.privilege`]="{ item }"
            ><v-select :items="privilege" v-model="item.privilege"></v-select
          ></template>
          <template v-slot:[`item.status`]="{ item }"
            ><v-select :items="status" v-model="item.status"></v-select
          ></template>
          <template v-slot:[`item.delete`]="{}">
            <v-btn icon> <delete-icon></delete-icon></v-btn></template
          ><template v-slot:[`item.password`]="{}">
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on"
                  ><lock-clock-icon></lock-clock-icon>
                </v-btn>
              </template>
              <v-card>
                <v-card-title> Reset the password </v-card-title>
                <div style="padding-right: 10px; padding-left: 10px">
                  <v-text-field></v-text-field>
                </div>
                <div style="padding-right: 10px; padding-left: 10px">
                  <v-text-field></v-text-field>
                </div>
                <v-row>
                  <v-spacer></v-spacer>
                  <div style="padding-right: 20px">
                    <v-btn disabled>reset</v-btn>
                  </div>
                </v-row>
              </v-card>
            </v-dialog></template
          >
        </v-data-table>
      </v-card>
    </div>
  </v-app>
</template>
<script lang="ts">
import User from "../Classes/User";
import UserAdministration from "../Model/UserAdministration";

const userAdministrationObject = new UserAdministration([
  { text: "Username", value: "name" },
  { text: "User priviliges", value: "privilege" },
  { text: "Status", value: "status" },
  { text: "Delete", value: "delete" },
  { text: "Reset password", value: "password" },
]);

export default {
  name: "UserAdministration",
  data: function () {
    return {
      status: ["activated", "suspended", "pending"],
      privilege: ["visitor", "developer", "administrator"],
      dialog: false,
    };
  },
  computed: {
    tableHeaders: {
      get: function(): object[] {
        return userAdministrationObject.tableHeaders
      },
      set: function(tableHeaders: object[]) {
        userAdministrationObject.tableHeaders = tableHeaders
      }
    },
    users: {
      get: function() : User[] {
        return userAdministrationObject.users
      },
      set: function(users: User[]) {
        userAdministrationObject.users = users
      }
    }
  }
};
</script>