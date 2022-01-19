<template>
  <v-app>
    <create-workflow-instance></create-workflow-instance>
  </v-app>
</template>

<script>
import CreateWorkflowInstance from './View/CreateWorkflowInstance.vue'

export default {
  name: 'App',

  components: {
    CreateWorkflowInstance
  },

  data: () => ({
    //
  }),
};
</script>
