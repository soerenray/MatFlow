import { shallowMount } from '@vue/test-utils'
import ConfigFile from '../../src/Classes/ConfigFile'
import ChooseConfigFileView from '../../src/View/ChooseConfigFile.vue'
// import ChooseConfigFileModel from '../../src/Model/ChooseConfigFile'
// import BackendServerCommunicator from "../../src/Controler/BackendServerCommunicator";

describe('ChooseConfigFile.vue', () => {
  // (method) colorForConfigFileName: (updatedConfigFiles: ConfigFile[], selectedConfigFileName: string, configFileName: string) => string
  it('colorForConfigFileName', () => {

    const wrapper = shallowMount(ChooseConfigFileView, {})
    const color1 = "#a9cce3"
    const color2 = "#a3e4d7"
    const color3 = "#FFFFFF"

    const configFileName1 = "conf1"
    const configFileName2 = "conf2"

    const updatedConfigFiles = [new ConfigFile(configFileName2, [])]

    // selectedConfigFileName equals configFileName
    expect(wrapper.vm.colorForConfigFileName([], configFileName1, configFileName1)).toBe(color1)

    // configFileName is in updateConfigFiles
    expect(wrapper.vm.colorForConfigFileName(updatedConfigFiles, configFileName1, configFileName2)).toBe(color2)

    // configFileName is neither equal to selectedConfigFileName nor in updatedConfigFiles
    expect(wrapper.vm.colorForConfigFileName([], configFileName1, configFileName2)).toBe(color3)
  })
})

describe('ChooseConfigFile.vue', () => {
  // (method) isConfigFileNameInUpdatedConfigFiles(updatedConfigFiles: ConfigFile[], configFileName: string): boolean
  it('isConfigFileNameInUpdatedConfigFiles', () => {
    const wrapper = shallowMount(ChooseConfigFileView, {})

    const configFileName1 = "conf1"
    const configFileName2 = "conf2"

    const updatedConfigFiles = [new ConfigFile(configFileName2, [])]

    // updatedConfigFiles is empty
    expect(wrapper.vm.isConfigFileNameInUpdatedConfigFiles([], configFileName1)).toBe(false)

    // updatedConfigFiles does not contain configFileName
    expect(wrapper.vm.isConfigFileNameInUpdatedConfigFiles(updatedConfigFiles, configFileName1)).toBe(false)

    // updatedConfigFiles does contain configFileName
    expect(wrapper.vm.isConfigFileNameInUpdatedConfigFiles(updatedConfigFiles, configFileName2)).toBe(true)
  })
})

describe('ChooseConfigFile.vue', () => {
  // (method) changeAllKeyValuePairs(configFileName: string, newKeyValuePairs: Array<[string, string]>): void
  it('changeAllKeyValuePairs', () => {
    const wrapper = shallowMount(ChooseConfigFileView, {})

    const conf1Name = 'conf1'

    const keyValuePair1 = [['a', 'b'], ['c', 'd']]
    const keyValuePair2 = [['1', '2'], ['c', 'd']]

    const conf1 = new ConfigFile(conf1Name, keyValuePair1)

    wrapper.vm.updatedConfigFiles.push(conf1)
    wrapper.vm.changeAllKeyValuePairs(conf1Name, keyValuePair2)
    expect(keyValuePair1).toEqual(keyValuePair2)
  })
})

describe('ChooseConfigFile.vue', () => {
  // (method) updateKeyValuePairs(oldKetValuePairs: Array<[string, string]>, newKeyValuePairs: Array<[string, string]>): void
  it('updateKeyValuePairs', () => {
    const wrapper = shallowMount(ChooseConfigFileView, {})

    const keyValuePair1 = [['a', 'b'], ['c', 'd']]
    const keyValuePair2 = [['1', '2'], ['c', 'd']]

    // Expects the key-value pairs to be changed in keyValuePair1
    wrapper.vm.updateKeyValuePairs(keyValuePair1, keyValuePair2)
    expect(keyValuePair1).toEqual(keyValuePair2)
  })
})

describe('ChooseConfigFile.vue', () => {
  // (method) getConfigFileFromUpdatedConfigFiles(updatedConfigFiles: ConfigFile[], configFileName: string): ConfigFile
  it('getConfigFileFromUpdatedConfigFiles', () => {
    const wrapper = shallowMount(ChooseConfigFileView, {})

    const conf1Name = 'conf1'
    const conf2Name = 'conf2'

    const conf1File = new ConfigFile(conf1Name, [])

    const updatedConfigFiles = [conf1File]

    // Checks if the name conf1Name is in a configFile of updatedConfigFiles and returns the file
    expect(wrapper.vm.getConfigFileFromUpdatedConfigFiles(updatedConfigFiles, conf1Name)).toBe(conf1File)

    // Checks if the name conf2Name is in a configFile of updatedConfigFiles and throws an error
    expect(() => { wrapper.vm.getConfigFileFromUpdatedConfigFiles(updatedConfigFiles, conf2Name) }).toThrow()

    // Checks if the name conf2Name is in a configFile of updatedConfigFiles and throws an error with message "'There is no configFile with name ' + conf2Name"
    expect(() => { wrapper.vm.getConfigFileFromUpdatedConfigFiles(updatedConfigFiles, conf2Name) }).toThrow('There is no configFile with name ' + conf2Name)
  })
})

describe('ChooseConfigFile.vue', () => {
  // (method) setSelectedWorkflowInstanceNameAndResetConfigFileNameAndUpdatedConfigFiles(selectedWorkflowInstanceName: string): void
  it('setSelectedWorkflowInstanceNameAndResetConfigFileNameAndUpdatedConfigFiles', () => {
    const wrapper = shallowMount(ChooseConfigFileView, {})

    const selectedWorkflowInstanceName = 'workflowInstance1'

    wrapper.vm.setSelectedWorkflowInstanceNameAndResetConfigFileNameAndUpdatedConfigFiles(selectedWorkflowInstanceName)

    // These are the changes that are made in the method
    expect(wrapper.vm.selectedWorkflowInstanceName).toBe(selectedWorkflowInstanceName)
    expect(wrapper.vm.selectedConfigFileName).toBe("")
    expect(wrapper.vm.updatedConfigFiles).toEqual([])
    expect(wrapper.vm.chosenConfigFile).toEqual(new ConfigFile())
  })
})
