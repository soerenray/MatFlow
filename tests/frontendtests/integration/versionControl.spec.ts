/// <reference types="cypress" />

import { mountCallback } from '@cypress/vue';
import VersionControlView from '@View/VersionControl.vue';
import vuetify from '@/plugins/vuetify';
import VersionControlModel from '@Model/VersionControl';
import { camelize } from 'vue';
import Version from '@Classes/Version';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

BackendServerCommunicatorSimulation.prototype
  . pullVersionsWithWorkflowInstanceName = async () => this.versions;
BackendServerCommunicatorSimulation.prototype
  . pullWorkflowInstancesNameAndConfigFilesName = async () => this
    .workflowInstancesNameAndConfigFilesName;

const workflowInstance1Version1 = new Version('1.1', 'changed value of key1', [['key1: Ipsom lorum', 'key1: lorem ipsum'], ['key1: xy', 'key2: xy'],
  ['key3: 5.0 5.0', "key3: 'text'"]]);
const workflowInstance1Version2 = new Version('1.1.1', 'reverted previous change', [['key1: Ipsom lorum', 'key1: lorem ipsum'], ['key1: xy', 'key2: xy'],
  ['key3: 5.0 5.0', "key3: 'text'"]]);
const workflowInstance2Version1 = new Version('2.1', 'changed name of key3', [['key3: Foo bar', 'key1: Foo bar']]);
const workflowInstance2Version2 = new Version('2.2', 'fixed typo in key-value', [['key1: xy', 'key1: xy'], ['key2: 42', 'key2: 420'],
]);

const backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();

backendServerCommunicatorObject.workflowInstancesNameAndConfigFilesName = [
  ['workflowInstance1', [
    'conf1',
    'conf2',
  ]],
  ['workflowInstance2', [
    'conf1',
    'conf2',
    'conf3',
  ]],
];

describe('VersionControl workflowInstance-button check', () => {
  beforeEach(
    mountCallback(VersionControlView, {
      data() {
        return {
          backendServerCommunicatorObject,
          versionControlObject: new VersionControlModel([
            { text: 'Version number', value: 'versionNumber' },
            { text: 'Version notes', value: 'versionNote' },
            { text: 'Changed parameters', value: 'parameterChanges' },
            { text: 'Load into current workspace', value: 'workspace' },
          ]),
        };
      },
      extensions: {
        use: vuetify,
      },
    }),
  );
  it('There are exactly two workflowInstances to choose from', () => {
    cy.get('[data-cy=workflowInstancesName] .v-col').should('have.length', 2);
  });

  it('The workflowInstances should be colored white as default', () => {
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).should('have.css', 'background-color', 'rgb(255, 255, 255)');
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).should('have.css', 'background-color', 'rgb(255, 255, 255)');
  });

  it('The workflowInstances to choose from have the correct name in the correct order', () => {
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).should('have.text', 'workflowInstance1');
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).should('have.text', 'workflowInstance2');
  });

  it("The element from workflowInstance1 is colored blue when 'workflowInstance1' is pressed", () => {
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).click();
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).should('have.css', 'background-color', 'rgb(169, 204, 227)');
  });

  it("The element from workflowInstance2 is colored blue when 'workflowInstance2' is pressed", () => {
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).click();
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).should('have.css', 'background-color', 'rgb(169, 204, 227)');
  });

  it("The element from workflowInstance2 is colored white after 'workflowInstance2' is pressed and then 'workflowInstance1' is pressed", () => {
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).click();
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).click();
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).should('have.css', 'background-color', 'rgb(255, 255, 255)');
  });

  it("The element from workflowInstance1 is colored white after 'workflowInstance1' is pressed and then 'workflowInstance2' is pressed", () => {
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).click();
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).click();
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).should('have.css', 'background-color', 'rgb(255, 255, 255)');
  });
});

describe('VersionControl table content check', () => {
  beforeEach(
    mountCallback(VersionControlView, {
      data() {
        return {
          backendServerCommunicatorObject,
          versionControlObject: new VersionControlModel([
            { text: 'Version number', value: 'versionNumber' },
            { text: 'Version notes', value: 'versionNote' },
            { text: 'Changed parameters', value: 'parameterChanges' },
            { text: 'Load into current workspace', value: 'workspace' },
          ]),
        };
      },
      extensions: {
        use: vuetify,
      },
    }),
  );

  it('The table-headers should contain the correct entries with the correct order', () => {
    cy.get('[data-cy=tableHeader] > td').eq(0).should('have.text', 'Version number');
    cy.get('[data-cy=tableHeader] > td').eq(1).should('have.text', 'Version notes');
    cy.get('[data-cy=tableHeader] > td').eq(2).should('have.text', 'Changed parameters');
    cy.get('[data-cy=tableHeader] > td').eq(3).should('have.text', 'Load into current workspace');
  });

  it('The table should not contain any entry as default (since no workflowInstance is selected)', () => {
    cy.get('[data-cy=tableBody] > tr').should('not.exist');
  });

  it('The tablebody with elements should exist after workflowInstance1 is clicked', () => {
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).click();
    backendServerCommunicatorObject.versions = [workflowInstance1Version1, workflowInstance1Version2];
    cy.get('[data-cy=tableBody] > tr').should('exist');
  });

  it("The tablebody has the correct (versionNumber, version note)-pairs in the correct order after clicked on 'workflowInstance1'", () => {
    backendServerCommunicatorObject.versions = [workflowInstance1Version1, workflowInstance1Version2];
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).click();
    cy.get('[data-cy=tableBody] > tr').eq(0).children().eq(0)
      .should('have.text', '1.1');
    cy.get('[data-cy=tableBody] > tr').eq(0).children().eq(1)
      .should('have.text', 'changed value of key1');
    cy.get('[data-cy=tableBody] > tr').eq(1).children().eq(0)
      .should('have.text', '1.1.1');
    cy.get('[data-cy=tableBody] > tr').eq(1).children().eq(1)
      .should('have.text', 'reverted previous change');
  });

  it("The tablebody has the correct (versionNumber, version note)-pairs in the correct order after clicked on 'workflowInstance1' and then 'workflowInstance2'", () => {
    backendServerCommunicatorObject.versions = [workflowInstance1Version1, workflowInstance1Version2];
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).click().then(() => {
      backendServerCommunicatorObject.versions = [workflowInstance2Version1, workflowInstance2Version2];
    });
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).click();
    cy.get('[data-cy=tableBody] > tr').eq(0).children().eq(0)
      .should('have.text', '2.1');
    cy.get('[data-cy=tableBody] > tr').eq(0).children().eq(1)
      .should('have.text', 'changed name of key3');
    cy.get('[data-cy=tableBody] > tr').eq(1).children().eq(0)
      .should('have.text', '2.2');
    cy.get('[data-cy=tableBody] > tr').eq(1).children().eq(1)
      .should('have.text', 'fixed typo in key-value');
  });

  it('The headers of keyValuePairs are displayed correctly in the correct order', () => {
    backendServerCommunicatorObject.versions = [workflowInstance1Version1, workflowInstance1Version2];
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).click();
    cy.get('[data-cy=fileButton]').eq(0).click();
    cy.get('[data-cy=keyValuePair] [data-cy=tableHeader] > td').eq(0).should('have.text', 'old value');
    cy.get('[data-cy=keyValuePair] [data-cy=tableHeader] > td').eq(1).should('have.text', 'new value');
  });

  it("The changed parameters of version '1.1' of 'workflowInstance1' should be displayed correctly in the correct order", () => {
    backendServerCommunicatorObject.versions = [workflowInstance1Version1, workflowInstance1Version2];
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(0).click();
    cy.get('[data-cy=fileButton]').eq(0).click();
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(0).children().eq(0)
      .should('have.text', 'key1: Ipsom lorum');
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(1).children().eq(0)
      .should('have.text', 'key1: xy');
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(2).children().eq(0)
      .should('have.text', 'key3: 5.0 5.0');
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(0).children().eq(1)
      .should('have.text', 'key1: lorem ipsum');
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(1).children().eq(1)
      .should('have.text', 'key2: xy');
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(2).children().eq(1)
      .should('have.text', "key3: 'text'");
  });

  it("The changed parameters of version '2.2' of 'workflowInstance2' should be displayed correctly in the correct order", () => {
    backendServerCommunicatorObject.versions = [workflowInstance2Version1, workflowInstance2Version2];
    cy.get('[data-cy=workflowInstancesName] .v-col').eq(1).click();
    cy.get('[data-cy=fileButton]').eq(1).click();
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(0).children().eq(0)
      .should('have.text', 'key1: xy');
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(1).children().eq(0)
      .should('have.text', 'key2: 42');
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(0).children().eq(1)
      .should('have.text', 'key1: xy');
    cy.get('[data-cy=keyValuePair] [data-cy=tableBody] > tr').eq(1).children().eq(1)
      .should('have.text', 'key2: 420');
  });
});
