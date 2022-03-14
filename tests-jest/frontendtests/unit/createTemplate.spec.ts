import { shallowMount } from '@vue/test-utils';
import Template from '@Classes/Template';
import CreateTemplate from '@View/CreateTemplate.vue';

describe('CreateTemplate.vue', () => {
  // (method) createTemplateObject(templateBlueprintFile: File, templateName: string): Template
  it('createTemplateObject', () => {
    const wrapper = shallowMount(CreateTemplate, {});

    const file = new File([], 'emptyFile', { type: 'application/zip' });
    const templateName = 'temp1';

    // Tests if the template is created of the file and templateName
    // @ts-ignore
    expect(wrapper.vm.createNewTemplateObject(file, templateName))
      .toEqual(new Template(file, templateName));
  });
});
