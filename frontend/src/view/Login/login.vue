<template>
  <div class="bg-red-400 h-screen overflow-hidden flex items-center justify-center">
    <div class="bg-white lg:w-5/12 md:6/12 w-10/12 shadow-3xl">
      <div class="bg-gray-800 absolute left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-full p-4 md:p-8">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="#FFF">
          <path
              d="M0 3v18h24v-18h-24zm6.623 7.929l-4.623 5.712v-9.458l4.623 3.746zm-4.141-5.929h19.035l-9.517 7.713-9.518-7.713zm5.694 7.188l3.824 3.099 3.83-3.104 5.612 6.817h-18.779l5.513-6.812zm9.208-1.264l4.616-3.741v9.348l-4.616-5.607z"/>
        </svg>
      </div>
      <el-form class="p-12 md:p-24"
               ref="ruleFormRef"
               style="max-width: 600px"
               :model="ruleForm"

               :rules="rules"
               label-width="auto"
      >

        <el-form-item label="用户名" prop="username" class="flex items-center text-lg mb-6 md:mb-8">
          <el-input v-model="ruleForm.username" type="text" autocomplete="off" prefix-icon="User"/>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
              v-model="ruleForm.password"
              type="password"
              autocomplete="off"
              prefix-icon="Lock"
          />
        </el-form-item>
        <el-form-item>
          <div class="w-full flex items-center justify-center">
            <el-button type="primary" @click="submitForm(ruleFormRef)" size="large">
              Submit
            </el-button>
            <el-button @click="resetForm(ruleFormRef)" size="large">Reset</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>


<script setup lang="ts">
import {reactive, ref} from 'vue'
import type {FormInstance, FormRules} from 'element-plus'
import {userLogin} from "@/api/user";
import {useUserStore} from "@/store/index.ts"
import {useRouter} from "vue-router";

const router = useRouter()

const ruleFormRef = ref<FormInstance>()
const userStore = useUserStore()
const checkAge = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('Please input the age'))
  }
  setTimeout(() => {
    if (!Number.isInteger(value)) {
      callback(new Error('Please input digits'))
    } else {
      if (value < 18) {
        callback(new Error('Age must be greater than 18'))
      } else {
        callback()
      }
    }
  }, 1000)
}

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please input the password'))
  } else {
    callback()
  }
}

const ruleForm = reactive({
  username: '',
  password: '',
})

const rules = reactive<FormRules<typeof ruleForm>>({
  password: [{required: true, message: "Please input the password", trigger: 'blur'}],
  username: [{required: true, message: 'Please input the username', trigger: 'blur'}],
})

const loginEvent = async () => {
  const result = await userLogin({username: ruleForm.username, password: ruleForm.password})
  const {code, data, msg} = result.data
  if (code === 400400) {
    console.log('login failed')
    return
  }

  console.log('login success')
  if (code === 200200 && data) {
    userStore.updateUserInfo({...data!.userInfo, refresh: data!.refresh, access: data.access})
    await router.push('/Home')
  }
}


const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      console.log('submit!')
      loginEvent()
    } else {
      console.log('error submit!')
    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>
<style scoped>

</style>
