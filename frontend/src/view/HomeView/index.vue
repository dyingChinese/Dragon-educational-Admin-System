<template>
  <div class="w-full my-5 text-lg text-blue-500">首页</div>
  <div class="flex flex-wrap justify-center bg-gray-100  p-10">
    <div class="bg-white font-semibold text-center mx-auto rounded-3xl border shadow-lg p-10 max-w-xs">
      <h1 class=" text-gray-700">学生课表</h1>
      <h3 class="text-sm text-gray-400 "> 查看学生课表 </h3>
      <button class="bg-indigo-600 px-8 py-2 mt-8 rounded-3xl text-gray-100 font-semibold uppercase tracking-wide">前往</button>
    </div>
    <div class="bg-white font-semibold text-center mx-auto rounded-3xl border shadow-lg p-10 max-w-xs" v-if="hasPermission(['教务管理员'],'view_user')">
      <h1 class=" text-gray-700">信息管理系统</h1>
      <h3 class="text-sm text-gray-400 "> 查看系统信息 </h3>
      <button class="bg-indigo-600 px-8 py-2 mt-8 rounded-3xl text-gray-100 font-semibold uppercase tracking-wide">前往</button>
    </div>
    <div class="bg-white font-semibold text-center mx-auto rounded-3xl border shadow-lg p-10 max-w-xs" v-if="hasPermission(['宿舍管理员'],'view_dormitory')">
      <h1 class=" text-gray-700">宿舍管理系统</h1>
      <h3 class="text-sm text-gray-400 "> 查看宿舍情况 </h3>
      <button class="bg-indigo-600 px-8 py-2 mt-8 rounded-3xl text-gray-100 font-semibold uppercase tracking-wide">前往</button>
    </div>
    <div class="bg-white font-semibold text-center mx-auto rounded-3xl border shadow-lg p-10 max-w-xs" v-if="hasPermission(['教务管理员'])">
      <h1 class=" text-gray-700">统计面板</h1>
      <h3 class="text-sm text-gray-400 "> 查看数据统计 </h3>
      <button class="bg-indigo-600 px-8 py-2 mt-8 rounded-3xl text-gray-100 font-semibold uppercase tracking-wide">前往</button>
    </div>
    <div class="bg-white font-semibold text-center mx-auto rounded-3xl border shadow-lg p-10 max-w-xs">
      <h1 class=" text-gray-700">系统设置</h1>
      <h3 class="text-sm text-gray-400 "> 系统设置 </h3>
      <button class="bg-indigo-600 px-8 py-2 mt-8 rounded-3xl text-gray-100 font-semibold uppercase tracking-wide">前往</button>
    </div>
  </div>
  <div class="w-full">

  </div>
</template>


<script setup lang="ts">

import {hasPermission} from "@/utils/permission.ts";
</script>
<style scoped>

</style>
