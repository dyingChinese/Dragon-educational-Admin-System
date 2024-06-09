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

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.4s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}

//-----------------//


.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.6s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

//-----------------//

.slide-enter-active,
.slide-leave-active {
  transition: all 0.75s ease-out;
}


.slide-enter-to {
  position: absolute;
  right: 0;
}


.slide-enter-from {
  position: absolute;
  right: -100%;
}


.slide-leave-to {
  position: absolute;
  left: -100%;
}


.slide-leave-from {
  position: absolute;
  left: 0;
}

//-----------------//

.scale-enter-active,
.scale-leave-active {
  transition: all 1s ease;
}


.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.5);
}

</style>
