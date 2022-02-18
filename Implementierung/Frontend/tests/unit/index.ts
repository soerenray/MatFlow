import Vue from "vue";
import Vuetify from "vuetify";
//Search icons: https://materialdesignicons.com/
import PlusIcon from 'vue-material-design-icons/Plus.vue';
import FileDocumentOutlineIcon from 'vue-material-design-icons/FileDocumentOutline.vue'
import FileRestoreIcon from 'vue-material-design-icons/FileRestore.vue'
import DeleteIcon from 'vue-material-design-icons/Delete.vue'
import LockClockIcon from 'vue-material-design-icons/LockClock.vue'
import MemeoryIcon from 'vue-material-design-icons/Memory.vue'
import SendIcon from 'vue-material-design-icons/Send.vue'

Vue.component('plus-icon', PlusIcon);
Vue.component('file-document-outline-icon', FileDocumentOutlineIcon)
Vue.component('file-restore-icon', FileRestoreIcon)
Vue.component('delete-icon', DeleteIcon)
Vue.component('lock-clock-icon', LockClockIcon)
Vue.component('memory-icon', MemeoryIcon)
Vue.component('send-icon', SendIcon)

Vue.config.productionTip = false;
Vue.use(Vuetify);