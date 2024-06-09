<template>
  <el-menu class="el-menu-demo" mode="horizontal" :ellipsis="false" @select="handleSelect">
    <el-menu-item index="0">

    </el-menu-item>
    <div class="flex-grow" />
    <el-menu-item index="1">
      <el-badge value="5" class="item" :max="99">
        <el-icon>
          <Bell />
        </el-icon>
      </el-badge>
    </el-menu-item>

    <el-menu-item index="2" style="width: var(--el-header-height);">
      <el-dropdown>
        <el-avatar :size="30" :src="userSvg">
          <img :src="userSvg" />
        </el-avatar>
        <template #dropdown>
          <el-dropdown-item @click="router.push('/profile')">个人中心</el-dropdown-item>
          <el-dropdown-item>切换主题</el-dropdown-item>
          <el-dropdown-item divided @click="router.push('/login')">登出</el-dropdown-item>
        </template>
      </el-dropdown>

    </el-menu-item>
    <span style="width: 30px;" />
  </el-menu>
</template>


<script setup lang="ts">
import userSvg from "@/assets/svg/user.svg"
import { ref } from "vue"
import router from "@/router/index.ts"
import { Bell } from "@element-plus/icons-vue"
ref(0)
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}
</script>
<style scoped lang="less">
/* 去除边框 */
:deep(.el-select .el-input__wrapper) {
  box-shadow: none !important;
}

:deep(.el-badge .el-badge__content) {
  margin-top: 16px;
}

/* 去除选中时蓝色边框（下面两个都要加上） */
:deep(.el-input .el-input__wrapper.is-focus) {
  box-shadow: none !important;
}

.flex-grow {
  flex-grow: 1;
}

.el-menu--horizontal > .el-menu-item.is-active {
  border: none;
}
</style>
