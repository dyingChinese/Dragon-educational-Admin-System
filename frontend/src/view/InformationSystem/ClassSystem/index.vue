<template>
  <el-row :gutter="20" class="mb-16">
    <div class="flex flex-col items-start gap-4">
      <el-segmented v-model="segmentedValue" :options="segmentedOptions" @change="handleSegmentedChange"
                    size="default" :block="false"/>
    </div>
  </el-row>
  <el-table :data="tableData" style="width: 100%" v-loading="isLoading" stripe border
            size="small" lazy scrollbar-always-on flexible>
    <el-table-column prop="id" label="id" width="70"/>
    <el-table-column prop="institute" label="学院"/>
    <el-table-column prop="domain" label="专业"/>
    <el-table-column prop="grade" label="年级"/>
    <el-table-column prop="aclass" label="班级"/>
    <el-table-column prop="count" label="班级人数"/>
    <el-table-column prop="average" label="班级平均绩点"/>
    <el-table-column prop="duration" label="学制"/>
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

import {ref, onMounted, watch, computed, reactive} from 'vue'
import {useAxios} from "@/api";
import {FormInstance} from "element-plus";
import {Aclass} from "@/types/global.ts";
import segmented from "@/components/Segmented.vue";


const segmentedValue = ref('全部学院')
const segmentedOptions = ref(['全部学院', '法学院', '医学院'])
const tableData = ref<Aclass[]>([])
const tableDataTotal = ref<Aclass[]>([])
const {data, isLoading, execute} = useAxios('/api/infoSystem/aclass')
const {data: InstituteMinds, isLoading: InstituteIsLoading} = useAxios('/api/infoSystem/aclass/getInstitute')
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
  execute('/api/infoSystem/aclass', {
    params: {
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: segmentedValue.value
    }
  })
}
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  execute('/api/infoSystem/aclass', {
    params: {
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: segmentedValue.value
    }
  })
}
onMounted(() => {
  WindowLayoutMainRef.value = document.getElementById('WindowLayoutMain') as HTMLDivElement
  WindowLayoutMain.value = WindowLayoutMainRef.value.offsetHeight
  window.addEventListener('resize', () => {
    WindowLayoutMain.value = WindowLayoutMainRef.value.offsetHeight
  })
})


// // 使用watch监听data的变化，并在数据更新时设置tableData
watch(InstituteMinds, (newData) => {
  if (newData && newData.data) {
    segmentedOptions.value = ['全部学院', ...newData.data]
  }
}, {
  immediate: true // 初始执行一次
})


watch(data, (newData) => {
  if (newData && newData.data && newData.data.records) {
    tableData.value = newData.data.records
    tableDataTotal.value = newData.data.total
    currentPage.value = newData.data.current
    pageSize.value = newData.data.pageSize
    total.value = newData.data.total
    console.log(tableData)
  }
}, {
  immediate: true // 初始执行一次
})


const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
    } else {
      console.log('error submit!')
    }
  })
}
const handleSegmentedChange = (value: string) => {
  execute('/api/infoSystem/aclass', {
    params: {
      page: currentPage.value,
      pageSize: pageSize.value,
      keyword: segmentedValue.value
    }
  })
}
</script>
<style scoped>
:deep(.el-input__inner) {
  min-width: 80px;
}

:deep(.el-select__wrapper) {
  min-width: 80px;
}

:deep(.el-segmented__group) {
  width: 100%;
  display: flex;
  flex: 1;
  flex-shrink: initial;
  justify-content: center;
  flex-wrap: wrap;
}

:deep(.el-segmented__item) {
  width: min-content;
  height: 40px;
  line-height: 40px;
  cursor: pointer;
  border-radius: 4px;
}
</style>
