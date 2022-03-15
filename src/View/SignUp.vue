<template>
  <v-app :style="{ background: '#B5EEF6' }">
    <v-layout justify-center align-center class="mx-auto mt-8">
      <v-card width="800px" height="400px">
        <v-card-title class="justify-center">
          <p>Sign-up</p>
        </v-card-title>
        <v-card-text>
          <v-col>
            <v-row>
              <v-text-field
                data-cy='emailAddress'
                v-model="userName"
                label="email-address"
              ></v-text-field
            ></v-row>
            {{  }}
            <v-row>
              <v-text-field
                data-cy='userPassword'
                v-model="userPassword"
                label="password"
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
              ></v-text-field
            ></v-row>
            <v-row>
              <v-text-field
                data-cy='userPasswordRepeated'
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
            <v-btn data-cy='signUp' @click="pushSignUpAndResetView" color="blue" dark>
              SignUp
            </v-btn>
          </v-row>
        </v-card-text>
      </v-card>
    </v-layout>
  </v-app>
</template>

<script lang='ts'>
// @ts-nocheck
import BackenderServerCommunicator from '@Controler/BackendServerCommunicator';
import SignUp from '@Model/SignUp';

const signUpObject = new SignUp();

export default {
  name: 'SignUp',
  data() {
    return {
      backendServerCommunicatorObject: new BackenderServerCommunicator(),
      signUpObject,
      signUpMementoObject: signUpObject.createSignUpMemento(),
    };
  },
  methods: {
    pushSignUpAndResetView() {
      this.pushSignUp();
      this.resetView();
    },
    pushSignUp() {
      this.backendServerCommunicatorObject.pushSignUp(
        this.signUpObject.userName,
        this.signUpObject.userPassword,
        this.signUpObject.userPasswordRepeated,
      );
    },
    resetView() {
      this.signUpObject.setSignUpMemento(this.signUpMementoObject);
    },
  },
  computed: {
    userName: {
      get(): string {
        return this.signUpObject.userName;
      },
      set(userName: string) {
        this.signUpObject.userName = userName;
      },
    },
    userPassword: {
      get(): string {
        return this.signUpObject.userPassword;
      },
      set(userPassword: string) {
        this.signUpObject.userPassword = userPassword;
      },
    },
    userPasswordRepeated: {
      get(): string {
        return this.signUpObject.userPasswordRepeated;
      },
      set(userPasswordRepeated: string) {
        this.signUpObject.userPasswordRepeated = userPasswordRepeated;
      },
    },
    showPassword: {
      get(): boolean {
        return this.signUpObject.showPassword;
      },
      set(showPassword: boolean) {
        this.signUpObject.showPassword = showPassword;
      },
    },
    showPasswordRepeated: {
      get(): boolean {
        return this.signUpObject.showPasswordRepeated;
      },
      set(showPasswordRepeated: boolean) {
        this.signUpObject.showPasswordRepeated = showPasswordRepeated;
      },
    },
  },
};
</script>
