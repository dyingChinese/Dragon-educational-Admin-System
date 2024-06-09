<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="200px">
        <router-view name="globalLayoutAside"/>
      </el-aside>
      <el-container>
        <el-header ref="WindowLayoutHeader" id="WindowLayoutHeader">
          <router-view name="globalLayoutHeader"/>
        </el-header>
        <el-main ref="WindowLayoutMain" id="WindowLayoutMain">
              <Transition  name="slide-fade">
                <router-view/>
              </Transition>
        </el-main>
        <el-footer ref="WindowLayoutFooter" id="WindowLayoutFooter">
          <router-view name="globalLayoutFooter"/>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>


<script setup lang="ts">
import {onMounted, ref, computed, nextTick} from 'vue'
import {useWindowLayout} from "@/store/setting.ts";

const WindowLayoutHeader = ref(null)
const WindowLayoutMain = ref(null)
const WindowLayoutFooter = ref(null)

const windowLayout = useWindowLayout()

onMounted(async () => {
  await nextTick();
  const updateDimensions = () => {
    const headerHeight = WindowLayoutHeader.value?.offsetHeight || 0;
    const mainHeight = WindowLayoutMain.value?.offsetHeight || 0;
    const footerHeight = WindowLayoutFooter.value?.offsetHeight || 0;
    windowLayout.setLayoutHeight(headerHeight, mainHeight, footerHeight);
  };
  updateDimensions();
  window.addEventListener('resize', updateDimensions);
})


</script>
<style scoped>
.common-layout {
  height: 100%;
  min-height: 100%;

  .el-aside {
    height: 100%;
    min-height: 100vh;
    background-color: #f5f7fa;
  }
}

</style>
<style>

</style>
