/// <reference types="cypress" />

// @ts-ignore
/* eslint-disable */

import { mountCallback } from '@cypress/vue';
import vuetify from '@/plugins/vuetify';
import CreateWorkflowInstanceCaretaker from '@Memento/CreateWorkflowInstanceCaretaker';
import CreateWorkflowInstanceView from '@View/CreateWorkflowInstance.vue';
import CreateWorkflowInstanceModel from '@Model/CreateWorkflowInstance';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

BackendServerCommunicatorSimulation.prototype
  . pullTemplatesName = async () => this.templateNames;

const backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
backendServerCommunicatorObject.templateNames = (['Template1', 'Template2', 'Template3']);

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

  it("Name the workflowInstance 'workflowInstance1', select 'Template2' as template-blueprint and send it", () => {
    cy.get('#nameOfTheWorkflowInstance').should('have.value', '');
    cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
    cy.get('[data-cy=nameOfTheWorkflowInstance]').click().type('workflowInstance1');
    cy.get('[data-cy=selectTemplateNameFromDropdown]').click();
    cy.get('[data-cy=selectTemplateNameFromDropdown]').parents().contains('Template2').click();
    cy.get('#selectTemplateNameFromDropdown').should('have.value', 'Template2');
    cy.get('#nameOfTheWorkflowInstance').should('have.value', 'workflowInstance1');
    cy.get('[data-cy=sendWorkflowInstance]').click();
    cy.get('#nameOfTheWorkflowInstance').should('have.value', '');
    cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
  });
});
