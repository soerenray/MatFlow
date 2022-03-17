<template>
  <v-app :style="{ background: '#B5F6BC', height: '1080px' }">
    <v-layout class="mx-auto mt-8">
      <v-main>
        <v-card width="800px" height="400px">
          <v-card-title class="justify-center">
            <p>LogIn</p>
          </v-card-title>
          <v-card-text>
            <v-col>
              <v-row>
                <v-text-field
                  data-cy="emailAddress"
                  v-model="userName"
                  label="email-address"
                ></v-text-field
              ></v-row>
              <v-row>
                <v-text-field
                  data-cy="userPassword"
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
                <v-btn data-cy='loginButton' @click=
                "pushLogInAndResetView" color="blue">LogIn</v-btn>
              </v-row>
            </v-col>
          </v-card-text>
        </v-card>
      </v-main>
    </v-layout>
  </v-app>
</template>
<script lang='ts'>
// @ts-nocheck
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';
import LogIn from '@Model/LogIn';

const logInObject = new LogIn();

export default {
  name: 'LogIn',
  data() {
    return {
      backendServerCommunicatorObject: new BackendServerCommunicator(),
      logInObject,
      logInMementoObject: logInObject.createLogInMemento(),
    };
  },
  methods: {
    pushLogInAndResetView() {
      this.pushLogIn();
      this.resetView();
    },
    pushLogIn() {
      this.backendServerCommunicatorObject.pushLogIn(
        this.logInObject.userName,
        this.logInObject.userPassword,
      );
    },
    resetView() {
      this.logInObject.setLogInMemento(this.logInMementoObject);
    },
  },
  computed: {
    userName: {
      get(): string {
        return this.logInObject.userName;
      },
      set(userName: string) {
        this.logInObject.userName = userName;
      },
    },
    userPassword: {
      get(): string {
        return this.logInObject.userPassword;
      },
      set(userPassword: string) {
        this.logInObject.userPassword = userPassword;
      },
    },
    showPassword: {
      get(): boolean {
        return this.logInObject.showPassword;
      },
      set(showPassword: boolean) {
        this.logInObject.showPassword = showPassword;
      },
    },
  },
};
</script>
