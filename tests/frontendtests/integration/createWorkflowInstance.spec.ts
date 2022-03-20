/// <reference types="cypress" />

// @ts-nocheck
/* eslint-disable */

import { mountCallback } from '@cypress/vue';
import vuetify from '@/plugins/vuetify';
import CreateWorkflowInstanceCaretaker from '@Memento/CreateWorkflowInstanceCaretaker';
import CreateWorkflowInstanceView from '@View/CreateWorkflowInstance.vue';
import CreateWorkflowInstanceModel from '@Model/CreateWorkflowInstance';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

BackendServerCommunicatorSimulation.prototype
  .pullTemplatesName = async function () {
    return new Promise((res) => setTimeout(res(this.templateNames), 500))
  }

const templatesName = ['Template1', 'Template2', 'Template3']
let backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
backendServerCommunicatorObject.templateNames = templatesName

describe('CreateWorkflowInstance', () => {
  beforeEach(
    mountCallback(CreateWorkflowInstanceView, {
      data() {
        return {
          backendServerCommunicatorObject,
          chooseConfigFileObject: new CreateWorkflowInstanceModel(
            ['import worfklow', 'create workflow-instance from template'],
            'create workflow-instance from template',
          ),
          createTemplateCaretakerObject: new CreateWorkflowInstanceCaretaker(),
        };
      },
      extensions: {
        use: vuetify,
      },
    }),
  );

  afterEach(() => {
    backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
    backendServerCommunicatorObject.templateNames = templatesName
  })

  it('Type the name of the workflowInstance to workflowInstance1', () => {
    cy.get('#nameOfTheWorkflowInstance').should('have.value', '');
    cy.get('[data-cy=nameOfTheWorkflowInstance]').click().type('workflowInstance1');
    cy.get('#nameOfTheWorkflowInstance').should('have.value', 'workflowInstance1');
  });

  it('Select Template2 as template-blueprint', () => {
    cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
    cy.get('[data-cy=selectTemplateNameFromDropdown]').click();
    cy.get('[data-cy=selectTemplateNameFromDropdown]').parents().contains('Template2').click();
    cy.get('#selectTemplateNameFromDropdown').should('have.value', 'Template2');
  });

  // // simulates choosing a config file, since this cannot be testet with cypress
  // it("Name the workflowInstance 'workflowInstance1', select 'Template2' as template-blueprint, select a config file and send it", () => {
  //   cy.get('#nameOfTheWorkflowInstance').should('have.value', '');
  //   cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
  //   cy.get('[data-cy=nameOfTheWorkflowInstance]').click().type('workflowInstance1');
  //   cy.get('[data-cy=selectTemplateNameFromDropdown]').click();
  //   cy.get('[data-cy=selectTemplateNameFromDropdown]').parents().contains('Template2').click();
  //   cy.get('#selectTemplateNameFromDropdown').should('have.value', 'Template2');
  //   cy.get('#nameOfTheWorkflowInstance').should('have.value', 'workflowInstance1');
  //   cy.get('[data-cy=sendWorkflowInstance]').click();
  //   cy.get('#nameOfTheWorkflowInstance').should('have.value', '');
  //   cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
  // });
});
