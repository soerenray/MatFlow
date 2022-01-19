<template>
  <v-app>
    <v-card>
      <v-card-title> Create new workflow-instance </v-card-title>
      <div style="padding-left: 20px">
        <v-select :items="dropwDown" v-model="selectedDrowpnItem"></v-select>
        <div
          v-if="selectedDrowpnItem == 'create workflow-instance from template'"
        >
          <v-row>
            <v-col>
              <v-text-field
                label="Name of the workflow-instance"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-select :items="templates" label="choose template"> </v-select>
            </v-col>
            <v-col>
              <v-select :items="folder" label="config-file folder"> </v-select>
            </v-col>
            <v-col>
              <v-btn fab small color="#58D68D"><v-icon>add</v-icon></v-btn>
            </v-col>
          </v-row>
        </div>
      </div>
      <div v-if="selectedDrowpnItem == 'import worfklow-instance'">
        <v-file-input accept="image/*" label="Workflow-folder"></v-file-input>
      </div>
    </v-card>
  </v-app>
</template>

<script lang='ts'>
import CreateWorkflowInstance from '../Model/CreateWorkflowInstance'

let createWorkflowInstanceObject = new CreateWorkflowInstance()

export default {
  data: function () {
    return {
      templates: ["MyNewTemplate"],
      folder: ["Empty Folder", "Config-Folder"],
      selectedDrowpnItem: "create workflow-instance from template",
      dropwDown: ["import worfklow", "create workflow-instance from template"],
    };
  },
};
</script>