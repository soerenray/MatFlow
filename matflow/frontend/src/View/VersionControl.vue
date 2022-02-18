<template>
  <v-app>
    <v-row style="padding-left: 30px; padding-top: 30px">
      <v-card style="padding-right: 5px">
        <v-col></v-col>
        <v-col></v-col>
        <v-divider></v-divider>
        <div
          v-for="workflowInstanceName in workflowInstancesName"
          :key="workflowInstanceName"
        >
          <v-col
            @click="
              selectWorkflowInstanceNameAndPullVersions(workflowInstanceName)
            "
            v-if="selectedWorkflowInstanceName != workflowInstanceName"
          >
            {{ workflowInstanceName }}
          </v-col>
          <v-col
            v-if="selectedWorkflowInstanceName == workflowInstanceName"
            style="background-color: #a9cce3"
          >
            {{ workflowInstanceName }}
          </v-col>
          <v-divider></v-divider>
        </div>
      </v-card>
      <v-card width="700px">
        <v-data-table :headers="tableHeaders" :items="versions" item-key="name">
          <template v-slot:[`item.parameterChanges`]="{ item }">
            <v-btn icon>
              <v-dialog v-model="dialogKeyValuePairs" max-width="600px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    @click="selectedVersionObject = item"
                    icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    <file-document-outline-icon></file-document-outline-icon>
                  </v-btn>
                </template>
                <key-value-pairs
                  :parameter-changes="selectedVersionObject.parameterChanges"
                ></key-value-pairs>
              </v-dialog>
            </v-btn>
          </template>
          <template v-slot:[`item.workspace`]="{}"
            ><v-btn @click="pushReplaceActiveVersionOfWorkflowInstance" icon
              ><file-restore-icon></file-restore-icon></v-btn
          ></template>
        </v-data-table>
      </v-card>
    </v-row>
  </v-app>
</template>

<script lang='ts'>
import Vue from "vue";
import BackendServerCommunicator from "../Controler/BackendServerCommunicator";
import Version from "../Classes/Version";
import VersionControl from "../Model/VersionControl";
import KeyValuePairs from "./KeyValuePairs.vue";

const backendServerCommunicatorObject = new BackendServerCommunicator();
const versionControlObject = new VersionControl([
  { text: "Version number", value: "versionNumber" },
  { text: "Version notes", value: "versionNote" },
  { text: "Changed parameters", value: "parameterChanges" },
  { text: "Load into current workspace", value: "workspace" },
]);

export default {
  name: "VersionControl",
  components: {
    KeyValuePairs,
  },
  methods: {
    selectWorkflowInstanceNameAndPullVersions(
      selectedWorkflowInstanceName: string
    ) {
      this.selectedWorkflowInstanceName = selectedWorkflowInstanceName;
      this.pullVersionsWithWorkflowInstanceName();
    },
    pullVersionsWithWorkflowInstanceName: function () {
      versionControlObject.versions =
        backendServerCommunicatorObject.pullVersionsWithWorkflowInstanceName(
          this.selectedWorkflowInstanceName
        );
    },
    pullWorkflowInstancesName: function () {
      this.workflowInstancesName = backendServerCommunicatorObject
        .pullWorkflowInstancesNameAndConfigFilesName()
        .map((workflowInstanceNameAndConfigFilesName) => {
          return workflowInstanceNameAndConfigFilesName[0];
        });
    },
    pushReplaceActiveVersionOfWorkflowInstance() {
      backendServerCommunicatorObject.pushReplaceActiveVersionOfWorkflowInstance(
        this.selectedWorkflowInstanceName,
        this.selectedVersionObject.versionNumber
      );
    },
  },
  computed: {
    tableHeaders: {
      get: function (): object[] {
        return versionControlObject.tableHeaders;
      },
      set: function (tableHeaders: object[]) {
        versionControlObject.tableHeaders = tableHeaders;
      },
    },
    dialogKeyValuePairs: {
      get: function (): boolean {
        return versionControlObject.dialogKeyValuePairs;
      },
      set: function (dialogKeyValuePairs: boolean) {
        versionControlObject.dialogKeyValuePairs = dialogKeyValuePairs;
      },
    },
    selectedVersionObject: {
      get: function (): Version {
        return versionControlObject.selectedVersionObject;
      },
      set: function (selectedVersionObject: Version) {
        versionControlObject.selectedVersionObject = selectedVersionObject;
      },
    },
    versions: {
      get: function (): Version[] {
        return versionControlObject.versions;
      },
      set: function (versions: Version[]) {
        versionControlObject.versions = versions;
      },
    },
    selectedWorkflowInstanceName: {
      get: function (): string {
        return versionControlObject.selectedWorkflowInstanceName;
      },
      set: function (selectedWorkflowInstanceName: string) {
        versionControlObject.selectedWorkflowInstanceName =
          selectedWorkflowInstanceName;
      },
    },
    workflowInstancesName: {
      get: function (): string[] {
        return versionControlObject.workflowInstancesName;
      },
      set: function (workflowInstancesName: string[]) {
        versionControlObject.workflowInstancesName = workflowInstancesName;
      },
    },
  },
  beforeCreate: function () {
    // Vue is oberserving data in the data property.
    // Vue.observable has to be used to make an object outside of data reactive:
    // https://v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(versionControlObject);
  },
  created: function () {
    this.pullWorkflowInstancesName();
  },
};
</script>