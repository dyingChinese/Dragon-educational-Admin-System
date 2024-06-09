/// <reference types="vite/client" />
declare module "*.vue" {
    import type {DefineComponent} from "vue"
    const vueComponent: DefineComponent<{}, {}, any>
    export default vueComponent
}

declare module "*.ts" {

}
declare module "element-plus/dist/locale/zh-cn.mjs"

declare module "*.scss" {
    const classes: { readonly [key: string]: string };
    export default classes;
}
