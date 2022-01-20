<template>
  <v-app>
    <!--
    <create-template></create-template>
    <create-workflow-instance></create-workflow-instance>
    -->
    <version-control></version-control>
  </v-app>
</template>

<script lang='ts'>
import CreateWorkflowInstance from './View/CreateWorkflowInstance.vue'
import CreateTemplate from './View/CreateTemplate.vue'
import VersionControl from './View/VersionControl.vue'

export default {
  name: 'App',

  components: {
    CreateWorkflowInstance,
    CreateTemplate,
    VersionControl
  },

  data: () => ({
    //
  }),
};
</script>
