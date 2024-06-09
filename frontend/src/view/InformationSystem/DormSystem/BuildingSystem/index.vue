<template>
  <el-row :gutter="20" class="mb-16">
    <div class="flex flex-col items-start gap-4">
      <el-segmented v-model="segmentedValue" :options="segmentedOptions" size="large" @change="handleSegmentedChange"/>
    </div>
  </el-row>
  <el-table :data="tableData" style="width: 100%" v-loading="isLoading" stripe border
            size="small" lazy scrollbar-always-on flexible column-key="id"
  >
    >
    <el-table-column prop="id" label="id" width="70"/>
    <el-table-column prop="user_name" label="姓名"/>
    <el-table-column prop="room_number" label="宿舍号" sortable/>
    <el-table-column prop="capacity" label="宿舍容量" width="120" sortable/>
    <el-table-column prop="gender_allowed" label="允许性别" width="100" :filters="[
        { text: '男', value: 'M' },
        { text: '女', value: 'F' },
      ]" :filter-method="filterGender">
      <template #default="scope">
        <span v-if="scope.row.gender_allowed==='M'" style="color: var(--el-table-text-color);">男</span>
        <span v-else style="color: var(--el-table-text-color);">女</span>
      </template>
    </el-table-column>
    <el-table-column prop="address" label="所属位置"/>
    <el-table-column prop="emergency_contact" label="紧急联系人"/>
    <el-table-column prop="emergency_contact_phone" label="紧急联系人电话"/>
    <el-table-column prop="health" label="健康状况"/>
    <el-table-column prop="warden_name" label="楼栋负责人"/>
    <el-table-column prop="" label="操作" min-width="120">
      <template #default="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
          Edit
        </el-button>
      </template>
    </el-table-column>
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
  <el-dialog v-model="dialogVisible" title="编辑用户信息" center align-center
             :before-close="handleClose">
    <el-form :model="form" :rules="rules" ref="ruleFormRef" inline>
      <el-form-item label="姓名" prop="userName">
        <el-input v-model="form.user_name"/>
      </el-form-item>
      <el-form-item label="宿舍号" prop="roomNumber">
        <el-input v-model="form.room_number"/>
      </el-form-item>
      <el-form-item label="宿舍容量" prop="capacity">
        <el-input v-model="form.capacity"/>
      </el-form-item>
      <el-form-item label="允许性别" prop="genderAllowed">
        <el-input v-model="form.gender_allowed"/>
      </el-form-item>
      <el-form-item label="宿舍位置" prop="address">
        <el-input v-model="form.address"/>
      </el-form-item>
      <el-form-item label="紧急联系人" prop="emergencyContact">
        <el-input v-model="form.emergency_contact"/>
      </el-form-item>
      <el-form-item label="紧急联系人电话" prop="emergencyContactPhone">
        <el-input v-model="form.emergency_contact_phone"/>
      </el-form-item>
      <el-form-item label="健康状况" prop="health">
        <el-input v-model="form.health"/>
      </el-form-item>
      <el-form-item label="楼栋负责人" prop="wardenName">
        <el-input v-model="form.warden_name"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="submitForm(ruleFormRef)">确 定</el-button>
    </template>
  </el-dialog>
</template>


<script setup lang="ts">
import {ref, onMounted, watch, computed, reactive} from 'vue'
import {useAxios} from "@/api";


const segmentedValue = ref('全部')
const tableData = ref<User[]>([])
const tableDataTotal = ref<User[]>([])
const {data, isLoading, execute} = useAxios('/api/infoSystem/dormitory')
const WindowLayoutMainRef = ref(null)
const WindowLayoutMain = ref(0)


const dialogVisible = ref(false)
const currentPage = ref(1)
const total = ref(0)
const pageSize = ref(70)
const small = ref(false)
const background = ref(false)
const disabled = ref(false)
import {ElMessage, FormInstance, FormRules} from 'element-plus'
import {Dormitory} from "@/types/global.ts";

const ruleFormRef = ref<FormInstance>()
const segmentedOptions = ['全部', '东区', '西区', '南区', '北区']
const form = ref<Dormitory>({
  id: -1,
  user_name: '',
  room_number: '',
  capacity: 0,
  gender_allowed: '',
  address: '',
  emergency_contact: '',
  emergency_contact_phone: '',
  health: '',
  warden: -1,
  warden_name: '',

})


const handleSizeChange = (val: number) => {
  pageSize.value = val
  console.log('pageSize', pageSize.value)
  execute('/api/infoSystem/dormitory', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
const handleCurrentChange = (val: number) => {
  console.log('currentPage', val)
  currentPage.value = val
  execute('/api/infoSystem/dormitory', {params: {page: currentPage.value, pageSize: pageSize.value}})
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
    tableDataTotal.value = newData.data.records
    currentPage.value = newData.data.currentPage
    pageSize.value = newData.data.pageSize
    total.value = newData.data.total
  }
}, {
  immediate: true // 初始执行一次
})
const rules = reactive<FormRules<typeof ruleForm>>({
  user_name: [
    {required: true, message: '请输入姓名', trigger: 'blur'},
  ],
  room_number: [
    {required: true, message: '请输入宿舍号', trigger: 'blur'},
  ],
  capacity: [
    {required: true, message: '请输入宿舍容量', trigger: 'blur'},
  ]

})
const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
      execute('/api/infoSystem/dormitory/' + form.value.id, {
        method: 'PUT',
        headers: {"Content-Type": "application/json"},
        data: form.value,
      }).then(res => {
        const {code, msg} = res.data.value
        if (code === 200200) {
          ElMessage.success(msg)
          dialogVisible.value = false
        } else {
          ElMessage.error(msg)
        }
      })
    } else {
      console.log('error submit!')
    }
  })
}


const handleEdit = (index: number, row: Dormitory) => {
  form.value = row
  dialogVisible.value = true
}
const handleDelete = (index: number, row: Dormitory) => {
  console.log(index, row)
}
const handleClose = (done: () => void) => {
  done()
}
const handleDormitory = (index: number, row: Dormitory) => {
  console.log(index, row)
}
const filterHandler = (value: string, row: Dormitory) => {
  return row.address === segmentedValue.value
}
const handleFilterChange = (value: string) => {

}

const filterGender = (value: string, row: Dormitory) => {
  return row.gender_allowed === value
}
const handleSegmentedChange = (value: string) => {
  tableData.value = tableDataTotal.value.filter(item => value === '全部' ? true : item.address === value)
}
</script>
<style scoped>

</style>
