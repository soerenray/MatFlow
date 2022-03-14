<template>
  <v-app>
    <v-card>
      <v-card-title> Create new workflow-instance </v-card-title>
      <div style="padding-left: 20px">
        <v-select
          id="selectOptionToCreateWorkflowInstance"
          data-cy="selectOptionToCreateWorkflowInstance"
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
                id="nameOfTheWorkflowInstance"
                data-cy="nameOfTheWorkflowInstance"
                label="Name of the workflow-instance"
                v-model="workflowInstanceName"
                hide-details="auto"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-select
                id="selectTemplateNameFromDropdown"
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
                data-cy="importConfigFiles"
                :multiple="true"
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

<script lang='ts'>
// @ts-nocheck
import CreateWorkflowInstance from '@Model/CreateWorkflowInstance';
import CreateWorkflowInstanceCaretaker from '@Memento/CreateWorkflowInstanceCaretaker';
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';
import WorkflowInstance from '@Classes/WorkflowInstance';

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
    async pressSendButton() {
      this.pushCreateWorkflowInstanceFromTemplate();
      this.resetView();
      await this
        .backendServerCommunicatorObject.pullTemplatesName().then((res) => {
          res.forEach((elem) => {
            this.createWorkflowInstanceObject.templatesName.push(elem);
          });
        });
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
          this.createNewWorkflowInstanceObject(
            this.workflowInstanceFolder,
            this.workflowInstanceName,
          ),
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
      set(worklfowInstanceName: string) {
        this.createWorkflowInstanceObject.workflowInstanceName = worklfowInstanceName;
      },
    },
  },
  async created() {
    await this
      .backendServerCommunicatorObject.pullTemplatesName().then((res) => {
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
