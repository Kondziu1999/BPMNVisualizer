import { createApp } from 'vue'
import vuetify from './plugins/vuetify'
import App from './App.vue'

const app = createApp(App)
app.use(vuetify)

app.component('v-alert')

app.mount('#app')
