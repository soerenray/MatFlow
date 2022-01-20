<template>
  <v-app>
    <!--
    <create-template></create-template>
    -->
    <create-workflow-instance></create-workflow-instance>
  </v-app>
</template>

<script lang='ts'>
import CreateWorkflowInstance from './View/CreateWorkflowInstance.vue'
import CreateTemplate from './View/CreateTemplate.vue'

export default {
  name: 'App',

  components: {
    CreateWorkflowInstance,
    CreateTemplate
  },

  data: () => ({
    //
  }),
};
</script>
