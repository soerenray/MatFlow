/// <reference types="cypress" />

import { mount } from '@cypress/vue';
import vuetify from '@/plugins/vuetify';
import SignUpView from '@View/SignUp.vue';
import SignUpModel from '@Model/SignUp';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

BackendServerCommunicatorSimulation.prototype.pullTemplatesName = async () => this.templateNames;

const backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();

describe('SignUpView', () => {
  beforeEach(() => {
    const signUpObject = new SignUpModel();
    const createTemplateCaretakerObject = signUpObject.createSignUpMemento();
    mount(SignUpView, {
      data() {
        return {
          backendServerCommunicatorObject,
          signUpObject,
          signUpMementoObject: createTemplateCaretakerObject,
        };
      },
      extensions: {
        use: vuetify,
      },
    });
  });

  it('Both eye-symbols should be closed at the begining', () => {
    cy.get('[data-cy=userPassword] .mdi-eye-off');
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye-off');
  });

  it('Both eye-symbols should be open after clicked on', () => {
    cy.get('[data-cy=userPassword] .mdi-eye-off').click();
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye-off').click();
    cy.get('[data-cy=userPassword] .mdi-eye');
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye');
  });

  it('Both eye-symbols should be closed after clicked twice', () => {
    cy.get('[data-cy=userPassword] .mdi-eye-off').click();
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye-off').click();
    cy.get('[data-cy=userPassword] .mdi-eye').click();
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye').click();
    cy.get('[data-cy=userPassword] .mdi-eye-off');
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye-off');
  });

  it("Both eye-symbols should be closed after the 'signup' button is clicked", () => {
    cy.get('[data-cy=signUp]').click();
    cy.get('[data-cy=userPassword] .mdi-eye-off');
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye-off');
  });

  it("Both eye-symbols should be closed after clicked once and the 'signup' button is clicked", () => {
    cy.get('[data-cy=userPassword] .mdi-eye-off').click();
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye-off').click();
    cy.get('[data-cy=signUp]').click();
    cy.get('[data-cy=userPassword] .mdi-eye-off');
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye-off');
  });

  it('As default text of the repeated password field is not visible', () => {
    cy.get('[data-cy=userPasswordRepeated] .v-field__input').should('have.prop', 'type').should('to.eq', 'password');
  });

  it('After the eye-icon of the repeated password field is clicked the password becomes visible', () => {
    cy.get('[data-cy=userPasswordRepeated] .mdi-eye-off').click();
    cy.get('[data-cy=userPasswordRepeated] .v-field__input').should('have.prop', 'type').should('to.eq', 'text');
  });

  it('As default text of the password field is not visible', () => {
    cy.get('[data-cy=userPassword] .v-field__input').should('have.prop', 'type').should('to.eq', 'password');
  });

  it('After the eye-icon of the password field is clicked the password becomes visible', () => {
    cy.get('[data-cy=userPassword] .mdi-eye-off').click();
    cy.get('[data-cy=userPassword] .v-field__input').should('have.prop', 'type').should('to.eq', 'text');
  });

  it('The fields for email-address, the password and the repeated password should contain their typed input', () => {
    cy.get('[data-cy=emailAddress] .v-field__input').should('have.value', '');
    cy.get('[data-cy=userPassword] .v-field__input').should('have.value', '');
    cy.get('[data-cy=userPasswordRepeated] .v-field__input').should('have.value', '');
    cy.get('[data-cy=emailAddress] .v-field__input').click().type('email123');
    cy.get('[data-cy=userPassword] .v-field__input').click().type('password123');
    cy.get('[data-cy=userPasswordRepeated] .v-field__input').click().type('password456');
    cy.get('[data-cy=emailAddress] .v-field__input').should('have.value', 'email123');
    cy.get('[data-cy=userPassword] .v-field__input').should('have.value', 'password123');
    cy.get('[data-cy=userPasswordRepeated] .v-field__input').should('have.value', 'password456');
  });

  it("The fields for email-address, the password and the repeated password should have empty input after being typed on and the 'singup' button is pressed", () => {
    cy.get('[data-cy=emailAddress] .v-field__input').click().type('email123');
    cy.get('[data-cy=userPassword] .v-field__input').click().type('password123');
    cy.get('[data-cy=userPasswordRepeated] .v-field__input').click().type('password456');
    cy.get('[data-cy=signUp]').click();
    cy.get('[data-cy=emailAddress] .v-field__input').should('have.value', '');
    cy.get('[data-cy=userPassword] .v-field__input').should('have.value', '');
    cy.get('[data-cy=userPasswordRepeated] .v-field__input').should('have.value', '');
  });
});
