/// <reference types="cypress" />

// @ts-nocheck
/* eslint-disable */

import { mountCallback } from '@cypress/vue';
import vuetify from '@/plugins/vuetify';
import ServerConfigView from '@View/ServerConfig.vue';
import ServerConfigModel from '@Model/ServerConfig';
import Server from '@Classes/Server';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

const server1 = new Server(
  '123.123.11.1',
  'running',
  5,
  true,
  'kit-materialwissenschaften',
  [['cpu1', '50%']],
);

BackendServerCommunicatorSimulation.prototype.pullServers = async function () {
  return new Promise((res) => setTimeout(res(this.servers), 500))
}

let backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
backendServerCommunicatorObject.servers = [server1];

describe('ServerConfig', () => {
  beforeEach(
    mountCallback(ServerConfigView, {
      data() {
        return {
          backendServerCommunicatorObject: backendServerCommunicatorObject,
          serverConfigObject: new ServerConfigModel(
            [
              { text: 'Server location name', value: 'serverName' },
              { text: 'Address', value: 'serverAddress' },
              { text: 'Status', value: 'serverStatus' },
              { text: 'Container limit', value: 'containerLimit' },
              {
                text: 'Select server for execution',
                value: 'selectedForExecution',
              },
              { text: 'Configurate server resources', value: 'serverResources' },
              { text: 'apply changes', value: 'apply' },
            ],
            [],
            false,
          ),
        };
      },
      extensions: {
        use: vuetify,
      },
    }),
  );

  afterEach(() => {
    backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
    backendServerCommunicatorObject.servers = [server1];
  })

  it('Table headers are displayed correctly and in the correct order', () => {
    cy.get('[data-cy=tableHeader]')
    cy.get('[data-cy=tableHeader] > tr > th').eq(0).should('have.text', 'Server location name');
    cy.get('[data-cy=tableHeader] > tr > th').eq(1).should('have.text', 'Address');
    cy.get('[data-cy=tableHeader] > tr > th').eq(2).should('have.text', 'Status');
    cy.get('[data-cy=tableHeader] > tr > th').eq(3).should('have.text', 'Container limit');
    cy.get('[data-cy=tableHeader] > tr > th').eq(4).should('have.text', 'Select server for execution');
    cy.get('[data-cy=tableHeader] > tr > th').eq(5).should('have.text', 'Configurate server resources');
    cy.get('[data-cy=tableHeader] > tr > th').eq(6).should('have.text', 'apply changes');
  });

  it('Table-body exists of exactly one element', () => {
    cy.get('[data-cy=tableBody]').should('exist');
  });

  it('Table-body consits of exactly one element', () => {
    cy.get('[data-cy=tableBody] > tr').should('have.length', 1);
  });

  it("'Server location name', 'Address', 'Status', 'Container limit', 'Selected for execution' should contain the correct values", () => {
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(0).should('have.value', 'kit-materialwissenschaften');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(1).should('have.value', '123.123.11.1');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(2).should('have.value', 'running');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).should('have.value', '5');
  });

  it("'Server location name', 'Address', 'Status', 'Container limit', 'Selected for execution' should contain the correct values after 'apply changes' is pressed", () => {
    cy.get('[data-cy=applyChanges]').eq(0).click();
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(0).should('have.value', 'kit-materialwissenschaften');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(1).should('have.value', '123.123.11.1');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(2).should('have.value', 'running');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).should('have.value', '5');
  });

  it("Changes made to 'Server location name', 'Address', 'Status', 'Container limit' should be applied", () => {
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(0).invoke('val', 'kit-informatik');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(1).invoke('val', '123,456.78');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(2).invoke('val', 'waiting')
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).invoke('val', '10')
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(0).should('have.value', 'kit-informatik');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(1).should('have.value', '123,456.78');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(2).should('have.value', 'waiting');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).should('have.value', '10');
  });

  it("Container limit should be 5. Then after typing 10 it should contain the value 10", () => {
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).invoke('val', '5')
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).should('have.value', '5');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).click().clear().type('10')
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).should('have.value', '10');
  });

  it("Changes made to 'Server location name', 'Address', 'Status', 'Container limit' should not change after 'apply changes' is pressed", () => {
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(0).invoke('val', 'kit-informatik');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(1).invoke('val', '123,456.78');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(2).invoke('val', 'waiting')
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).invoke('val', '10')
    // bit hackie
    cy.then(() => {
      backendServerCommunicatorObject.servers = [
        new Server(
          '123,456.78',
          'waiting',
          10,
          true,
          'kit-informatik',
          [['cpu1', '50%']],
        ),
      ];
    });
    cy.get('[data-cy=applyChanges]').eq(0).click();
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(0).should('have.value', 'kit-informatik');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(1).should('have.value', '123,456.78');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(2).should('have.value', 'waiting');
    cy.get('[data-cy=tableBody] > tr .v-field__input').eq(3).should('have.value', '10');
  });

  it("Server resources of 'server1' should contain the correct entries in the correct order", () => {
    cy.get('[data-cy=serverResources]').eq(0).click();
    cy.get('[data-cy=keyValuePairs] .v-field__input').eq(0).should('have.value', 'cpu1');
    cy.get('[data-cy=keyValuePairs] .v-field__input').eq(1).should('have.value', '50%');
  });

  it("The changes should be applied, after typing new key-value-pairs in 'server resoureces'", () => {
    cy.get('[data-cy=serverResources]').eq(0).click();
    cy.get('[data-cy=keyValuePairs] .v-field__input').eq(0).click().clear()
      .type('cpu2');
    cy.get('[data-cy=keyValuePairs] .v-field__input').eq(1).click().clear()
      .type('100%');
    cy.get('[data-cy=keyValuePairs] .v-field__input').eq(0).should('have.value', 'cpu2');
    cy.get('[data-cy=keyValuePairs] .v-field__input').eq(1).should('have.value', '100%');
  });
});
