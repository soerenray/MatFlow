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
            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary" dark v-bind="attrs" v-on="on">
                  Open Dialog
                </v-btn>
              </template>
              <v-card>
                <v-card-title> Registration was successfull </v-card-title>
                <v-card-text
                  >Your registration was send to the adminastrator, who will
                  approve your account.
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-row>
        </v-card-text>
      </v-card>
    </v-layout>
  </v-app>
</template>

<script lang='ts'>
import SignUp from "../Model/SignUp";

let signUpObject = new SignUp();

export default {
  name: "SignUp",
  data: () => {
    return { showPassword: false, showPasswordRepeated: false, dialog: false };
  },
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
  },
};
</script>
