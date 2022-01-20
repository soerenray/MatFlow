<template>
  <v-app>
    <!--
    <create-template></create-template>
    <create-workflow-instance></create-workflow-instance>
    <version-control></version-control>
    <log-in></log-in>
    -->
    <sign-up></sign-up>
  </v-app>
</template>

<script lang='ts'>
import CreateWorkflowInstance from './View/CreateWorkflowInstance.vue'
import CreateTemplate from './View/CreateTemplate.vue'
import VersionControl from './View/VersionControl.vue'
import SignUp from './View/SignUp.vue'
import LogIn from './View/LogIn.vue'

export default {
  name: 'App',

  components: {
    CreateWorkflowInstance,
    CreateTemplate,
    VersionControl,
    SignUp,
    LogIn,
  },

  data: () => ({
    //
  }),
};
</script>
