<template>
  <v-app>
    <v-card>
      <v-card-title> Create new template </v-card-title>
      <div style="padding-left: 20px">
        <v-row>
          <v-col>
            <v-text-field
              id="nameOfTheTempalte"
              data-cy="nameOfTheTemplate"
              label="Name of the template"
              variant="contained"
              style="width: 200px"
              v-model="newTemplateName"
              hide-details="auto"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-select
              data-cy="selectTemplateNameFromDropdown"
              id="selectTemplateNameFromDropdown"
              :items="templatesName"
              variant="contained"
              style="width: 200px"
              v-model="chosenTemplateName"
              label="use predefined template"
            >
            </v-select>
          </v-col>
          <v-col>
            <v-file-input
              data-cy="fileInput"
              id="fileInput"
              v-model="templateFolderAsArray"
              variant="contained"
              style="width: 200px"
              :clearable="false"
              accept="application/zip"
              label="import folder"
            >
            </v-file-input>
          </v-col>
          <v-col>
            <v-radio-group v-model="createFromEmptyFile">
              <v-radio data-cy="createFromEmptyFile">
                <template v-slot:label>
                  <div>
                    <div>
                      Create template from <br />
                      <strong>empty file</strong>
                    </div>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
          </v-col>
          <v-col>
            <v-row style="padding-top: 25px">
              <v-btn data-cy="editTemplate" color="blue">Edit</v-btn>
              <div style="padding-left: 25px">
                <v-btn
                  data-cy="sendTemplate"
                  @click="pressSendButton"
                  color="#58D68D"
                >
                  <v-icon> mdi-send </v-icon>
                </v-btn>
              </div>
            </v-row>
          </v-col>
          <v-col></v-col>
        </v-row>
      </div>
    </v-card>
  </v-app>
</template>

<script lang='ts'>
// @ts-nocheck
import CreateTemplate from '@Model/CreateTemplate';
import CreateTemplateCaretaker from '@Memento/CreateTemplateCaretaker';
import Template from '@Classes/Template';
import BackendServerCommunicator from '@Controler/BackendServerCommunicator';

export default {
  name: 'CreateTemplate',
  data() {
    return {
      backendServerCommunicatorObject: new BackendServerCommunicator(),
      createTemplateObject: new CreateTemplate(),
      createTemplateCaretakerObject: new CreateTemplateCaretaker(),
    };
  },
  methods: {
    pressSendButton() {
      this.pushTemplateObjectToBackend();
      this.resetView();
    },
    async resetView() {
      await this.backendServerCommunicatorObject.pullTemplatesName();
      this.createTemplateObject.setCreateTemplateMemento(
        this.createTemplateCaretakerObject.createTemplateMementoObjects[0],
      );
      await this
        .backendServerCommunicatorObject.pullTemplatesName().then((res) => {
          res.forEach((elem) => this.createTemplateObject.templatesName.push(elem));
        });
    },
    pushTemplateObjectToBackend() {
      this.backendServerCommunicatorObject.pushCreateTemplate(
        this.createNewTemplateObject(
          this.createTemplateObject.templateFolder,
          this.newTemplateName,
        ),
      );
    },
    createNewTemplateObject(
      templateBlueprintFile: File,
      templateName: string,
    ): Template {
      return new Template(templateBlueprintFile, templateName);
    },
  },
  computed: {
    newTemplateName: {
      get() {
        return this.createTemplateObject.newTemplateName;
      },
      set(newTemplateName: string) {
        this.createTemplateObject.newTemplateName = newTemplateName;
      },
    },
    templatesName: {
      get() {
        return this.createTemplateObject.templatesName;
      },
      set(templatesName: string[]) {
        this.createTemplateObject.templatesName = templatesName;
      },
    },
    chosenTemplateName: {
      get(): string {
        return this.createTemplateObject.chosenTemplateName;
      },
      set(chosenTemplateName: string) {
        this.createTemplateObject.chosenTemplateName = chosenTemplateName;
      },
    },
    templateFolderAsArray: {
      get(): File[] {
        return [this.createTemplateObject.templateFolder];
      },
      set(templateFolder: File[]) {
        [this.createTemplateObject.templateFolder] = templateFolder;
      },
    },
    templateFolder: {
      get(): File {
        return this.createTemplateObject.templateFolder;
      },
      set(templateFolder: File) {
        this.createTemplateObject.templateFolder = templateFolder;
      },
    },
    dagFile: {
      get(): File {
        return this.createTemplateObject.dagFile;
      },
      set(dagFile: File) {
        this.createTemplateObject.dagFile = dagFile;
      },
    },
    createFromEmptyFile: {
      get(): boolean {
        return this.createTemplateObject.createFromEmptyFile;
      },
      set(createFromEmptyFile: File) {
        this.createTemplateObject.createFromEmptyFile = createFromEmptyFile;
      },
    },
  },
  async created() {
    await this
      .backendServerCommunicatorObject.pullTemplatesName().then((res) => {
        res.forEach((elem) => this.createTemplateObject.templatesName.push(elem));
      });
    // For now this is everything I want to recover
    this.createTemplateCaretakerObject.addCreateTemplateMementoObjectToArray(
      this.createTemplateObject.createTemplateMemento(),
    );
  },
};
</script>
