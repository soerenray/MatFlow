import VueRouter from "vue-router"

import ChooseConfigFile from './View/ChooseConfigFile.vue'
import CreateWorkflowInstance from './View/CreateWorkflowInstance'
import LogIn from './View/LogIn'
import SignUp from './View/SignUp'
import UserAdministration from './View/UserAdministration'
import VersionControl from './View/VersionControl'

const routes = [
  { path: '/ChooseConfigFile', component: ChooseConfigFile },
  { path: '/CreateWorkflowInstance', component: CreateWorkflowInstance },
  { path: '/LogIn', component: LogIn },
  { path: '/SignUp', component: SignUp },
  { path: '/UserAdministration', component: UserAdministration },
  { path: '/VersionControl', component: VersionControl },
]

export default new VueRouter({
  mode: 'history',
  routes,
})