<template>
  <el-row  class="mb-8">
      <h1>学生信息</h1>
  </el-row>
  <el-table :data="tableData" style="width: 100%" v-loading="isLoading" stripe border
            size="small" lazy scrollbar-always-on flexible>
    <el-table-column prop="id" label="id" width="70"/>
    <el-table-column prop="nickname" label="nickname"/>
    <el-table-column prop="username" label="name" width="100"/>
    <el-table-column prop="gender" label="gender" width="60">
      <template #default="scope">
        <span v-if="scope.row.gender==='M'" style="color: var(--el-table-text-color);">男</span>
        <span v-else style="color: var(--el-table-text-color);">女</span>
      </template>
    </el-table-column>
    <el-table-column prop="email" label="email"/>
    <el-table-column prop="last_login" label="last_login" :formatter="row => formatDate(row.last_login)"/>
    <el-table-column prop="mobile" label="mobile"/>
    <el-table-column prop="official_id" label="身份证号"/>
    <el-table-column prop="ethnicity" label="民族" width="70"/>
    <el-table-column prop="political_affiliation" label="政治面貌"/>
    <el-table-column prop="dormitory" label="宿舍">
      <template #default="scope">
        <el-text v-if="scope.row.dormitory" type="info" class="cursor-pointer hover:underline hover:text-blue-500"
                 @click="handleDormitory(scope.$index, scope.row)">有
        </el-text>
        <span v-else>无</span>
      </template>
    </el-table-column>
    <el-table-column prop="status" label="status">
      <template #default="scope">
        <span v-if="scope.row.status === -3">待激活</span>
        <span v-else-if="scope.row.status === -2">异常</span>
        <span v-else-if="scope.row.status === -1">注销</span>
        <span v-else-if="scope.row.status === 0">正常</span>
        <span v-else-if="scope.row.status === 1">封号</span>
        <span v-else type="danger">禁用</span>
      </template>
    </el-table-column>
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
      <el-form-item label="昵称" prop="nickname">
        <el-input v-model="form.nickname"/>
      </el-form-item>
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username"/>
      </el-form-item>
      <el-form-item label="性别" prop="gender">
        <el-select v-model="form.gender" :placeholder="form.gender?.toString()">
          <el-option label="男" value="M"/>
          <el-option label="女" value="F"/>
        </el-select>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email"/>
      </el-form-item>
      <el-form-item label="手机号" prop="mobile">
        <el-input v-model="form.mobile"/>
      </el-form-item>
      <el-form-item label="身份证号" prop="official_id">
        <el-input v-model="form.official_id"/>
      </el-form-item>
      <el-form-item label="民族" prop="ethnicity">
        <el-input v-model="form.ethnicity"/>
      </el-form-item>
      <el-form-item label="政治面貌" prop="political_affiliation">
        <el-input v-model="form.political_affiliation"/>
      </el-form-item>
      <el-form-item label="账号状态" prop="status">
        <el-select v-model="form.political_affiliation">
          <el-option label="正常" :value="0"/>
          <el-option label="封号" :value="1"/>
          <el-option label="注销" :value="-1"/>
          <el-option label="异常" :value="-2"/>
          <el-option label="待激活" :value="-3"/>
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="submitForm(ruleFormRef)">确 定</el-button>
    </template>
  </el-dialog>
</template>


<script setup lang="ts">

import {ref, onMounted, watch, computed} from 'vue'
import {useAxios} from "@/api";
import {useWindowLayout} from "@/store/setting.ts";
import {formatDate} from "@/utils/Date";
import {ElMessage, FormInstance} from "element-plus";
import {User} from "@/types/global.ts";

const tableData = ref<User[]>([])
const {data, isLoading, execute} = useAxios('/api/infoSystem/userStu')
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
const ruleFormRef = ref<FormInstance>()
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
const rules = []

const handleSizeChange = (val: number) => {
  pageSize.value = val
  execute('/api/infoSystem/userStu', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
const handleCurrentChange = (val: number) => {
currentPage.value = val
  execute('/api/infoSystem/userStu', {params: {page: currentPage.value, pageSize: pageSize.value}})
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




const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
      execute('/api/infoSystem/userStu/' + form.value.id, {
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


</script>
<style scoped>
:deep(.el-input__inner) {
  min-width: 80px;
}

:deep(.el-select__wrapper) {
  min-width: 80px;
}
</style>
