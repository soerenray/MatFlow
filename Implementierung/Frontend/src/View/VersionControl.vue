<template>
  <v-app>
    <v-container>
      <v-col align="center">
        <v-card width="1000px">
          <v-data-table
            :headers="headers"
            :items="versionsTableObject"
            item-key="name"
          >
            <template v-slot:[`item.parameterChanges`]="{ item }">
              <v-btn icon>
                <v-dialog v-model="dialoge" max-width="600px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      @click="handleEvent(item)"
                      icon
                      v-bind="attrs"
                      v-on="on"
                    >
                      <file-document-outline-icon></file-document-outline-icon>
                    </v-btn>
                  </template>
                  <key-value-pairs
                    :parameter-changes="
                      getKeyValuePairsByVersionNumber(
                        selectedItem.versionNumber
                      )
                    "
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

interface VersionsTableObject {
  versionNumber: string;
  versionNote: string;
}

const backendServerCommunicatorObject = new BackendServerCommunicator();
const versionControlObject = new VersionControl();

export default {
  name: "VersionControl",
  data: function () {
    return {
      dialoge: false,
      selectedVersion: "",
      selectedItem: {},
      headers: [
        { text: "Version number", value: "versionNumber" },
        { text: "Version notes", value: "versionNote" },
        { text: "Changed parameters", value: "parameterChanges" },
        { text: "Load into current workspace", value: "workspace" },
      ],
    };
  },
  components: {
    KeyValuePairs,
  },
  methods: {
    handleEvent: function (selectedItem: any) {
      this.selectedItem = selectedItem;
    },
    pullVersionsWithWorkflowInstanceName: function () {
      versionControlObject.versions =
        backendServerCommunicatorObject.pullVersionsWithWorkflowInstanceName(
          ""
        );
    },
    getKeyValuePairsByVersionNumber: function (
      versionNumber: string
    ): Array<[string, string]> {
      let keyValuePairs = new Array<[string, string]>(["", ""]);
      let temp = versionControlObject.versions.find(
        (version: Version): Boolean => {
          return version.versionNumber === versionNumber;
        }
      );
      if (temp !== undefined) {
        keyValuePairs = temp.parameterChanges;
      }
      return keyValuePairs;
    },
  },
  computed: {
    versionsTableObject: {
      get: function (): Array<VersionsTableObject> {
        return versionControlObject.versions.map(
          (version: Version): VersionsTableObject => {
            return {
              versionNumber: version.versionNumber,
              versionNote: version.versionNote,
            };
          }
        );
      },
    },
    tableHeaders: {
      get: function () {
        return versionControlObject.tableHeaders;
      },
      set: function (tableHeaders: object[]) {
        versionControlObject.tableHeaders = tableHeaders;
      },
    },
    versions: {
      get: function () {
        return versionControlObject.versions;
      },
      set: function (versions: Version[]) {
        versionControlObject.versions;
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