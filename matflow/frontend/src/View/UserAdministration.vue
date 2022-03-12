<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 30px">
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
                    padding-bottom: 5px;
                  A"
                >
                  <v-btn @click="pushUsersAndPullUsersFromServer()" color="blue"
                    >Update users</v-btn
                  >
                </div>
              </v-col>
            </v-row>
            <v-divider></v-divider>
          </template>
          <template v-slot:[`item.name`]="{ item }"
            ><v-text-field disabled v-model="item.userName"></v-text-field
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
            <v-btn @click="pushDeleteUserAndPullUsersFromServer(item)" icon>
              <delete-icon></delete-icon></v-btn
          ></template>
        </v-data-table>
      </v-card>
    </div>
  </v-app>
</template>
<script lang="ts">
import Vue from "vue";
import BackendServerCommunicator from "@Controler/BackendServerCommunicator";
import User from "@Classes/User";
import UserAdministration from "@Model/UserAdministration";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const userAdministrationObject = new UserAdministration(
  [
    { text: "Username", value: "name" },
    { text: "User priviliges", value: "privilege" },
    { text: "Status", value: "status" },
    { text: "Delete", value: "delete" },
  ],
  [],
  ["activated", "suspended", "pending"],
  ["visitor", "developer", "administrator"]
);

export default {
  name: "UserAdministration",
  methods: {
    pushDeleteUserAndPullUsersFromServer(user: User) {
      backendServerCommunicatorObject.pushDeleteUser(user);
      this.pullUsersFromServer();
    },
    pullUsersFromServer() {
      this.removeUsersFromComponent();
      backendServerCommunicatorObject.pullUsers().then(function (result){
        this.users = result;
      });
    },
    pushUsersAndPullUsersFromServer() {
      this.users.forEach((user: User) => {
        backendServerCommunicatorObject.pushUser(user);
      });
      this.pullUsersFromServer();
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
      backendServerCommunicatorObject.pullUsers().then(function (result){
        userAdministrationObject.users = result;
      });
  },
};
</script>