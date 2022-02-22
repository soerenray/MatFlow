import { shallowMount } from "@vue/test-utils"
import EditKeyValuePairsModel from "@Model/EditKeyValuePairs"
import EditKeyValuePairsView from "@View/EditKeyValuePairs.vue"

import Vue from 'vue'
Vue.config.silent = true;

describe('EditKeyValuePairs.vue', () => {
    // (method) getKeyValuePairsAsTupleArray(keyValuePairs: Array<KeyValuePair>): Array<[string, string]>
    it('getKeyValuePairsAsTupleArray', () => {
        const wrapper = shallowMount(EditKeyValuePairsView, {
            propsData: {
                keyValuePairsFromParent: []
            }
        })

        const array1: [string, string] = ['a', 'b']
        const array2: [string, string] = ['1', '2']
        const keyValuePairsAsTupleArray = new Array<[string, string]>(array1, array2)
        const editKeyValuePairsObject = new EditKeyValuePairsModel()

        editKeyValuePairsObject.addKeyValuePair(array1)
        editKeyValuePairsObject.addKeyValuePair(array2)

        expect(wrapper.vm.getKeyValuePairsAsTupleArray(editKeyValuePairsObject.keyValuePairs)).toEqual(keyValuePairsAsTupleArray)
    })
})