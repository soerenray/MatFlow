<template>
  <v-app :style="{ background: '#B5EEF6' }">
    <v-layout justify-center align-center>
      <v-card width="800px" height="400px">
        <v-card-title class="justify-center">
          <p>Sign-up</p>
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
            <v-row>
              <v-text-field
                label="repeat password"
                v-model="userPasswordRepeated"
                :type="showPasswordRepeated ? 'text' : 'password'"
                :append-icon="showPasswordRepeated ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPasswordRepeated = !showPasswordRepeated"
              ></v-text-field
            ></v-row>
          </v-col>
          <v-row>
            <v-spacer></v-spacer>
            <v-btn color="primary" dark> SignUp </v-btn>
          </v-row>
        </v-card-text>
      </v-card>
    </v-layout>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";
import SignUp from "../Model/SignUp";

let signUpObject = new SignUp();

export default {
  name: "SignUp",
  computed: {
    userName: {
      get: function (): string {
        return signUpObject.userName;
      },
      set: function (userName: string) {
        signUpObject.userName = userName;
      },
    },
    userPassword: {
      get: function (): string {
        return signUpObject.userPassword;
      },
      set: function (userPassword: string) {
        signUpObject.userPassword = userPassword;
      },
    },
    userPasswordRepeated: {
      get: function (): string {
        return signUpObject.userPasswordRepeated;
      },
      set: function (userPasswordRepeated: string) {
        signUpObject.userPasswordRepeated = userPasswordRepeated;
      },
    },
    showPassword: {
      get: function (): boolean {
        return signUpObject.showPassword;
      },
      set: function (showPassword: boolean) {
        signUpObject.showPassword = showPassword;
      },
    },
    showPasswordRepeated: {
      get: function (): boolean {
        return signUpObject.showPasswordRepeated;
      },
      set: function (showPasswordRepeated: boolean) {
        signUpObject.showPasswordRepeated = showPasswordRepeated;
      },
    },
  },
    beforeCreate: function () {
      // Vue is oberserving data in the data property.
      // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
      Vue.observable(signUpObject);
    },
};
</script>
