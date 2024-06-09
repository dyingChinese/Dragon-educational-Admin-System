<template>

  <div class="w-full flex flex-row">
    <table class="table flex-1" v-loading="isLoading">
      <thead class="table_header">
      <tr class="table__header_row">
        <th class="table_cell table_header_cell">id</th>
        <th class="table_cell table_header_cell">角色名</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in tableData" :key="item.id" @click="handleRoleRequset(item.name)">
        <td class="table_cell table_body_cell">{{ item.id }}</td>
        <td class="table_cell table_body_cell">{{ item.name }}</td>
      </tr>
      </tbody>
    </table>

    <el-transfer :titles="['其他权限', '已有权限']" v-model="permissionValue" :data="permissionData"
                 :props="{key:'id',label:'name'}" class="transfer flex-1">
      <template #left-footer>
        <el-button class="transfer-footer" type="info" size="small">添加</el-button>
      </template>
    </el-transfer>

  </div>

  <el-table :data="permissionData" show-header border stripe class="my-5" :header-cell-style="{ backgroundColor: '#3c507a', color: '#e8ebef', fontSize: '14px', textAlign: 'center'}">
    <el-table-column prop="id" label="ID" width="70"/>
    <el-table-column prop="name" label="名称"/>
    <el-table-column prop="codename" label="代码"/>
    <el-table-column prop="content_type_id" label="对应类型id"/>
  </el-table>
</template>


<script setup lang="ts">
import {useAxios} from "@/api";
import {ref, watch} from "vue";


const permissionValue = ref([])
const tableData = ref([])
const permissionData = ref([])


const {data, isLoading} = useAxios('/api/infoSystem/admin/roleName')
const {
  data: permissionTotalData,
  isLoading: permissionTotalDataLoading,
  execute: executeTotal
} = useAxios('/api/infoSystem/admin/permission')

const {
  data: permissionCurData,
  isLoading: permissionCurDataLoading,
  execute: executeCur
} = useAxios('/api/infoSystem/admin/permission', {},)

// 获取全部角色数据
watch(data, (newData) => {
  if (newData && newData.data) {
    tableData.value = newData.data
    console.log("触发了 tableData", tableData.value)
  }
}, {
  immediate: true // 初始执行一次
})


// 获取全部权限数据
watch(permissionTotalData, (newData) => {
  if (newData && newData.data) {
    permissionData.value = newData.data
  }
}, {
  immediate: true // 初始执行一次
})

// 获取当前权限数据
watch(permissionCurData, (newData) => {
  if (newData && newData.data) {
    permissionValue.value = newData.data.map((item: any) => item.id)
  }
}, {
  immediate: true // 初始执行一次
})


const handleRoleRequset = (name: number) => {
  executeCur('/api/infoSystem/admin/permission', {
    params: {
      group: name
    }
  })
}

</script>
<style scoped>
.table {
  border-collapse: collapse;
  padding: 20px;
  border-spacing: 0;
  border: 1px solid #dfe1e5;
  border-radius: 4px;
  background: #fff;
  cursor: default;
  margin-top: 20px;

  &:focus {
    outline: none;
    cursor: none;
  }
}

.transfer {
  padding: 20px;
  cursor: default;
  border-spacing: 0;
  border-radius: 4px;
}

.table__header_row {
  padding: 20px;
  background: #3c507a;
  color: #dddddd;
}

.table_cell {
  padding: 20px;
  border: 1px solid #dfe1e5;
}

:deep(.table_el_header_row) {
  background: #000000;
}
</style>
