import {createApp} from 'vue'
import {createPinia} from 'pinia'
import ElementPlus from 'element-plus'
import router from '@/router/index.ts'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './style.css'
import App from './App.vue'
// 如果您正在使用CDN引入，请删除下面一行。
import piniaPluginPersistedstate from "pinia-plugin-persistedstate"

const pinia = createPinia()

pinia.use(piniaPluginPersistedstate) //持久化插件

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
localStorage.setItem('AUTH_TOKEN', 'eyJsZW4iOjI1NiwidHlwIjoiSldUIiwidHlwZSI6IlJTQSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJ1c2VyQXV0aG9yaXR5IiwiYXV0aG9yaXR5IjoiMCIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3QiLCJpc0FkbWluIjpmYWxzZSwiZXhwIjoxNjkwMTMyNzI5LCJpYXQiOjE2OTAxMzI3MjksInVzZXJJZCI6IjIiLCJqdGkiOiI1MDEyODk2Zi01MGU0LTQ4ODQtYjViZC1iZDY1ODIxNWI1NWMiLCJ1c2VybmFtZSI6ImFkbWluIn0.V1hRVGTrrZarRhFn0T5kPwCp4V0OgQCwj3EYtYwZIWQ1Nc3LA3UYvJ8pyDBFoWNYfnILiN6Ay0mhmLzudb44Jp6DYjIN6wJ9fJ_8oDHQwaNKHTUZ_Cp_wJpIBxxOcyWNmubvYH-zTbNZRzwseRkkE9wDOJhalCeW_LMh6wholsUgdUjtsRPfblN_E6XCgI2D_gx7_JkuhOLiaduAgT284jBKs-iGXexvpmKQF7xC0uum0wWLcOG3QtPmVZJRs7vyB4mzL0L18T9sn7_0IYegrw1pnYoA-QRxzhQgPf8jUPXeJurHQ1qClx1kgG7BGG74kg8VSuSTNZHlS860lmEQEQ')
app.use(ElementPlus)
app.use(pinia)
app.use(router)
app.mount('#app')
