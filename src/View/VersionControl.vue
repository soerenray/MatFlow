<template>
  <v-app>
    <v-row style="padding-left: 30px; padding-top: 30px">
      <v-card style="padding-right: 5px">
        <v-col></v-col>
        <v-col></v-col>
        <v-divider></v-divider>
        <div
          data-cy="workflowInstancesName"
          v-for="workflowInstanceName in workflowInstancesName"
          :key="workflowInstanceName"
        >
          <v-col
            @click="
              selectWorkflowInstanceNameAndPullVersions(workflowInstanceName)
            "
            v-if="selectedWorkflowInstanceName != workflowInstanceName"
            style="background-color: white"
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
        <v-table>
          <thead data-cy="tableHeader">
            <tr>
              <td v-for="header in tableHeaders" :key="header.name">
                {{ header.text }}
              </td>
            </tr>
          </thead>
          <tbody data-cy="tableBody">
            <v-col></v-col>
            <tr v-for="version in versions" :key="version.name">
              <td>{{ version.versionNumber }}</td>
              <td>{{ version.versionNote }}</td>
              <td>
                <v-btn size="small" icon>
                  <v-dialog
                    class="mx-auto mt-8"
                    v-model="dialogKeyValuePairs"
                    max-width="600px"
                  >
                    <template v-slot:activator="{ props }">
                      <v-btn
                        data-cy="fileButton"
                        @click="selectedVersionObject = version"
                        size="small"
                        icon
                        v-bind="props"
                      >
                        <v-icon>mdi-file</v-icon>
                      </v-btn>
                    </template>
                    <key-value-pairs
                      data-cy="keyValuePair"
                      :parameter-changes="
                        selectedVersionObject.parameterChanges
                      "
                    ></key-value-pairs>
                  </v-dialog>
                </v-btn>
              </td>
              <td>
                <v-btn
                  size="small"
                  @click="pushReplaceActiveVersionOfWorkflowInstance"
                  icon
                  ><v-icon>mdi-file-restore</v-icon></v-btn
                >
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card>
    </v-row>
  </v-app>
</template>

<script lang='ts'>
// @ts-nocheck
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';
import Version from '@Classes/Version';
import VersionControl from '@Model/VersionControl';

import KeyValuePairs from '@View/KeyValuePairs.vue';

export default {
  name: 'VersionControl',
  data() {
    return {
      backendServerCommunicatorObject: new BackendServerCommunicator(),
      versionControlObject: new VersionControl([
        { text: 'Version number', value: 'versionNumber' },
        { text: 'Version notes', value: 'versionNote' },
        { text: 'Changed parameters', value: 'parameterChanges' },
        { text: 'Load into current workspace', value: 'workspace' },
      ]),
    };
  },
  components: {
    KeyValuePairs,
  },
  methods: {
    selectWorkflowInstanceNameAndPullVersions(
      selectedWorkflowInstanceName: string,
    ) {
      this.selectedWorkflowInstanceName = selectedWorkflowInstanceName;
      this.pullVersionsWithWorkflowInstanceName();
    },
    async pullVersionsWithWorkflowInstanceName() {
      this.versionControlObject.versions = await this
        .backendServerCommunicatorObject.pullVersionsWithWorkflowInstanceName(
          this.selectedWorkflowInstanceName,
        );
    },
    pullWorkflowInstancesName() {
      this.workflowInstancesName = this.backendServerCommunicatorObject
        .pullWorkflowInstancesNameAndConfigFilesName()
        .map((workflowInstanceNameAndConfigFilesName) => workflowInstanceNameAndConfigFilesName[0]);
    },
    pushReplaceActiveVersionOfWorkflowInstance() {
      this.backendServerCommunicatorObject.pushReplaceActiveVersionOfWorkflowInstance(
        this.selectedWorkflowInstanceName,
        this.selectedVersionObject.versionNumber,
      );
    },
  },
  computed: {
    tableHeaders: {
      get(): object[] {
        return this.versionControlObject.tableHeaders;
      },
      set(tableHeaders: object[]) {
        this.versionControlObject.tableHeaders = tableHeaders;
      },
    },
    dialogKeyValuePairs: {
      get(): boolean {
        return this.versionControlObject.dialogKeyValuePairs;
      },
      set(dialogKeyValuePairs: boolean) {
        this.versionControlObject.dialogKeyValuePairs = dialogKeyValuePairs;
      },
    },
    selectedVersionObject: {
      get(): Version {
        return this.versionControlObject.selectedVersionObject;
      },
      set(selectedVersionObject: Version) {
        this.versionControlObject.selectedVersionObject = selectedVersionObject;
      },
    },
    versions: {
      get(): Version[] {
        return this.versionControlObject.versions;
      },
      set(versions: Version[]) {
        this.versionControlObject.versions = versions;
      },
    },
    selectedWorkflowInstanceName: {
      get(): string {
        return this.versionControlObject.selectedWorkflowInstanceName;
      },
      set(selectedWorkflowInstanceName: string) {
        this.versionControlObject.selectedWorkflowInstanceName = selectedWorkflowInstanceName;
      },
    },
    workflowInstancesName: {
      get(): string[] {
        return this.versionControlObject.workflowInstancesName;
      },
      set(workflowInstancesName: string[]) {
        this.versionControlObject.workflowInstancesName = workflowInstancesName;
      },
    },
  },
  created() {
    this.pullWorkflowInstancesName();
  },
};
</script>
