<template>
  <v-app>
    <!--
    <create-workflow-instance></create-workflow-instance>
    -->
    <create-template></create-template>
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
