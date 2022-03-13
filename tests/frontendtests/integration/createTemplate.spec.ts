/// <reference types="cypress" />

import { mountCallback } from '@cypress/vue';
import CreateTemplateView from '@View/CreateTemplate.vue';
import CreateTemplateModel from '@Model/CreateTemplate';
import CreateTemplateCaretaker from '@Memento/CreateTemplateCaretaker';
import vuetify from '@/plugins/vuetify';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

BackendServerCommunicatorSimulation.prototype
  . pullTemplatesName = async () => this.templateNames;

const backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
backendServerCommunicatorObject.templateNames = ['Template1', 'Template2', 'Template3'];

describe('CreateTemplate', () => {
  beforeEach(
    mountCallback(CreateTemplateView, {
      data() {
        return {
          backendServerCommunicatorObject,
          chooseConfigFileObject: new CreateTemplateModel(),
          createTemplateCaretakerObject: new CreateTemplateCaretaker(),
        };
      },
      extensions: {
        use: vuetify,
      },
    }),
  );

  it('Type the name of the template to template1', () => {
    cy.get('#nameOfTheTempalte').should('have.value', '');
    cy.get('[data-cy=nameOfTheTemplate]').click().type('template1');
    cy.get('#nameOfTheTempalte').should('have.value', 'template1');
  });

  it('Select Template2 as template-blueprint', () => {
    cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
    cy.get('[data-cy=selectTemplateNameFromDropdown]').click();
    cy.get('[data-cy=selectTemplateNameFromDropdown]').parents().contains('Template2').click();
    cy.get('#selectTemplateNameFromDropdown').should('have.value', 'Template2');
  });

  it('Select to create template from empty file', () => {
    cy.get('[data-cy=createFromEmptyFile]').should('not.be.checked');
    cy.get('[data-cy=createFromEmptyFile]').click();
    cy.get('[data-cy=createFromEmptyFile]').should('be.checked');
  });

  it('Name the template template1, select Template2 as template-blueprint, check to create from empty file and send it', () => {
    cy.get('#nameOfTheTempalte').should('have.value', '');
    cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
    cy.get('[data-cy=createFromEmptyFile]').should('not.be.checked');
    cy.get('[data-cy=nameOfTheTemplate]').click().type('template1');
    cy.get('[data-cy=selectTemplateNameFromDropdown]').click();
    cy.get('[data-cy=selectTemplateNameFromDropdown]').parents().contains('Template2').click();
    cy.get('[data-cy=createFromEmptyFile]').click();
    cy.get('#nameOfTheTempalte').should('have.value', 'template1');
    cy.get('#selectTemplateNameFromDropdown').should('have.value', 'Template2');
    cy.get('[data-cy=createFromEmptyFile]').should('be.checked');
    cy.get('[data-cy=sendTemplate]').click();
    cy.get('#nameOfTheTempalte').should('have.value', '');
    cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
    cy.get('[data-cy=createFromEmptyFile]').should('not.be.checked');
  });
});
