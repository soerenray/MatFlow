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
                :items="templatesName"
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
                ><send-icon
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
import Vue from "vue";
import CreateWorkflowInstance from "../Model/CreateWorkflowInstance";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";
import WorkflowInstance from '../Classes/WorkflowInstance';

const backendServerCommunicatorObject = new BackendServerCommunicator();
const createWorkflowInstanceObject = new CreateWorkflowInstance();

export default {
  data: function () {
    return {
      selectedDrowpnItem: "create workflow-instance from template",
      dropwDown: ["import worfklow", "create workflow-instance from template"],
    };
  },
  methods: {
    pressSendButton() {
      this.push();
      this.resetView();
    },
    resetView() {
    },
    pushCreateWorkflowInstanceFromTemplate() {
      backendServerCommunicatorObject.pushCreateWorkflowInstanceFromTemplate(this.createWorkflowInstanceObject())
    },
    createWorkflowInstanceObject(): WorkflowInstance {

    }
  },
  computed: {
    templatesName: {
      get: function (): string[] {
        return createWorkflowInstanceObject.templatesName;
      },
      set: function (templatesName: string[]) {
        createWorkflowInstanceObject.templatesName = templatesName;
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
    selectedTemplateName: {
      get: function (): string {
        return createWorkflowInstanceObject.selectedTemplateName;
      },
      set: function (selectedTemplateName: string) {
        createWorkflowInstanceObject.selectedTemplateName =
          selectedTemplateName;
      },
    },
    workflowInstanceName: {
      get: function (): string {
        return createWorkflowInstanceObject.workflowInstanceName;
      },
      set: function (worklfowInstanceName: string) {
        createWorkflowInstanceObject.workflowInstanceName =
          worklfowInstanceName;
      },
    },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // The object choosenConfigFileObject wouldn't update, when the parameters are
    // initialized in data
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(createWorkflowInstanceObject);
    createWorkflowInstanceObject.templatesName =
      backendServerCommunicatorObject.pullTemplatesName();
  },
};
</script>