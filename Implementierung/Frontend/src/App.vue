<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<script lang='ts'>
import UserAdministration from "./View/UserAdministration.vue";
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
    UserAdministration,
  },

  data: () => ({
    //
  }),
};
</script>
