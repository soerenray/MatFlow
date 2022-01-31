<template>
  <v-app :style="{ background: '#B5F6BC' }">
    <v-layout justify-center align-center>
      <v-card width="800px" height="400px">
        <v-card-title class="justify-center">
          <p>Log-in</p>
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
                <a href>register</a>
              </div>
              <v-spacer></v-spacer>
              <v-btn disabled>log-in</v-btn>
            </v-row>
          </v-col>
        </v-card-text>
      </v-card>
    </v-layout>
  </v-app>
</template>

<script lang='ts'>
import BackendServerCommunicator from "../Controler/BackendServerCommunicator"
import LogIn from "../Model/LogIn";

const backendServerCommunicatorObject = new BackendServerCommunicator()
const logInObject = new LogIn();

export default {
  name: "LogIn",
  data: () => {
    return {
      showPassword: false,
    };
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
  },
};
</script>