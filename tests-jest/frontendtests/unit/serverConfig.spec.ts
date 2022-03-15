import { shallowMount } from '@vue/test-utils';
import Server from '@Classes/Server';
import ServerConfig from '@View/ServerConfig.vue';

describe('ServerConfig.vue', () => {
  // (method) findServerByServerName(servers: Server[], serverName: string): Server
  it('findServerByServerName', () => {
    const wrapper = shallowMount(ServerConfig, {});

    const server1Name = 'server1';
    const server2Name = 'sever2';
    const server1 = new Server('', '', 0, true, server1Name, []);
    const server2 = new Server('', '', 0, true, server2Name, []);
    const serverArray = new Array<Server>(server1);

    expect(wrapper.vm.findServerByServerName(serverArray, server1Name)).toBe(server1);
    expect(() => { wrapper.vm.findServerByServerName(serverArray, server2Name); }).toThrow();
  });
});
