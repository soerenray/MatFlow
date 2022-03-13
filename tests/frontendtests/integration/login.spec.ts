/// <reference types="cypress" />

// @ts-ignore
/* eslint-disable */

import { mount } from '@cypress/vue';
import vuetify from '@/plugins/vuetify';
import LogInView from '@View/LogIn.vue';
import LogInModel from '@Model/LogIn';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

const backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();

describe('LogIn', () => {
  beforeEach(() => {
    const logInObject = new LogInModel();
    const logInMementoObject = logInObject.createLogInMemento();

    mount(LogInView, {
      data() {
        return {
          backendServerCommunicatorObject,
          logInObject,
          logInMementoObject,
        };
      },
      extensions: {
        use: vuetify,
      },
    });
  });

  it('Email-Address and Password should be empty after the side is loaded', () => {
    cy.get('[data-cy=emailAddress] .v-field__input').should('have.value', '');
    cy.get('[data-cy=userPassword] .v-field__input').should('have.value', '');
  });

  it('After typing the email-address and password, the corresponding fields should contain the typed values', () => {
    cy.get('[data-cy=emailAddress]').click().type('email123');
    cy.get('[data-cy=userPassword]').click().type('password123');
    cy.get('[data-cy=emailAddress] .v-field__input').should('have.value', 'email123');
    cy.get('[data-cy=userPassword] .v-field__input').should('have.value', 'password123');
  });

  it("After typing an email and password and pressing the 'login' the email and password field should be empty", () => {
    cy.get('[data-cy=emailAddress]').click().type('email123');
    cy.get('[data-cy=userPassword]').click().type('password123');
    cy.get('[data-cy=emailAddress] .v-field__input').should('have.value', 'email123');
    cy.get('[data-cy=userPassword] .v-field__input').should('have.value', 'password123');
    cy.get("[data-cy='loginButton']").click();
    cy.get('[data-cy=emailAddress] .v-field__input').should('have.value', '');
    cy.get('[data-cy=userPassword] .v-field__input').should('have.value', '');
  });

  it('The password field should be default not be visible (have password tag)', () => {
    cy.get('[data-cy=userPassword] .v-field__input').should('have.prop', 'type').should('to.eq', 'password');
  });

  it('The eye-icon should be closed by default', () => {
    cy.get('.mdi-eye-off');
  });

  it('The eye-icon should be after after one clicl', () => {
    cy.get('.mdi-eye-off').click();
    cy.get('.mdi-eye');
  });

  it('The password field should be visible (have password tag) after clicking the eye-icon', () => {
    cy.get('.mdi-eye-off').click();
    cy.get('[data-cy=userPassword] .v-field__input').should('have.prop', 'type').should('to.eq', 'text');
  });

  it('The password field should not be visible (have text tag) after clicking the eye-icon twice', () => {
    cy.get('.mdi-eye-off').click();
    cy.get('.mdi-eye').click();
    cy.get('[data-cy=userPassword] .v-field__input').should('have.prop', 'type').should('to.eq', 'password');
  });
});
