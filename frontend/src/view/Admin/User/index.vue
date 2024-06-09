<template>
  <div class="flex flex-row items-start gap-4">
    <el-segmented v-model="value" :options="options" size="large" @change="handleChange"/>
  </div>
  <el-table :data="userData" show-header border stripe class="my-5"
            :header-cell-style="{ backgroundColor: '#3c507a', color: '#e8ebef', fontSize: '14px', textAlign: 'center'}">
    <el-table-column prop="id" label="id" width="70"/>
    <el-table-column prop="nickname" label="昵称"/>
    <el-table-column prop="username" label="姓名" width="100"/>
    <el-table-column prop="gender" label="性别" width="60">
      <template #default="scope">
        <span v-if="scope.row.gender==='M'" style="color: var(--el-table-text-color);">男</span>
        <span v-else style="color: var(--el-table-text-color);">女</span>
      </template>
    </el-table-column>
    <el-table-column prop="email" label="邮件"/>
    <el-table-column prop="last_login" label="上次登录" :formatter="row => formatDate(row.last_login)"/>
    <el-table-column prop="mobile" label="手机号"/>
    <el-table-column prop="official_id" label="身份证号"/>
    <el-table-column prop="ethnicity" label="民族" width="70"/>
    <el-table-column prop="political_affiliation" label="政治面貌"/>
    <el-table-column prop="status" label="状态">
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
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)" disabled>
          Edit
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>


<script setup lang="ts">
import {ref, watch} from 'vue'
import {useAxios} from "@/api";
import {formatDate} from "@/utils/Date";

const value = ref('全部')
const options = ref(['全部'])
const {data, isLoading, execute} = useAxios('/api/infoSystem/admin/roleName')
const {
  data: userData,
  isLoading: userLoading,
  execute: userExecute
} = useAxios('/api/infoSystem/user')


// 获取全部角色数据
watch(data, (newData) => {
  if (newData && newData.data) {
    options.value = ['全部', ...newData.data.map(item => item.name)]
  }
}, {
  immediate: true // 初始执行一次
})

// 获取当前角色用户数据
watch(userData, (newData) => {
  if (newData && newData.data&&newData.data.records) {
    userData.value = newData.data.records
  }
}, {
  immediate: true // 初始执行一次
})

const handleChange = (value) => {
  userExecute('/api/infoSystem/admin/role', {
    params: {
      name: value === '全部' ? '全部' : value
    }
  })
}

</script>
<style scoped>

</style>
