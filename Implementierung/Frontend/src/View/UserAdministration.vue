<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 40px">
      <v-card>
        <v-data-table
          :headers="tableHeaders"
          :items="users"
          :item-key="users.name"
        >
          <template v-slot:top
            ><v-row>
              <v-col>
                <div
                  style="
                    padding-left: 20px;
                    padding-top: 5px;
                    padding-bottom: 5px;
                  "
                >
                  <v-btn @click="pullUsersFromServer" color="yellow"
                    >Pull users from server</v-btn
                  >
                </div>
              </v-col>
              <v-col align="right">
                <div
                  style="
                    padding-right: 20px;
                    padding-top: 5px;
                    padding-bottom: 5px;
                  A"
                >
                  <v-btn color="blue">Update users</v-btn>
                </div>
              </v-col>
            </v-row>
          </template>
          <template v-slot:[`item.name`]="{ item }"
            ><v-text-field v-model="item.userName"></v-text-field
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
            <v-dialog v-model="dialog">
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
import Vue from "vue";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";
import User from "../Classes/User";
import UserAdministration from "../Model/UserAdministration";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const userAdministrationObject = new UserAdministration(
  [
    { text: "Username", value: "name" },
    { text: "User priviliges", value: "privilege" },
    { text: "Status", value: "status" },
    { text: "Delete", value: "delete" },
    { text: "Reset password", value: "password" },
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
      this.removeUsersFromComponent();
      backendServerCommunicatorObject.pushDeleteUser(user);
      this.users = backendServerCommunicatorObject.pullUsers();
    },
    pullUsersFromServer() {
      this.removeUsersFromComponent();
      this.users = backendServerCommunicatorObject.pullUsers();
    },
    removeUsersFromComponent() {
      this.users.splice(0);
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