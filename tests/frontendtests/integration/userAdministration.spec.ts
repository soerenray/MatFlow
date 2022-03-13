/// <reference types="cypress" />

// @ts-nocheck
/* eslint-disable */

import { mountCallback } from '@cypress/vue';
import vuetify from '@/plugins/vuetify';
import UserAdministrationView from '@View/UserAdministration.vue';
import UserAdministrationModel from '@Model/UserAdministration';
import User from '@Classes/User';
import BackendServerCommunicatorSimulation from './helper/BackendServerCommunicatorSimulation';

BackendServerCommunicatorSimulation.prototype.pullUsers = async function() {
  return new Promise((res) => setTimeout(res(this.users), 500))
};

const backendServerCommunicatorObject = new BackendServerCommunicatorSimulation();

const user1 = new User('name1', 'suspended', 'administrator');
const user2 = new User('name2', 'pending', 'visitor');

beforeEach(
  mountCallback(UserAdministrationView, {
    data() {
      return {
        backendServerCommunicatorObject,
        userAdministrationObject: new UserAdministrationModel(
          [
            { text: 'Username', value: 'name' },
            { text: 'User priviliges', value: 'privilege' },
            { text: 'Status', value: 'status' },
            { text: 'Delete', value: 'delete' },
          ],
          [],
          ['activated', 'suspended', 'pending'],
          ['visitor', 'developer', 'administrator'],
        ),
      };
    },
    extensions: {
      use: vuetify,
    },
  }),
);

describe('UserAdministration', () => {
  // users are pulled at the very begining and 'before' runs before 'beforEach'
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it('Should only contain two users after initialisation phase', () => {
    cy.get('[data-cy=userName]').should('have.length', 2);
    cy.get('[data-cy=userPriviliges]').should('have.length', 2);
    cy.get('[data-cy=userStatus]').should('have.length', 2);
    cy.get('[data-cy=delete]').should('have.length', 2);
  });
});

describe('UserAdministration', () => {
  // users are pulled at the very begining and 'before' runs before 'beforEach'
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it('Checks if the users from the database are displayed correctly', () => {
    cy.get('[data-cy=userName] .v-field__input').eq(0).should('have.value', 'name1');
    cy.get('[data-cy=userName] .v-field__input').eq(1).should('have.value', 'name2');
    cy.get('[data-cy=userPriviliges]').eq(0).contains('suspended');
    cy.get('[data-cy=userPriviliges]').eq(1).contains('pending');
    cy.get('[data-cy=userStatus]').eq(0).contains('administrator');
    cy.get('[data-cy=userStatus]').eq(1).contains('visitor');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(0).should('have.text', 'suspended');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(1).should('have.text', 'pending');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(0).should('have.text', 'administrator');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(1).should('have.text', 'visitor');
  });
});

describe('UserAdministration', () => {
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it('Deletes user1 and should only contain user2', () => {
    // a bit hackie, should be solved differently
    cy.then(() => {
      backendServerCommunicatorObject.users = [user2];
    });
    cy.get('[data-cy=delete]').eq(0).click();
    cy.get('[data-cy=userName]').should('have.length', 1);
    cy.get('[data-cy=userPriviliges]').should('have.length', 1);
    cy.get('[data-cy=userStatus]').should('have.length', 1);
    cy.get('[data-cy=delete]').should('have.length', 1);
    cy.get('[data-cy=userName] .v-field__input').eq(0).should('have.value', 'name2');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(0).should('have.text', 'pending');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(0).should('have.text', 'visitor');
  });
});

describe('UserAdministration', () => {
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it('Deletes user2 and should only contain user1', () => {
    // a bit hackie, should be solved differently
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1];
    });
    cy.get('[data-cy=delete]').eq(0).click();
    cy.get('[data-cy=userName]').should('have.length', 1);
    cy.get('[data-cy=userPriviliges]').should('have.length', 1);
    cy.get('[data-cy=userStatus]').should('have.length', 1);
    cy.get('[data-cy=delete]').should('have.length', 1);
    cy.get('[data-cy=userName] .v-field__input').eq(0).should('have.value', 'name1');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(0).should('have.text', 'suspended');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(0).should('have.text', 'administrator');
  });
});

describe('UserAdministration', () => {
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it('changes made to both users should be applied', () => {
    cy.get('[data-cy=userPriviliges]').eq(0).click().get('.v-overlay-container .v-list:visible')
      .contains('activated')
      .click();
    cy.get('[data-cy=userPriviliges]').eq(1).click().get('.v-overlay-container .v-list:visible')
      .contains('suspended')
      .click();
    cy.get('[data-cy=userStatus]').eq(0).click().get('.v-overlay-container .v-list:visible')
      .contains('visitor')
      .click();
    cy.get('[data-cy=userStatus]').eq(1).click().get('.v-overlay-container .v-list:visible')
      .contains('developer')
      .click();
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(0).should('have.text', 'activated');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(1).should('have.text', 'suspended');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(0).should('have.text', 'visitor');
    cy.get('[data-cy=userStatus] .v-select__selection-text ').eq(1).should('have.text', 'developer');
  });
});

describe('UserAdministration', () => {
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it("Default values dont change after 'pull users from server'-button is pressed", () => {
    cy.get('[data-cy=pullUsersFromServer]').click();
    cy.get('[data-cy=userName] .v-field__input').eq(0).should('have.value', 'name1');
    cy.get('[data-cy=userName] .v-field__input').eq(1).should('have.value', 'name2');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(0).should('have.text', 'suspended');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(1).should('have.text', 'pending');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(0).should('have.text', 'administrator');
    cy.get('[data-cy=userStatus] .v-select__selection-text ').eq(1).should('have.text', 'visitor');
  });
});

describe('UserAdministration', () => {
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it("changes made to both users should be applied and the reverted after 'pull users from sever'-button is pressed", () => {
    cy.get('[data-cy=userPriviliges]').eq(0).click().get('.v-overlay-container .v-list:visible')
      .contains('activated')
      .click();
    cy.get('[data-cy=userPriviliges]').eq(1).click().get('.v-overlay-container .v-list:visible')
      .contains('suspended')
      .click();
    cy.get('[data-cy=userStatus]').eq(0).click().get('.v-overlay-container .v-list:visible')
      .contains('visitor')
      .click();
    cy.get('[data-cy=userStatus]').eq(1).click().get('.v-overlay-container .v-list:visible')
      .contains('developer')
      .click();
    cy.get('[data-cy=pullUsersFromServer]').click();
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(0).should('have.text', 'suspended');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(1).should('have.text', 'pending');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(0).should('have.text', 'administrator');
    cy.get('[data-cy=userStatus] .v-select__selection-text ').eq(1).should('have.text', 'visitor');
  });
});

describe('UserAdministration', () => {
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it("Default values dont change after 'update users'-button is pressed", () => {
    cy.get('[data-cy=updateUsers]').click();
    cy.get('[data-cy=userName] .v-field__input').eq(0).should('have.value', 'name1');
    cy.get('[data-cy=userName] .v-field__input').eq(1).should('have.value', 'name2');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(0).should('have.text', 'suspended');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(1).should('have.text', 'pending');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(0).should('have.text', 'administrator');
    cy.get('[data-cy=userStatus] .v-select__selection-text ').eq(1).should('have.text', 'visitor');
  });
});

describe('UserAdministration', () => {
  before(() => {
    cy.then(() => {
      backendServerCommunicatorObject.users = [user1, user2];
    });
  });

  it("changes made to both users should be applied and stay after pressing 'update users'- and then 'pull users from sever'-button", () => {
    cy.get('[data-cy=userPriviliges]').eq(0).click().get('.v-overlay-container .v-list:visible')
      .contains('activated')
      .click();
    cy.get('[data-cy=userPriviliges]').eq(1).click().get('.v-overlay-container .v-list:visible')
      .contains('suspended')
      .click();
    cy.get('[data-cy=userStatus]').eq(0).click().get('.v-overlay-container .v-list:visible')
      .contains('visitor')
      .click();
    cy.get('[data-cy=userStatus]').eq(1).click().get('.v-overlay-container .v-list:visible')
      .contains('developer')
      .click();
    cy.get('[data-cy=updateUsers]').click().then(() => {
      backendServerCommunicatorObject.users = [new User('name1', 'activated', 'visitor'), new User('name2', 'suspended', 'developer')];
    });
    cy.get('[data-cy=pullUsersFromServer]').click();
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(0).should('have.text', 'activated');
    cy.get('[data-cy=userPriviliges] .v-select__selection-text').eq(1).should('have.text', 'suspended');
    cy.get('[data-cy=userStatus] .v-select__selection-text').eq(0).should('have.text', 'visitor');
    cy.get('[data-cy=userStatus] .v-select__selection-text ').eq(1).should('have.text', 'developer');
  });
});
