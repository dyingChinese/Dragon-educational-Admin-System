<template>
  <el-row class="mb-8">
    <h1>床位信息</h1>
  </el-row>
  <el-table :data="tableData" style="width: 100%" v-loading="isLoading" stripe border
            size="small" lazy scrollbar-always-on flexible
            :header-cell-style="{ background: '#F5F7FA', color: '#909399' }"
  >
    <el-table-column prop="id" label="id" width="70"/>
    <el-table-column prop="capacity" label="宿舍容量"/>
    <el-table-column prop="capacityNum" label="此宿舍数量"/>

    <el-table-column prop="gender_allowed" label="允许性别" width="100" :filters="[
        { text: '男', value: 'M' },
        { text: '女', value: 'F' },
      ]" :filter-method="filterGender">
      <template #default="{row}">
        <span v-if="row.gender_allowed==='M'" style="color: var(--el-table-text-color);">男</span>
        <span v-else style="color: var(--el-table-text-color);">女</span>
      </template>
    </el-table-column>
    <el-table-column prop="" label="健康状况" align="center">
      <el-table-column prop="healthStatusArray.健康" label="健康" align="center"/>
      <el-table-column prop="healthStatusArray.慢性病" label="慢性病" align="center"/>
      <el-table-column prop="healthStatusArray.精神疾病" label="精神疾病" align="center"/>
      <el-table-column prop="healthStatusArray.残障人士" label="残障人士" align="center"/>
      <el-table-column prop="healthStatusArray.传染病" label="传染病" align="center"/>
    </el-table-column>
    <el-table-column prop="" label="总人数" :formatter="handleFomat"/>
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

import {onMounted, ref, watch} from 'vue'
import {useAxios} from "@/api";
import {DormitoryStatic} from "@/types/global.ts";

const tableData = ref<DormitoryStatic[]>([])
const {data, isLoading, execute} = useAxios('/api/infoSystem/dormitory/getDormitoryStatic')
const WindowLayoutMainRef = ref(null)
const WindowLayoutMain = ref(0)


const currentPage = ref(4)
const total = ref(0)
const pageSize = ref(100)
const small = ref(false)
const background = ref(false)
const disabled = ref(false)


const handleSizeChange = (val: number) => {
  pageSize.value = val
  execute('/api/infoSystem/dormitory/getDormitoryStatic', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  execute('/api/infoSystem/dormitory/getDormitoryStatic', {params: {page: currentPage.value, pageSize: pageSize.value}})
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
    tableData.value = mergeData(newData.data.records)
    console.log(tableData.value)
    currentPage.value = newData.data.current
    pageSize.value = newData.data.pageSize
    total.value = newData.data.total
  }
}, {
  immediate: true // 初始执行一次
})

function mergeData(data) {
  // 创建一个空对象来存储合并后的数据
  const mergedData = {};

  // 遍历原始数据
  data.forEach(item => {
    // 提取关键信息
    const {id, capacity, gender_allowed, health, healthNum} = item;

    // 初始化合并数据的结构
    const key = `${capacity}-${gender_allowed}`; // 使用容量和性别作为键
    if (!mergedData[key]) {
      mergedData[key] = {
        id,
        capacity,
        gender_allowed,
        genderNum: 0,
        healthStatusArray: [],
        capacityNum: 0
      };
    }

    // 累加性别数量和容量数量
    mergedData[key].genderNum += healthNum;
    mergedData[key].capacityNum += healthNum;

    // 查找healthStatusArray中是否已有对应的健康状态
    let healthStatus = mergedData[key].healthStatusArray.find(status => status.health === health);

    if (healthStatus) {
      // 如果有，则更新数量
      healthStatus.healthNum += healthNum;
    } else {
      // 如果没有，则添加新的健康状态
      healthStatus = {health, healthNum};
      mergedData[key].healthStatusArray.push(healthStatus);
    }
  });

  // 转换合并后的数据为数组形式
  const result = Object.values(mergedData);

  // 确保每个宿舍容量下的healthStatusArray只包含两个健康状态（男性和女性的）
  result.forEach(item => {
    // 对healthStatusArray按healthNum排序，然后只保留前两个
    item.healthStatusArray.sort((a, b) => b.health - a.health);
  });




  result.map(item => {
    item.healthStatusArray = item.healthStatusArray.reduce((accumulator, health) => {
      accumulator[health.health] = health.healthNum;
      return accumulator;
    }, {});
  });

  return result;
}

const handleFomat = (row, column, cellValue, index) => {
  return Object.values(row.healthStatusArray).reduce((accumulator, currentValue) => {
    return accumulator + currentValue;
  }, 0)
}

const filterGender = (value, row) => {
  return row.gender_allowed === value
}
</script>
<style scoped>
:deep(.el-input__inner) {
  min-width: 80px;
}

:deep(.el-select__wrapper) {
  min-width: 80px;
}
</style>
