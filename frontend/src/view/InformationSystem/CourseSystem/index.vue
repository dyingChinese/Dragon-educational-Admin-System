<template>
  <el-row class="mb-8">
    <h1>课程信息</h1>
  </el-row>
  <el-table :data="tableData" style="width: 100%" v-loading="isLoading" stripe border
            size="small" lazy scrollbar-always-on flexible tooltip-effect="light">
    <el-table-column prop="id" label="id" width="70"/>
    <el-table-column prop="name" label="课程名"/>
    <el-table-column prop="description" label="课程简介" show-overflow-tooltip/>
    <el-table-column prop="credits" label="学分" width="100"/>
    <el-table-column prop="location" label="开课地点"/>
    <el-table-column prop="time" label="时间"/>

    <el-table-column prop="type" label="类型">
      <!--   row解构了本行   -->
      <template #default="{row}">
        <el-tag v-if="row.type === '必修'" type="danger">必修</el-tag>
        <el-tag v-else type="primary">选修</el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="students" label="学生数量"/>
    <el-table-column prop="teacher" label="开课教师" show-overflow-tooltip>
      <template #default="{row}">
        <span  class="text-gray-600/70 cursor-pointer hover:underline hover:text-blue-500" v-for="teacher in row.teacher" :key="teacher.id" type="success">{{ teacher.username }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="official_code" label="课程代码"/>
  </el-table>
  <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[70, 100, 150, 200,300,500]"
      :small="small"
      :disabled="disabled"
      :background="background"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
  />
</template>


<script setup lang="ts">

import {ref, onMounted, watch, computed} from 'vue'
import {useAxios} from "@/api";
import {Course} from "@/types/global.ts";

const tableData = ref<Course[]>([])
const {data, isLoading, execute} = useAxios('/api/infoSystem/course')
const WindowLayoutMainRef = ref(null)
const WindowLayoutMain = ref(0)


const currentPage = ref(4)
const total = ref(0)
const pageSize = ref(100)
const small = ref(false)
const background = ref(false)
const disabled = ref(false)


const handleSizeChange = (val: number) => {
  execute('/api/infoSystem/course', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
const handleCurrentChange = (val: number) => {
  execute('/api/infoSystem/course', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
onMounted(() => {
  WindowLayoutMainRef.value = document.getElementById('WindowLayoutMain') as HTMLDivElement
  WindowLayoutMain.value = WindowLayoutMainRef.value.offsetHeight
  window.addEventListener('resize', () => {
    WindowLayoutMain.value = WindowLayoutMainRef.value.offsetHeight
  })
})


// // 使用watch监听data的变化，并在数据更新时设置tableData
watch(data, (newData) => {
  if (newData && newData.data && newData.data.records) {
    tableData.value = newData.data.records
    currentPage.value = newData.data.current
    pageSize.value = newData.data.pageSize
    total.value = newData.data.total
  }
}, {
  immediate: true // 初始执行一次
})


</script>
<style scoped>
:deep(.el-input__inner) {
  min-width: 80px;
}

:deep(.el-select__wrapper) {
  min-width: 80px;
}
</style>
