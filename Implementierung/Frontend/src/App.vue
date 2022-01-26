<template>
  <v-app>
    <!--
    -->
    <choose-config-file></choose-config-file>
    <create-template></create-template>
    <create-workflow-instance></create-workflow-instance>
    <log-in></log-in>
    <sign-up></sign-up>
    <version-control></version-control>
  </v-app>
</template>

<script lang='ts'>
import CreateWorkflowInstance from "./View/CreateWorkflowInstance.vue";
import CreateTemplate from "./View/CreateTemplate.vue";
import VersionControl from "./View/VersionControl.vue";
import SignUp from "./View/SignUp.vue";
import LogIn from "./View/LogIn.vue";
import ChooseConfigFile from "./View/ChooseConfigFile.vue";

export default {
  name: "App",

  components: {
    CreateWorkflowInstance,
    CreateTemplate,
    VersionControl,
    SignUp,
    LogIn,
    ChooseConfigFile,
  },

  data: () => ({
    //
  }),
};
</script>
