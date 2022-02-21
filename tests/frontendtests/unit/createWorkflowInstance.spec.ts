import { shallowMount } from '@vue/test-utils'
import WorkflowInstance from '@Classes/WorkflowInstance'
import CreateWorkflowInstance from '@View/CreateWorkflowInstance.vue'

import Vue from 'vue'
Vue.config.silent = true;

describe('CreateWorkflowInstance.vue', () => {
    // (method) createWorkflowInstanceObject(workflowInstanceFolder: File, workflowInstanceName: string): WorkflowInstance
    it('createWorkflowInstanceObject', () => {
        const wrapper = shallowMount(CreateWorkflowInstance, {})

        const file = new File([], "emptyFile", { type: 'application/zip' })
        const workflowInstanceName = 'workflowInstance'

        expect(wrapper.vm.createWorkflowInstanceObject(file, workflowInstanceName)).toEqual(new WorkflowInstance(file, workflowInstanceName))
    })
})