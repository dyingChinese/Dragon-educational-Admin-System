<script setup lang="ts">
import {ref} from 'vue'
import {useToggle} from '@vueuse/core'
import {ElConfigProvider} from 'element-plus'
import {useToggleLanguage} from "@/store/setting.ts";


const zIndex = ref(3000)
const size = ref('small')
const language = useToggleLanguage().language

</script>

<template>
  <el-config-provider :size="size" :z-index="zIndex" :locale="language">
    <RouterView/>
  </el-config-provider>
</template>

<style scoped>

</style>
