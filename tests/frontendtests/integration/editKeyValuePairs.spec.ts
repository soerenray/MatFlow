/// <reference types="cypress" />

import { mountCallback } from '@cypress/vue'
import vuetify from '@/plugins/vuetify'
import EditKeyValuePairsView from '@View/EditKeyValuePairs.vue'
import EditKeyValuePairsModel from "@Model/EditKeyValuePairs";

describe('EditKeyValuePairs', () => {
    beforeEach(
        mountCallback(EditKeyValuePairsView, {
            data: function () {
                return {
                    editKeyValuePairsObject: new EditKeyValuePairsModel()
                }
            },
            props: {
                keyValuePairsFromParent: [['key1', 'val1'], ['key2', 'val2']]
            },
            extensions: {
                use: vuetify
            }
        })
    )

    it("The key-value pairs contain the correct entries", () => {
        cy.get("[data-cy=keyEntry] .v-field__input").eq(0).should('have.value', 'key1')
        cy.get("[data-cy=valueEntry] .v-field__input").eq(0).should('have.value', 'val1')
        cy.get("[data-cy=keyEntry] .v-field__input").eq(1).should('have.value', 'key2')
        cy.get("[data-cy=valueEntry] .v-field__input").eq(1).should('have.value', 'val2')
    })

    it("The entry of key1 is changed to key2, which should failed (duplicated key)", () => {
        cy.get("[data-cy=keyEntry] .v-field__input").eq(0).click().clear().type('key2')
        cy.get("[data-cy=keyEntry] .v-field__input").eq(0).should('not.have.value', 'key2')
        // it should have entry 'key', since that is the last entry that was valid
        cy.get("[data-cy=keyEntry] .v-field__input").eq(0).should('have.value', 'key')
    })

    it("The entry of key1 is changed to key3", () => {
        cy.get("[data-cy=keyEntry] .v-field__input").eq(0).click().clear().type('key3')
        cy.get("[data-cy=keyEntry] .v-field__input").eq(0)
    })

    it("The entry of val1 is changed to val2", () => {
        cy.get("[data-cy=valueEntry] .v-field__input").eq(0).click().clear().type('val2')
        cy.get("[data-cy=valueEntry] .v-field__input").eq(0).should('have.value', 'val2')
    })

    // It depends on a call to the parent class. No idea how to test/smiulate it
    // But it is tested in chooseConfigFile, where editKeyValuePairs is implemented
    // it("The entry of key1 and val1 should be changed, then 'revert all files' is pressed and they should have entries key1, val1 again", () => {
    //     cy.get("[data-cy=keyEntry] .v-field__input").eq(0).should('have.value', 'key1')
    //     cy.get("[data-cy=valueEntry] .v-field__input").eq(0).should('have.value', 'val1')
    //     cy.get("[data-cy=keyEntry] .v-field__input").eq(0).click().clear().type('key')
    //     cy.get("[data-cy=valueEntry] .v-field__input").eq(0).click().clear().type('val')
    //     cy.get("[data-cy=keyEntry] .v-field__input").eq(0).should('have.value', 'key')
    //     cy.get("[data-cy=valueEntry] .v-field__input").eq(0).should('have.value', 'val')
        // cy.get("[data-cy=revertAllFiles]").click()
        // cy.get("[data-cy=keyEntry] .v-field__input").eq(0).should('have.value', 'key1')
        // cy.get("[data-cy=valueEntry] .v-field__input").eq(0).should('have.value', 'val1')
    // })
})