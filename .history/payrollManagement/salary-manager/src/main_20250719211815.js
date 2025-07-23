import { createApp } from 'vue';
import axios from 'axios'
import './style.css'
import './index.css'
import router from './router'
import App from './App.vue'

axios.defaults.baseURL = 'http://127.0.0.1:5000'
createApp(App).use(router).mount('#app')
