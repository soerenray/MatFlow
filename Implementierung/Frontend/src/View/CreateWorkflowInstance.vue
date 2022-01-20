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
              <v-select
                :items="templates"
                v-model="selectedTemplateName"
                label="choose template"
              >
              </v-select>
            </v-col>
            <v-col>
              <v-file-input
                v-model="configFolder"
                accept="application/zip"
                label="Config file folder"
              ></v-file-input>
            </v-col>
            <v-col>
              <v-btn
                fab
                small
                color="#58D68D"
                style="padding-right:0.75px, padding-top:0.75px"
                ><plus-icon :size="30"
              /></v-btn>
            </v-col>
          </v-row>
        </div>
      </div>
      <div v-if="selectedDrowpnItem == 'import worfklow-instance'">
        <v-file-input
          v-model="workflowInstanceFolder"
          accept="application/zip"
          label="Workflow-folder"
        ></v-file-input>
      </div>
    </v-card>
  </v-app>
</template>

<script lang='ts'>
import CreateWorkflowInstance from "../Model/CreateWorkflowInstance";

let createWorkflowInstanceObject = new CreateWorkflowInstance();

export default {
  data: function () {
    return {
      templates: createWorkflowInstanceObject.templatesName,
      folder: ["Empty Folder", "Config-Folder"],
      selectedDrowpnItem: "create workflow-instance from template",
      dropwDown: ["import worfklow", "create workflow-instance from template"],
    };
  },
  computed: {
    selectedTemplateName: {
      get: function (): string {
        return createWorkflowInstanceObject.selectedTemplateName;
      },
      set: function (selectedTemplateName: string) {
        createWorkflowInstanceObject.selectedTemplateName =
          selectedTemplateName;
      },
    },
    configFolder: {
      get: function (): File {
        return createWorkflowInstanceObject.configFolder;
      },
      set: function (configFolder: File) {
        createWorkflowInstanceObject.configFolder = configFolder;
      },
    },
    workflowInstanceFolder: {
      get: function (): File {
        return createWorkflowInstanceObject.workflowInstanceFolder;
      },
      set: function (workflowInstanceFolder: File) {
        createWorkflowInstanceObject.workflowInstanceFolder =
          workflowInstanceFolder;
      },
    },
  },
};
</script>