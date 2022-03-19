<template>
  <v-app>
    <v-main>
      <v-row>
          <v-toolbar style='width: 100%' dense color="#AED6F1">
            <v-row>
              <v-col style='width: 200px'>
                <v-btn to="/CreateTemplate" variant="text">CreateTemplate
                   <router-link to="/CreateTemplate"></router-link>
                </v-btn>
              </v-col>
              <v-col style='width: 250px'>
                <v-btn to="/CreateWorkflowInstance" variant="text">CreateWorkflowInstance
                   <router-link to="/CreateWorkflowInstance"></router-link>
                </v-btn>
              </v-col>
              <v-col style='width: 200px'>
                <v-btn to="/ChooseConfigFile" variant="text">ChooseConfigFile
                   <router-link to="/ChooseConfigFile"></router-link>
                </v-btn>
              </v-col>
              <v-col style='width: 200px'>
                <v-btn to="/VersionControl" variant="text">VersionControl
                   <router-link to="/VersionControl"></router-link>
                </v-btn>
              </v-col>
              <v-col style='width: 200px'>
                <v-btn to="/UserAdministration" variant="text">UserAdministration
                   <router-link to="/UserAdministration"></router-link>
                </v-btn>
              </v-col>
              <v-col style='width: 200px'>
                <v-btn to="/ServerConfig" variant="text">ServerConfig
                   <router-link to="/ServerConfig"></router-link>
                </v-btn>
              </v-col>
              <v-col style='width: 100px'>
                <v-btn to="/LogIn" variant="text">LogIn
                   <router-link to="/LogIn"></router-link>
                </v-btn>
              </v-col>
              <v-col style='width: 100px'>
                <v-btn href='http://localhost:8080' variant="text">
                   Airflow
                </v-btn>
              </v-col>
            </v-row>
          </v-toolbar>
      </v-row>
      <v-row style='padding-top: 20px'>
          <router-view/>
      </v-row>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',

  data() {
    return {
      //
    };
  },
});
</script>
