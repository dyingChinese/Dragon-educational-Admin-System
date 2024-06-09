<template>
  <el-row  class="mb-8">
    <h1>教师信息</h1>
  </el-row>
  <el-table :data="tableData" style="width: 100%" v-loading="isLoading" stripe border
            size="small" lazy scrollbar-always-on flexible>
    <el-table-column prop="id" label="id" width="70"/>
    <el-table-column prop="username" label="姓名" width="100"/>
    <el-table-column prop="gender" label="性别" width="60">
      <template #default="scope">
        <span v-if="scope.row.gender==='M'" style="color: var(--el-table-text-color);">男</span>
        <span v-else style="color: var(--el-table-text-color);">女</span>
      </template>
    </el-table-column>
    <el-table-column prop="mobile" label="手机"/>
    <el-table-column prop="political_affiliation" label="政治面貌"/>
    <el-table-column prop="status" label="账号状态">
      <template #default="scope">
        <span v-if="scope.row.status === -3">待激活</span>
        <span v-else-if="scope.row.status === -2">异常</span>
        <span v-else-if="scope.row.status === -1">注销</span>
        <span v-else-if="scope.row.status === 0">正常</span>
        <span v-else-if="scope.row.status === 1">封号</span>
        <span v-else type="danger">禁用</span>
      </template>
    </el-table-column>
    <el-table-column prop="usersubtablestea" label="教师信息" align="center">
      <el-table-column prop="usersubtablestea.title" label="职称"/>
      <el-table-column prop="usersubtablestea.department" label="部门"/>
      <el-table-column prop="usersubtablestea.position" label="职位"/>
      <el-table-column prop="usersubtablestea.office_location" label="办公室位置"/>
      <el-table-column prop="usersubtablestea.research_interests" label="研究">
        <template #default="scope">
          <el-tooltip :show-after="400"
                      class="box-item"
                      effect="light"
                      :content="scope.row.usersubtablestea?.research_interests?scope.row.usersubtablestea?.research_interests:'无'"
          >
            <span class="overflow-hidden text-gray-600 h-9 truncate">{{
                scope.row.usersubtablestea?.research_interests ? scope.row.usersubtablestea?.research_interests : '无'
              }}</span>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table-column>
    <el-table-column prop="groups" label="角色">
      <template #default="scope">
        <el-tag v-for="(tag) in scope.row.groups" :key="tag.id" type="primary" size="small">
          {{ tag.name }}
        </el-tag>
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
  <el-dialog v-model="dialogVisible" title="编辑用户信息" center align-center>
    <el-form :model="form" ref="ruleFormRef" :rules="rules" inline>
      <el-form-item label="姓名" prop="username">
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
        <el-select v-model="form.political_affiliation" :placeholder="form.political_affiliation.toString()">
          <el-option v-for="opt in political_affiliationOptions" :label="opt.label" :key="opt.label"/>
        </el-select>
      </el-form-item>
      <el-form-item label="账号状态" prop="status">
        <el-select v-model="form.status" :placeholder="form.status.toString()">
          <el-option label="正常" :value="0"/>
          <el-option label="封号" :value="1"/>
          <el-option label="注销" :value="-1"/>
          <el-option label="异常" :value="-2"/>
          <el-option label="待激活" :value="-3"/>
        </el-select>
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-tag v-for="(tag) in form.groups" :key="tag.id" type="primary" size="small">
          {{ tag.name }}
        </el-tag>
      </el-form-item>
      <el-form-item label="头像" prop="avatar">
        <el-upload
            class="avatar-uploader"
            action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
        >
          <img v-if="form.avatar" :src="form.avatar" class="avatar w-10 h-10"/>
          <el-icon v-else class="avatar-uploader-icon">
            <Plus/>
          </el-icon>
        </el-upload>
      </el-form-item>
      <el-form-item label="描述" prop="description">
        <el-input v-model="form.description" type="textarea"/>
      </el-form-item>
      <el-form-item label="是否超级用户" prop="is_superuser">
        <el-input v-model="form.is_superuser" hidden="hidden" disabled/>
      </el-form-item>
      <el-form-item label="是否激活" prop="is_active">
        <el-checkbox v-model="form.is_active" type="checkbox" :checked="form.is_active"/>
      </el-form-item>
      <div class="" v-if="isObjectNotEmpty(form.usersubtablestea)">
        <el-form-item label="部门">
          <el-input v-model="form.usersubtablestea.department"/>
        </el-form-item>
        <el-form-item label="职称">
          <el-input v-model="form.usersubtablestea.title"/>
        </el-form-item>
        <el-form-item label="职位">
          <el-input v-model="form.usersubtablestea.position"/>
        </el-form-item>
        <el-form-item label="办公室位置">
          <el-input v-model="form.usersubtablestea.office_location"/>
        </el-form-item>
        <el-form-item label="研究">
          <el-input v-model="form.usersubtablestea.research_interests"/>
        </el-form-item>
      </div>
    </el-form>
    <template #footer>
      <el-button type="primary" @click="submitForm(ruleFormRef)">保存</el-button>
      <el-button @click="dialogVisible=false">取消</el-button>
    </template>
  </el-dialog>
</template>


<script setup lang="ts">

import {ref, onMounted, watch, computed, reactive} from 'vue'
import {useAxios} from "@/api";
import {Plus} from "@element-plus/icons-vue";
import {useWindowLayout} from "@/store/setting.ts";
import {UserSubTablesTEA} from "@/types/global.ts";
import type {User} from "@/types/global.ts";
import {isObjectNotEmpty} from "@/utils/objUtils";
import {ElMessage, FormInstance, FormRules} from "element-plus";


const tableData = ref<UserComb[]>([])
const {data, isLoading, execute} = useAxios('/api/infoSystem/userTea')
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

type UserComb = User & { usersubtablestea: UserSubTablesTEA }

const form = ref<UserComb>({
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
  usersubtablestea: {
    title: '',
    department: '',
    position: '',
    office_location: '',
    research_interests: ''
  }
})
const political_affiliationOptions = [
  {label: '群众', value: '群众'},
  {label: '团员', value: '团员'},
  {label: '党员', value: '党员'},
  {label: '预备党员', value: '预备党员'},
  {label: '共青团员', value: '共青团员'},
  {label: '无党派人士', value: '无党派人士'},
  {label: '民主党派', value: '民主党派'},
  {label: '宗教', value: '宗教'},
  {label: '其他', value: '其他'}
]

const handleSizeChange = (val: number) => {
  pageSize.value = val
  execute('/api/infoSystem/userTea', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  execute('/api/infoSystem/userTea', {params: {page: currentPage.value, pageSize: pageSize.value}})
}
onMounted(() => {
  WindowLayoutMainRef.value = document.getElementById('WindowLayoutMain') as HTMLDivElement
  WindowLayoutMain.value = WindowLayoutMainRef.value.offsetHeight
  window.addEventListener('resize', () => {
    WindowLayoutMain.value = WindowLayoutMainRef.value.offsetHeight
  })
})

const ruleForm = reactive({})

const rules = reactive<FormRules>({})
// // 使用watch监听data的变化，并在数据更新时设置tableData
watch(data, (newData) => {
  if (newData && newData.data && newData.data.records) {
    tableData.value = newData.data.records
    currentPage.value = newData.data.current
    pageSize.value = newData.data.pageSize
    total.value = newData.data.total
    console.log(tableData)
  }
}, {
  immediate: true // 初始执行一次
})
const handleEdit = (index: number, row: UserComb) => {
  form.value = row
  dialogVisible.value = true
}
const handleDelete = (index: number, row: UserComb) => {
  console.log(index, row)
}
const handleClose = (done: () => void) => {
  // done()
}
const handleDormitory = (index: number, row: UserComb) => {
  console.log(index, row)
}
const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
      execute('/api/infoSystem/userTea/' + form.value.id, {
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
const handleTeaView = (index, item) => {
  // const el = item[index]
  // console.log(el)
  console.log(index, item)
  // return el === 'title' || el === 'department' || el === 'position' || el === 'office_location' || el === 'research_interests';
}
const handleAvatarSuccess = () => {

}

const beforeAvatarUpload = () => {

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
