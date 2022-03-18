/// <reference types="cypress" />

// @ts-nocheck
/* eslint-disable */

import { mountCallback } from '@cypress/vue';
import CreateTemplateView from '@View/CreateTemplate.vue';
import CreateTemplateModel from '@Model/CreateTemplate';
import CreateTemplateCaretaker from '@Memento/CreateTemplateCaretaker';
import vuetify from '@/plugins/vuetify';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

BackendServerCommunicatorSimulation.prototype
  . pullTemplatesName = async function() {
    return new Promise((res) => setTimeout(res(this.templatesName), 500))
  }

const templatesName = ['Template1', 'Template2', 'Template3']
let backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
backendServerCommunicatorObject.templatesName = templatesName;

describe('CreateTemplate', () => {
  beforeEach(
    mountCallback(CreateTemplateView, {
      data() {
        return {
          backendServerCommunicatorObject: backendServerCommunicatorObject,
          createTemplateObject: new CreateTemplateModel(),
          createTemplateCaretakerObject: new CreateTemplateCaretaker(),
        };
      },
      extensions: {
        use: vuetify,
      },
    }),
  );

  afterEach(() => {
    backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();
    backendServerCommunicatorObject.templatesName = ['Template1', 'Template2', 'Template3'];
  })

  it("Type the name 'template1', open the text editor, press the 'save'-button, then the 'close'-button and after that press the 'send'-button", () => {
    cy.get('[data-cy=nameOfTheTemplate]').click().type('template1');
    cy.get('#nameOfTheTempalte').should('have.value', 'template1');
    cy.get('[data-cy=editTemplate]').click()
    cy.get('[data-cy=save]').click()
    cy.get('[data-cy=close]').click()
    cy.get('[data-cy=sendTemplate]').click()
  });

  it("Open the text-editor. The text-editor should only contain the word hello", () => {
    cy.get('[data-cy=editTemplate]').click()
    cy.get('[data-cy=textarea] .v-field__input').should('have.value', '')
  });
  
  it("Open the text-editor type in 'hello'. The text-editor should only contain the word hello", () => {
    cy.get('[data-cy=editTemplate]').click()
    cy.get('[data-cy=textarea').click().type('hello')
    cy.get('[data-cy=textarea] .v-field__input').should('have.value', 'hello')
  });

  it("Open the text-editor type in 'hello' and close it without saving. Then open the text-editor again. There should be no text", () => {
    cy.get('[data-cy=editTemplate]').click()
    cy.get('[data-cy=textarea').click().type('hello')
    cy.get('[data-cy=close]').click()
    cy.get('[data-cy=editTemplate]').click()
    cy.get('[data-cy=textarea] .v-field__input').should('have.value', '')
  });

  it("Open the text-editor type in 'hello' and close it with saving. Open the text-editor again. It should contain 'hello' ", () => {
    cy.get('[data-cy=editTemplate]').click()
    cy.get('[data-cy=textarea').click().type('hello')
    cy.get('[data-cy=save]').click()
    cy.get('[data-cy=close]').click()
    cy.get('[data-cy=editTemplate]').click()
    cy.get('[data-cy=textarea] .v-field__input').should('have.value', 'hello')
  });

  it('Type the name of the template to template1', () => {
    cy.get('[data-cy=nameOfTheTemplate]').click().type('template1');
    cy.get('#nameOfTheTempalte').should('have.value', 'template1');
  });

  it('Select Template2 as template-blueprint', () => {
    cy.get('[data-cy=selectTemplateNameFromDropdown]').click();
    cy.get('[data-cy=selectTemplateNameFromDropdown]').parents().contains('Template2').click();
    cy.get('#selectTemplateNameFromDropdown').should('have.value', 'Template2');
  });

  it('Name the template template1, select Template2 as template-blueprint and send it', () => {
    cy.get('[data-cy=nameOfTheTemplate]').click().type('template1');
    cy.get('[data-cy=selectTemplateNameFromDropdown]').click();
    cy.get('[data-cy=selectTemplateNameFromDropdown]').parents().contains('Template2').click();
    cy.get('#nameOfTheTempalte').should('have.value', 'template1');
    cy.get('#selectTemplateNameFromDropdown').should('have.value', 'Template2');
    cy.get('[data-cy=sendTemplate]').click();
    cy.get('#nameOfTheTempalte').should('have.value', '');
    cy.get('#selectTemplateNameFromDropdown').should('have.value', '');
  });
});
