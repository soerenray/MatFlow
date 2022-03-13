<template>
  <v-app>
    <div style="height: 30px">
      <v-toolbar dense color="#AED6F1">
        <v-toolbar-title>Administration</v-toolbar-title>
      </v-toolbar>
    </div>
    <div style="padding-top: 40px; padding-left: 10px; padding-right=10px">
      <v-card>
        <v-row>
          <v-col>
            <div style="padding-left: 20px; padding-bottom: 5px">
              <v-btn
                data-cy="pullUsersFromServer"
                @click="pullUsersFromServer"
                color="yellow"
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
              <v-btn
                data-cy="updateUsers"
                @click="pushUsersAndPullUsersFromServer()"
                color="blue"
                >Update users</v-btn
              >
            </div>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-table>
          <thead>
            <tr>
              <th v-for="header in tableHeaders" class="text-left">
                {{ header.text }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.name">
              <td>
                <v-text-field
                  data-cy="userName"
                  disabled
                  v-model="user.userName"
                ></v-text-field>
              </td>
              <td>
                <v-select
                  data-cy="userPriviliges"
                  :items="selectStatuses"
                  v-model="user.userStatus"
                  label="Item"
                ></v-select>
              </td>
              <td>
                <v-select
                  data-cy="userStatus"
                  :items="selectPrivileges"
                  v-model="user.userPrivilege"
                ></v-select>
              </td>
              <td>
                <v-btn
                  data-cy="delete"
                  @click="pushDeleteUserAndPullUsersFromServer(user)"
                  fab
                  small
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card>
    </div>
  </v-app>
</template>
<script lang="ts">
// @ts-nocheck
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';
import User from '@Classes/User';
import UserAdministration from '@Model/UserAdministration';

export default {
  name: 'UserAdministration',
  data() {
    return {
      backendServerCommunicatorObject: new BackendServerCommunicator(),
      userAdministrationObject: new UserAdministration(
        [
          { text: 'Username', value: 'name' },
          { text: 'User priviliges', value: 'privilege' },
          { text: 'Status', value: 'status' },
          { text: 'Delete', value: 'delete' },
        ],
        [],
        ['activated', 'suspended', 'pending'],
        ['visitor', 'developer', 'administrator'],
      ),
    };
  },
  methods: {
    pushDeleteUserAndPullUsersFromServer(user: User) {
      this.backendServerCommunicatorObject.pushDeleteUser(user);
      this.pullUsersFromServer();
    },
    async pullUsersFromServer() {
      this.removeUsersFromComponent();
      this.users = await this.backendServerCommunicatorObject.pullUsers();
    },
    pushUsersAndPullUsersFromServer() {
      this.users.forEach((user: User) => {
        this.backendServerCommunicatorObject.pushUser(user);
      });
      this.pullUsersFromServer();
    },
    removeUsersFromComponent() {
      this.users.splice(0);
    },
  },
  computed: {
    tableHeaders: {
      get(): object[] {
        return this.userAdministrationObject.tableHeaders;
      },
      set(tableHeaders: object[]) {
        this.userAdministrationObject.tableHeaders = tableHeaders;
      },
    },
    users: {
      get(): User[] {
        return this.userAdministrationObject.users;
      },
      set(users: User[]) {
        this.userAdministrationObject.users = users;
      },
    },
    selectStatuses: {
      get(): string[] {
        return this.userAdministrationObject.selectStatuses;
      },
      set(selectStatuses: string[]) {
        this.userAdministrationObject.selectStatuses = selectStatuses;
      },
    },
    selectPrivileges: {
      get(): string[] {
        return this.userAdministrationObject.selectPrivileges;
      },
      set(selectPrivileges: string[]) {
        this.userAdministrationObject.selectPrivileges = selectPrivileges;
      },
    },
  },
  async created() {
    this.userAdministrationObject.users = await this.backendServerCommunicatorObject.pullUsers();
  },
};
</script>
