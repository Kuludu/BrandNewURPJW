import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import VueCookies from 'vue-cookies'
import axios from "axios";
import api from './config/server'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue'



Vue.use(BootstrapVue)
Vue.use(VueCookies)
Vue.config.productionTip = false

Vue.prototype.API = api
Vue.prototype.axios = axios

Vue.$cookies.config('7d')

new Vue({
  render: h => h(App),
}).$mount('#app')
