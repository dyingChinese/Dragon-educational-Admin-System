import {defineStore} from "pinia"
import {ref} from "vue"
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import enUS from 'element-plus/es/locale/lang/en'
import {useToggle} from "@vueuse/core";

export const useToggleLanguage = defineStore("useToggleLanguage", () => {
    const [language, toggle] = useToggle(zhCn, {
        truthyValue: zhCn,
        falsyValue: enUS
    })
    return {language, toggle}
})


export const useSettingStore = defineStore("useSettingStore", () => {
    const theme = ref("dark")
    const themeList = ref(["dark", "light"])
    return {theme, themeList}
}, {persist: true})


export const useWindowLayout = defineStore("useWindowLayout", () => {
    const isAsideCollapse = ref(true)
    const headerHeight = ref(0);
    const mainHeight = ref(0);
    const footerHeight = ref(0);
    const setHeaderHeight = (height: number) => {
        headerHeight.value = height
    }
    const setMainHeight = (height: number) => {
        mainHeight.value = height
    }

    const setFooterHeight = (height: number) => {
        footerHeight.value = height
    }

    const setLayoutHeight = (header: number, main: number, footer: number) => {
        headerHeight.value = header
        mainHeight.value = main
        footerHeight.value = footer
    }

    const toggleAsideCollapse = () => {
        isAsideCollapse.value = !isAsideCollapse.value
    }
    return {
        isAsideCollapse,
        toggleAsideCollapse,
        headerHeight,
        setHeaderHeight,
        mainHeight,
        setMainHeight,
        footerHeight,
        setFooterHeight,
        setLayoutHeight
    }
})
