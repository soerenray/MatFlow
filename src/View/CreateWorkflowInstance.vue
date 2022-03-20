<template>
  <v-app class="ma-4">
    <v-card flat>
      <v-card-title> Create new workflow-instance </v-card-title>
      <div class="ml-4">
        <v-select
          style="width: 80%"
          id="selectOptionToCreateWorkflowInstance"
          data-cy="selectOptionToCreateWorkflowInstance"
          :items="dropDownCreateOrImportWokflowInstance"
          :disabled="true"
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
                id="nameOfTheWorkflowInstance"
                data-cy="nameOfTheWorkflowInstance"
                variant="contained"
                label="Name of the workflow-instance"
                v-model="workflowInstanceName"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-select
                id="selectTemplateNameFromDropdown"
                variant="contained"
                data-cy="selectTemplateNameFromDropdown"
                :items="templatesName"
                v-model="selectedTemplateName"
                label="choose template"
              >
              </v-select>
            </v-col>
            <v-col>
              <v-file-input
                id="importConfigFiles"
                variant="contained"
                data-cy="importConfigFiles"
                @change="transformDagFilesToBase64"
                :multiple="true"
                :loading="
                  !areconfigFilesInBase64WithName && configFiles.length > 0
                "
                :disabled="
                  !areconfigFilesInBase64WithName &&
                  configFilesInBase64WithName.length > 0
                "
                v-model="configFiles"
                :clearable="false"
                accept="files"
                label="Config file folder"
              ></v-file-input>
            </v-col>
            <v-col>
              <v-btn
                id="sendWorkflowInstance"
                data-cy="sendWorkflowInstance"
                fab
                :disabled="
                  !(
                    areconfigFilesInBase64WithName &&
                    workflowInstanceName !== '' &&
                    selectedTemplateName !== '' &&
                    configFiles !== []
                  )
                "
                small
                @click="pressSendButton"
                color="#58D68D"
                style="padding-right:0.75px, padding-top:0.75px"
                ><v-icon>mdi-send</v-icon></v-btn
              >
            </v-col>
          </v-row>
        </div>
      </div>
      <div v-if="selectedDropDownItem == 'import worfklow'">
        <v-row>
          <v-col>
            <v-file-input
              v-model="workflowInstanceFolderAsArray"
              :clearable="false"
              accept="application/zip"
              label="Workflow-folder"
            ></v-file-input>
          </v-col>
          <v-col>
            <v-btn
              fab
              small
              @click="pressSendButton"
              color="#58D68D"
              style="padding-right:0.75px, padding-top:0.75px"
              ><v-icon>mdi-send</v-icon></v-btn
            ></v-col
          ></v-row
        >
      </div>
    </v-card>
  </v-app>
</template>

<script lang="ts">
// @ts-nocheck
import CreateWorkflowInstance from '@Model/CreateWorkflowInstance';
import CreateWorkflowInstanceCaretaker from '@Memento/CreateWorkflowInstanceCaretaker';
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';
import WorkflowInstance from '@Classes/WorkflowInstance';
import { filesToDataURLWithFunction } from '@Classes/base64Utility';

export default {
  name: 'CreateWorkflowInstance',
  data() {
    return {
      backendServerCommunicatorObject: new BackendServerCommunicator(),
      createWorkflowInstanceObject: new CreateWorkflowInstance(
        // ['import worfklow', 'create workflow-instance from template'],
        ['create workflow-instance from template'],
        'create workflow-instance from template',
      ),
      createWorkflowInstanceCaretakerObject:
        new CreateWorkflowInstanceCaretaker(),
    };
  },
  methods: {
    transformDagFilesToBase64() {
      filesToDataURLWithFunction(
        this.configFiles,
        (input: [ArrayBuffer | string, string][], isConverted: boolean) => {
          this.configFilesInBase64WithName = input;
          this.areconfigFilesInBase64WithName = isConverted;
        },
      );
    },
    async pressSendButton() {
      this.pushCreateWorkflowInstanceFromTemplate();
      this.resetView();

      this.createWorkflowInstanceObject.templatesName = await this
        .backendServerCommunicatorObject.pullTemplatesName();
    },
    resetView() {
      this.createWorkflowInstanceObject.setCreateWorkflowInstanceMemento(
        this.createWorkflowInstanceCaretakerObject
          .createWorkflowInstanceMementoObjects[0],
      );
    },
    pushCreateWorkflowInstanceFromTemplate() {
      if (
        this.createWorkflowInstanceObject.selectedDropDownItem
        === 'create workflow-instance from template'
      ) {
        this.backendServerCommunicatorObject.pushCreateWorkflowInstanceFromTemplate(
          this.workflowInstanceName,
          this.selectedTemplateName,
          this.configFilesInBase64WithName,
        );
      } else {
        this.backendServerCommunicatorObject.pushExistingWorkflowInstance(
          this.workflowInstanceFolder,
        );
      }
    },
    createNewWorkflowInstanceObject(
      workflowInstanceFolder: File,
      workflowInstanceName: string,
    ): WorkflowInstance {
      return new WorkflowInstance(workflowInstanceFolder, workflowInstanceName);
    },
  },
  computed: {
    dropDownCreateOrImportWokflowInstance: {
      get(): string[] {
        return this.createWorkflowInstanceObject
          .dropDownCreateOrImportWokflowInstance;
      },
      set(dropDownCreateOrImportWokflowInstance: string[]) {
        this.createWorkflowInstanceObject
          .dropDownCreateOrImportWokflowInstance = dropDownCreateOrImportWokflowInstance;
      },
    },
    selectedDropDownItem: {
      get(): string {
        return this.createWorkflowInstanceObject.selectedDropDownItem;
      },
      set(selectedDropDownItem: string) {
        this.createWorkflowInstanceObject.selectedDropDownItem = selectedDropDownItem;
      },
    },
    templatesName: {
      get(): string[] {
        return this.createWorkflowInstanceObject.templatesName;
      },
      set(templatesName: string[]) {
        this.createWorkflowInstanceObject.templatesName = templatesName;
      },
    },
    configFiles: {
      get(): File[] {
        return this.createWorkflowInstanceObject.configFiles;
      },
      set(configFiles: File[]) {
        this.createWorkflowInstanceObject.configFiles = configFiles;
      },
    },
    workflowInstanceFolderAsArray: {
      get(): File[] {
        return [this.createWorkflowInstanceObject.workflowInstanceFolder];
      },
      set(workflowInstanceFolder: File[]) {
        [this.createWorkflowInstanceObject.workflowInstanceFolder] = workflowInstanceFolder;
      },
    },
    workflowInstanceFolder: {
      get(): File {
        return this.createWorkflowInstanceObject.workflowInstanceFolder;
      },
      set(workflowInstanceFolder: File) {
        this.createWorkflowInstanceObject.workflowInstanceFolder = workflowInstanceFolder;
      },
    },
    selectedTemplateName: {
      get(): string {
        return this.createWorkflowInstanceObject.selectedTemplateName;
      },
      set(selectedTemplateName: string) {
        this.createWorkflowInstanceObject.selectedTemplateName = selectedTemplateName;
      },
    },
    workflowInstanceName: {
      get(): string {
        return this.createWorkflowInstanceObject.workflowInstanceName;
      },
      set(workflowInstanceName: string) {
        this.createWorkflowInstanceObject.workflowInstanceName = workflowInstanceName;
      },
    },
    areconfigFilesInBase64WithName: {
      get(): boolean {
        return this.createWorkflowInstanceObject.areconfigFilesInBase64WithName;
      },
      set(areconfigFilesInBase64WithName: boolean) {
        this.createWorkflowInstanceObject
          .areconfigFilesInBase64WithName = areconfigFilesInBase64WithName;
      },
    },
    configFilesInBase64WithName: {
      get(): [ArrayBuffer, string][] {
        return this.createWorkflowInstanceObject.configFilesInBase64WithName;
      },
      set(configFilesInBase64WithName: [ArrayBuffer, string][]) {
        this.createWorkflowInstanceObject.configFilesInBase64WithName = configFilesInBase64WithName;
      },
    },
  },
  async created() {
    await this.backendServerCommunicatorObject
      .pullTemplatesName()
      .then((res) => {
        res.forEach((elem) => {
          this.createWorkflowInstanceObject.templatesName.push(elem);
        });
      });
    // For now this is everthing I want to recover
    this.createWorkflowInstanceCaretakerObject.addCreateWorkflowInstanceMementoObjectToArray(
      this.createWorkflowInstanceObject.createWorkflowInstanceMemento(),
    );
  },
};
</script>
