import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {join} from "path"
import vueJsxPlugin from "@vitejs/plugin-vue-jsx";
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver} from 'unplugin-vue-components/resolvers'
// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueJsxPlugin(),
        AutoImport({
            resolvers: [ElementPlusResolver()],
        }),
        Components({
            resolvers: [ElementPlusResolver()],
        }),
    ],
    resolve: {
        alias: {
            "@": join(__dirname, "./src")
        }
    },
    server:{
        proxy:{
            "^/api": {
                target: "http://localhost:8000",
                rewrite: (path) => {
                    console.log(`path = ${path}, TO = ${path.replace(/^\/api\/+/, "")}`)
                    return path.replace(/^\/api\/+/, "")
                },
                changeOrigin: true
            }
        }
    }
})
