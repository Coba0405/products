import { createApp } from 'vue'
import axios from 'axios'
import './style.css'
import './index.css'
import router from './router'
import App from './App.vue'

axios.defaults.baseURL = 'http://lacalhost'
createApp(App).use(router).mount('#app')
