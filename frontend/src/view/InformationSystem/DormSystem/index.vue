<template>
  <el-row :gutter="20" class="mb-16">
    <div class="flex flex-col items-start gap-4">
      <el-segmented v-model="value" :options="options" size="large" />
      <el-segmented v-model="value" :options="options" size="default" />
      <el-segmented v-model="value" :options="options" size="small" />
    </div>
  </el-row>

</template>


<script setup lang="ts">
import {ref, onMounted, watch, computed} from 'vue'
import {useAxios} from "@/api";
import {useWindowLayout} from "@/store/setting.ts";
import {formatDate} from "@/utils/Date";
const value = ref('Mon')
const tableData = ref<User[]>([])
const {data, isLoading, execute} = useAxios('/api/infoSystem/user')
const WindowLayoutMainRef = ref(null)
const WindowLayoutMain = ref(0)

const windowLayout = useWindowLayout()
const dialogVisible = ref(false)
const currentPage = ref(4)
const total = ref(0)
const pageSize = ref(100)
const small = ref(false)
const background = ref(false)
const disabled = ref(false)
const options = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const form = ref<User>({
  id: -1,
  username: '',
  nickname: '',
  email: '',
  mobile: '',
  username: '',
  role: '',
  status: 0,
  nickname: '',
  avatar: '',
  mobile: '',
  email: '',
  gender: '',
  description: '',
  create_time: '',
  official_id: '',
  last_update_time: '',
  political_affiliation: '',
  ethnicity: '',
  groups: [],
  permissions: [],
  dormitory: {},
  last_login: '',
  is_superuser: false,
  is_staff: false,
  is_active: false,
  date_joined: '',
})


const handleSizeChange = (val: number) => {
  execute('/api/infoSystem/user', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
const handleCurrentChange = (val: number) => {
  execute('/api/infoSystem/user', {params: {page: currentPage.value, pageSize: pageSize.value}})
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
const handleEdit = (index: number, row: User) => {
  form.value = row
  dialogVisible.value = true
}
const handleDelete = (index: number, row: User) => {
  console.log(index, row)
}
const handleClose = (done: () => void) => {
  done()
}
const handleDormitory = (index: number, row: User) => {
  console.log(index, row)
}
</script>
<style scoped>

</style>
