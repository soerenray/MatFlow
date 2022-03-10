<template>
  <v-app>
    <v-card>
      <v-card-title> Create new workflow-instance </v-card-title>
      <div style="padding-left: 20px">
        <v-select
          :items="dropDownCreateOrImportWokflowInstance"
          v-model="selectedDropDownItem"
        ></v-select>
        <div
          v-if="
            selectedDropDownItem == 'create workflow-instance from template'
          "
        >
          <v-row>
            <v-col>
              <v-text-field
                label="Name of the workflow-instance"
                v-model="workflowInstanceName"
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
                :clearable="false"
                accept="application/zip"
                label="Config file folder"
              ></v-file-input>
            </v-col>
            <v-col>
              <v-btn
                fab
                small
                @click="pressSendButton"
                color="#58D68D"
                style="padding-right:0.75px, padding-top:0.75px"
                ><send-icon
              /></v-btn>
            </v-col>
          </v-row>
        </div>
      </div>
      <div v-if="selectedDropDownItem == 'import worfklow'">
        <v-row>
          <v-col>
            <v-file-input
              v-model="workflowInstanceFolder"
              :clearable="false"
              accept="application/zip"
              label="Workflow-folder"
            ></v-file-input
          ></v-col>
          <v-col>
            <v-btn
              fab
              small
              @click="pressSendButton"
              color="#58D68D"
              style="padding-right:0.75px, padding-top:0.75px"
              ><send-icon /></v-btn></v-col
        ></v-row>
      </div>
    </v-card>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";
import CreateWorkflowInstance from "@Model/CreateWorkflowInstance";
import CreateWorkflowInstanceCaretaker from "@Memento/CreateWorkflowInstanceCaretaker";
import BackendServerCommunicator from "@Controler/BackendServerCommunicator";
import WorkflowInstance from "@Classes/WorkflowInstance";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const createWorkflowInstanceObject = new CreateWorkflowInstance(
  ["import worfklow", "create workflow-instance from template"],
  "create workflow-instance from template"
);

const createWorkflowInstanceCaretakerObject =
  new CreateWorkflowInstanceCaretaker();
//For now this is everthing I want to recover
createWorkflowInstanceCaretakerObject.addCreateWorkflowInstanceMementoObjectToArray(
  createWorkflowInstanceObject.createWorkflowInstanceMemento()
);

export default {
  name: "CreateWorkflowInstance",
  methods: {
    pressSendButton() {
      this.pushCreateWorkflowInstanceFromTemplate();
      this.resetView();
      createWorkflowInstanceObject.templatesName =
        backendServerCommunicatorObject.pullTemplatesName();
    },
    resetView() {
      createWorkflowInstanceObject.setCreateWorkflowInstanceMemento(
        createWorkflowInstanceCaretakerObject
          .createWorkflowInstanceMementoObjects[0]
      );
    },
    pushCreateWorkflowInstanceFromTemplate() {
      if (
        createWorkflowInstanceObject.selectedDropDownItem ==
        "create workflow-instance from template"
      ) {
        backendServerCommunicatorObject.pushCreateWorkflowInstanceFromTemplate(
          this.createWorkflowInstanceObject(
            this.workflowInstanceFolder,
            this.workflowInstanceName
          )
        );
      } else {
        backendServerCommunicatorObject.pushExistingWorkflowInstance(
          this.workflowInstanceFolder
        );
      }
    },
    createWorkflowInstanceObject(
      workflowInstanceFolder: File,
      workflowInstanceName: string
    ): WorkflowInstance {
      return new WorkflowInstance(workflowInstanceFolder, workflowInstanceName);
    },
  },
  computed: {
    dropDownCreateOrImportWokflowInstance: {
      get: function (): string[] {
        return createWorkflowInstanceObject.dropDownCreateOrImportWokflowInstance;
      },
      set: function (dropDownCreateOrImportWokflowInstance: string[]) {
        createWorkflowInstanceObject.dropDownCreateOrImportWokflowInstance =
          dropDownCreateOrImportWokflowInstance;
      },
    },
    selectedDropDownItem: {
      get: function (): string {
        return createWorkflowInstanceObject.selectedDropDownItem;
      },
      set: function (selectedDropDownItem: string) {
        createWorkflowInstanceObject.selectedDropDownItem =
          selectedDropDownItem;
      },
    },
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
  beforeCreate: async function () {
    // Vue is oberserving data in the data property.
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(createWorkflowInstanceObject);
    createWorkflowInstanceObject.templatesName =
      await backendServerCommunicatorObject.pullTemplatesName();
  },
};
</script>