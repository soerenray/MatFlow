<template>
  <v-app>
    <v-container>
      <v-col align="center">
        <v-card width="1000px">
          <v-data-table
            :headers="tableHeaders"
            :items="versions"
            item-key="name"
          >
            <template v-slot:[`item.parameterChanges`]="{ item }">
              <v-btn icon>
                <v-dialog v-model="dialogKeyValuePairs" max-width="600px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      @click="selectNewVersionObject(item)"
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
              ><v-btn icon><file-restore-icon></file-restore-icon></v-btn
            ></template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-container>
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
    selectNewVersionObject: function (selectedVersionObject: Version) {
      versionControlObject.selectedVersionObject = selectedVersionObject;
    },
    pullVersionsWithWorkflowInstanceName: function () {
      versionControlObject.versions =
        backendServerCommunicatorObject.pullVersionsWithWorkflowInstanceName(
          ""
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
        versionControlObject.versions;
      },
    },
    workflowInstanceName: {
      get: function (): string {
        return versionControlObject.workflowInstanceName;
      },
      set: function (workflowInstanceName: string) {
        versionControlObject.workflowInstanceName = workflowInstanceName;
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
    // Vue.observable has to be used to make an object outside of data reactive: https:///// v3.vuejs.org/guide/reactivity-fundamentals.html#declaring-reactive-state
    Vue.observable(versionControlObject);
  },
  created: function () {
    this.pullVersionsWithWorkflowInstanceName();
  },
};
</script>