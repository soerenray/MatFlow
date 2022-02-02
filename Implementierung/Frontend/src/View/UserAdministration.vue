<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 20px">
      <v-col>
        <v-row>
          <v-card width="100%" style="padding-bottom: 10px; padding-top: 10px">
            <v-row>
              <v-col>
                <div style="padding-left: 20px; padding-top: 5px">
                  <v-btn color="yellow">Pull users from server</v-btn>
                </div>
              </v-col>
              <v-spacer></v-spacer>
              <v-col>
                <div style="padding-right: 20px; padding-top: 5px">
                  <v-btn color="blue">Update users</v-btn>
                </div>
              </v-col>
            </v-row>
          </v-card>
        </v-row>
        <v-row>
          <v-card>
            <v-data-table
              :headers="tableHeaders"
              :items="users"
              :item-key="users.name"
            >
              <template v-slot:[`item.name`]="{ item }"
                ><v-text-field :value="item.userName"></v-text-field
              ></template>
              <template v-slot:[`item.privilege`]="{ item }"
                ><v-select
                  :items="selectPrivileges"
                  v-model="item.userPrivilege"
                ></v-select
              ></template>
              <template v-slot:[`item.status`]="{ item }"
                ><v-select
                  :items="selectStatuses"
                  v-model="item.userStatus"
                ></v-select
              ></template>
              <template v-slot:[`item.delete`]="{ item }">
                <v-btn @click="pushDeleteUser(item)" icon>
                  <delete-icon></delete-icon></v-btn></template
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
        </v-row>
      </v-col>
    </div>
  </v-app>
</template>
<script lang="ts">
import Vue from "vue";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";
import User from "../Classes/User";
import UserAdministration from "../Model/UserAdministration";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const userAdministrationObject = new UserAdministration(
  [
    { text: "Username", value: "name", width: "50%" },
    { text: "User priviliges", value: "privilege", width: "50%" },
    { text: "Status", value: "status", width: "50%" },
    { text: "Delete", value: "delete", width: "50%" },
    { text: "Reset password", value: "password", width: "200px" },
  ],
  [],
  ["activated", "suspended", "pending"],
  ["visitor", "developer", "administrator"]
);

export default {
  name: "UserAdministration",
  data: function () {
    return {
      dialog: false,
    };
  },
  methods: {
    pushDeleteUser(user: User) {
      backendServerCommunicatorObject.pushDeleteUser(user);
      this.users = backendServerCommunicatorObject.pullUsers();
    },
  },
  computed: {
    tableHeaders: {
      get: function (): object[] {
        return userAdministrationObject.tableHeaders;
      },
      set: function (tableHeaders: object[]) {
        userAdministrationObject.tableHeaders = tableHeaders;
      },
    },
    users: {
      get: function (): User[] {
        return userAdministrationObject.users;
      },
      set: function (users: User[]) {
        userAdministrationObject.users = users;
      },
    },
    selectStatuses: {
      get: function (): string[] {
        return userAdministrationObject.selectStatuses;
      },
      set: function (selectStatuses: string[]) {
        userAdministrationObject.selectStatuses = selectStatuses;
      },
    },
    selectPrivileges: {
      get: function (): string[] {
        return userAdministrationObject.selectPrivileges;
      },
      set: function (selectPrivileges: string[]) {
        userAdministrationObject.selectPrivileges = selectPrivileges;
      },
    },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(userAdministrationObject);
  },
  created: function () {
    userAdministrationObject.users =
      backendServerCommunicatorObject.pullUsers();
  },
};
</script>