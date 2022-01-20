<template>
  <v-app :style="{ background: '#B5EEF6' }">
    <!-- <v-layout align-center justify-center style="border: 15px solid green"> -->
    <v-layout justify-center align-center>
      <v-card width="800px" height="400px">
        <v-card-title class="justify-center">
          <p>Sign-up</p>
        </v-card-title>
        <v-card-text>
          <v-col>
            <v-row> <v-text-field label="email-address"></v-text-field></v-row>
            <v-row> <v-text-field label="password"></v-text-field></v-row>
            <v-row>
              <v-text-field label="repeat password"></v-text-field
            ></v-row>
          </v-col>
          <v-row>
            <v-spacer></v-spacer>
            <v-dialog v-model="dialoge" max-width="500px">
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

<script>
export default {
    name: 'SignUp',
    computed: {
        userName: {

        },
        userPassword: {

        }
    }
};
</script>
