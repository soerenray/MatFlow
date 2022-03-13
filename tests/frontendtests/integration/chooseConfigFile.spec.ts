/// <reference types="cypress" />

// @ts-ignore
/* eslint-disable */

import { mountCallback } from '@cypress/vue';
import ChooseConfigFileView from '@View/ChooseConfigFile.vue';
import vuetify from '@/plugins/vuetify';
import ChooseConfigFileModel from '@Model/ChooseConfigFile';
import ConfigFile from '@Classes/ConfigFile';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

const workflowInstancesAndConfigFilesName = [['workflowInstance1', ['conf1', 'conf2']], ['workflowInstance2', ['conf1', 'conf2', 'conf3']]];
const workflow1Conf1 = new ConfigFile('conf1', [['key1', 'val1'], ['key2', 'val2']]);
const workflow1Conf2 = new ConfigFile('conf2', [['key1', 'val1'], ['key2', 'val2'], ['key3', 'val3']]);
const workflow2Conf1 = new ConfigFile('conf1', [['key1', 'val1']]);
const workflow2Conf2 = new ConfigFile('conf2', [['key1', 'val1'], ['key2', 'val2']]);
const workflow2Conf3 = new ConfigFile('conf3', [['key1', 'val1'], ['key2', 'val2'], ['key3', 'val3']]);

// Simulated backend-behavior
BackendServerCommunicatorSimulation.prototype
  . pullConfigFileWithConfigFileNameWithWorkflowInstanceName = async () => this.configFile;
BackendServerCommunicatorSimulation.prototype
  . pullWorkflowInstancesNameAndConfigFilesName = async () => this
    .workflowInstancesNameAndConfigFilesName;

const backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
backendServerCommunicatorObject.workflowInstancesNameAndConfigFilesName = [['workflowInstance1', ['conf1', 'conf2']], ['workflowInstance2', ['conf1', 'conf2', 'conf3']]];

beforeEach(
  mountCallback(ChooseConfigFileView, {
    data() {
      return {
        backendServerCommunicatorObject,
        chooseConfigFileObject: new ChooseConfigFileModel(),
      };
    },
    extensions: {
      use: vuetify,
    },
  }),
);

describe('ChooseConfigFile', () => {
  it('selected workflowInstances should be colored blue', () => {
    cy.contains('workflowInstance1').click();
    // color in hex: #a9cce3
    cy.contains('workflowInstance1').should('have.css', 'background-color', 'rgb(169, 204, 227)');

    cy.contains('workflowInstance2').click();
    // color in hex: #a9cce3
    cy.contains('workflowInstance2').should('have.css', 'background-color', 'rgb(169, 204, 227)');
  });

  it('not selected workflowInstances should be colored white', () => {
    console.log(cy);
    cy.contains('workflowInstance1').should('have.css', 'background-color', 'rgb(255, 255, 255)');
    cy.contains('workflowInstance2').should('have.css', 'background-color', 'rgb(255, 255, 255)');
  });

  it('not selected workflowInstances should be colored white', () => {
    cy.contains('workflowInstance1').click();
    // color in hex: #a9cce3
    cy.contains('workflowInstance1').should('have.css', 'background-color', 'rgb(169, 204, 227)');

    cy.contains('workflowInstance2').click();
    // color in hex: #a9cce3
    cy.contains('workflowInstance2').should('have.css', 'background-color', 'rgb(169, 204, 227)');
  });

  it('selected configfiles should be colored blue', () => {
    cy.contains('workflowInstance1').click();
    cy.contains('conf1').click();
    // color in hex: #a9cce3
    cy.contains('conf1').should('have.css', 'background-color', 'rgb(169, 204, 227)');
    cy.contains('conf2').click();
    // color in hex: #a9cce3
    cy.contains('conf2').should('have.css', 'background-color', 'rgb(169, 204, 227)');

    cy.contains('workflowInstance2').click();
    cy.contains('conf1').click();
    // color in hex: #a9cce3
    cy.contains('conf1').should('have.css', 'background-color', 'rgb(169, 204, 227)');
    cy.contains('conf2').click();
    // color in hex: #a9cce3
    cy.contains('conf2').should('have.css', 'background-color', 'rgb(169, 204, 227)');
    cy.contains('conf3').click();
    // color in hex: #a9cce3
    cy.contains('conf3').should('have.css', 'background-color', 'rgb(169, 204, 227)');
  });

  it('previously selected configfiles should be colored green', () => {
    cy.contains('workflowInstance1').click();
    cy.contains('conf1').click();
    cy.contains('conf2').click();
    cy.wait(2000);
    // color in hex: #a3e4d7
    cy.contains('conf1').should('have.css', 'background-color', 'rgb(163, 228, 215)');
    cy.contains('conf1').click();
    // color in hex: #a3e4d7
    cy.contains('conf2').should('have.css', 'background-color', 'rgb(163, 228, 215)');

    cy.contains('workflowInstance2').click();
    cy.contains('conf1').click();
    cy.contains('conf2').click();
    cy.contains('conf3').click();
    // color in hex: #a3e4d7
    cy.contains('conf1').should('have.css', 'background-color', 'rgb(163, 228, 215)');
    cy.contains('conf2').should('have.css', 'background-color', 'rgb(163, 228, 215)');
    cy.contains('conf1').click();
    // color in hex: #a3e4d7
    cy.contains('conf3').should('have.css', 'background-color', 'rgb(163, 228, 215)');
  });

  it('After the click on "Revert all files" the color of all config-files should be white, excepct for the one selected that should be blue', () => {
    cy.contains('workflowInstance1').click();
    cy.contains('conf1').click();
    cy.contains('conf2').click();
    cy.contains('Revert all files').click();
    // color in hex: #a9cce3
    cy.contains('conf2').should('have.css', 'background-color', 'rgb(169, 204, 227)');
    cy.contains('conf1').should('have.css', 'background-color', 'rgb(255, 255, 255)');

    cy.contains('workflowInstance2').click();
    cy.contains('conf1').click();
    cy.contains('conf2').click();
    cy.contains('conf3').click();
    cy.contains('Revert all files').click();
    cy.contains('conf1').should('have.css', 'background-color', 'rgb(255, 255, 255)');
    cy.contains('conf2').should('have.css', 'background-color', 'rgb(255, 255, 255)');
    // color in hex: #a9cce3
    cy.contains('conf3').should('have.css', 'background-color', 'rgb(169, 204, 227)');
  });

  it('keys and values preserve their entries when it is switched between the config files of a workflow instances', () => {
    cy.then(() => {
      backendServerCommunicatorObject.configFile = workflow1Conf1;
    });
    cy.get('.workflowInstanceName').children().eq(0).click();
    cy.get('.configFileName').children().eq(0).click();
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key1');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val1');
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).click().clear()
      .type('key30');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).click().clear()
      .type('val30');
    cy.then(() => {
      backendServerCommunicatorObject.configFile = (workflow1Conf2);
    });
    cy.get('.configFileName').eq(1).click();
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key1');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val1');
    cy.then(() => {
      backendServerCommunicatorObject.configFile = workflow1Conf1;
    });
    cy.get('.configFileName').eq(0).click();
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key30');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val30');
  });

  it("keys and values entries that have been changed should get their old value, after pressing 'resetAllFiles'", () => {
    cy.then(() => {
      backendServerCommunicatorObject.configFile = workflow1Conf1;
    });
    cy.get('.workflowInstanceName').children().eq(0).click();
    cy.get('.configFileName').children().eq(0).click();
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key1');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val1');
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).click().clear()
      .type('key30');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).click().clear()
      .type('val30');
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key30');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val30');
    cy.get('[data-cy=revertAllFiles]').first().click();
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key1');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val1');
  });

  it('keys and values preserve their entries when it is switched between the config files of a workflow instances', () => {
    cy.then(() => {
      backendServerCommunicatorObject.configFile = workflow1Conf1;
    });
    cy.get('.workflowInstanceName').children().eq(0).click();
    cy.get('.configFileName').children().eq(0).click();
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key1');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val1');
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).click().clear()
      .type('key30');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).click().clear()
      .type('val30');
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key30');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val30');
    cy.then(() => {
      backendServerCommunicatorObject.configFile = workflow1Conf2;
    });
    cy.get('.configFileName').eq(1).click();
    cy.then(() => {
      backendServerCommunicatorObject.configFile = workflow1Conf1;
    });
    cy.get('.configFileName').eq(0).click();
    cy.get('[data-cy=keyEntry] .v-field__input').eq(0).should('have.value', 'key30');
    cy.get('[data-cy=valueEntry] .v-field__input').eq(0).should('have.value', 'val30');
  });
});
