<template>
  <v-app :style="{ background: '#B5F6BC' }">
    <v-layout justify-center align-center>
      <v-card width="800px" height="400px">
        <v-card-title class="justify-center">
          <p>LogIn</p>
        </v-card-title>
        <v-card-text>
          <v-col>
            <v-row>
              <v-text-field
                v-model="userName"
                label="email-address"
              ></v-text-field
            ></v-row>
            <v-row>
              <v-text-field
                v-model="userPassword"
                label="password"
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
              ></v-text-field
            ></v-row>
          </v-col>
          <v-col>
            <div style="padding-left: 10px">
              <v-row> Create a user-account, when you are new</v-row>
            </div>
            <v-row>
              <div style="padding-left: 10px; padding-top: 5px">
                 <router-link to="/SignUp">SignUp</router-link>
              </div>
              <v-spacer></v-spacer>
              <v-btn @click='pushLogIn' color="blue">LogIn</v-btn>
            </v-row>
          </v-col>
        </v-card-text>
      </v-card>
    </v-layout>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";
import LogIn from "../Model/LogIn";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const logInObject = new LogIn();

export default {
  name: "LogIn",
  methods: {
    pushLogIn() {
      backendServerCommunicatorObject.pushLogIn(
        logInObject.userName,
        logInObject.userPassword
      );
    },
  },
  computed: {
    userName: {
      get: function (): string {
        return logInObject.userName;
      },
      set: function (userName: string) {
        logInObject.userName = userName;
      },
    },
    userPassword: {
      get: function (): string {
        return logInObject.userPassword;
      },
      set: function (userPassword: string) {
        logInObject.userPassword = userPassword;
      },
    },
    showPassword: {
      get: function (): boolean {
        return logInObject.showPassword;
      },
      set: function (showPassword: boolean) {
        logInObject.showPassword = showPassword;
      },
    },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(logInObject);
  },
};
</script>