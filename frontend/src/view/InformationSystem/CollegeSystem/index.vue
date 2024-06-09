<template>
  <el-row  class="mb-8">
    <h1>学院信息</h1>
  </el-row>
  <el-table :data="tableData" style="width: 100%" v-loading="isLoading" stripe border
            size="small" lazy scrollbar-always-on flexible>
    <el-table-column prop="id" label="id" width="70"/>
    <el-table-column prop="institute" label="学院名称"/>
    <el-table-column prop="domainCount" label="专业总数"/>
    <el-table-column prop="stuNum" label="学生总数"/>
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
import {Collage} from "@/types/global.ts";

const tableData = ref<Collage[]>([])
const {data, isLoading, execute} = useAxios('/api/infoSystem/institute')

const currentPage = ref(4)
const total = ref(0)
const pageSize = ref(100)
const small = ref(false)
const background = ref(false)
const disabled = ref(false)


const handleSizeChange = (val: number) => {
  execute('/api/infoSystem/institute', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
const handleCurrentChange = (val: number) => {
  execute('/api/infoSystem/institute', {params: {page: currentPage.value, pageSize: pageSize.value}})
}


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
