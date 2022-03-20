import { createRouter, createWebHistory } from 'vue-router';

import ChooseConfigFile from './View/ChooseConfigFile.vue';
import CreateTemplate from './View/CreateTemplate.vue';
import CreateWorkflowInstance from './View/CreateWorkflowInstance.vue';
import LogIn from './View/LogIn.vue';
import ServerConfig from './View/ServerConfig.vue';
import SignUp from './View/SignUp.vue';
import UserAdministration from './View/UserAdministration.vue';
import VersionControl from './View/VersionControl.vue';

const routes = [
  { path: '/ChooseConfigFile', name: 'ChooseConfigFile', component: ChooseConfigFile },
  { path: '/CreateTemplate', name: 'CreateTemplate', component: CreateTemplate },
  { path: '/CreateWorkflowInstance', name: 'CreateWorkflowInstance', component: CreateWorkflowInstance },
  { path: '/LogIn', name: 'LogIn', component: LogIn },
  { path: '/ServerConfig', name: 'ServerConfig', component: ServerConfig },
  { path: '/SignUp', name: 'SignUp', component: SignUp },
  { path: '/UserAdministration', name: 'UserAdministration', component: UserAdministration },
  { path: '/VersionControl', name: 'VersionControl', component: VersionControl },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
