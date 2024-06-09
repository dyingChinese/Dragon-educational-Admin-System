<template>
  <section class="min-h-screen p-20 bg-gray-900 overflow-x-hidden">
    <div class="flex flex-col items-center mb-8 gap-4" >
      <div class="relative my-4" @click="openQQ('2775210850')">
        <div class="absolute -inset-2">
          <div
              class="w-28 h-full max-w-sm mx-auto lg:mx-0 opacity-70 blur-lg bg-gradient-to-r from-pink-200 via-pink-500 to-fuchsia-300">
          </div>
        </div>
        <img src="https://q1.qlogo.cn/g?b=qq&nk=2775210850&s=640"
             class="relative object-cover shrink-0 h-28 w-28 z-10 rounded-xl">
      </div>

      <p class="text-2xl font-bold text-white">
        马文龙
      </p>

      <div class="text-gray-400">
        队长
      </div>

    </div>
    <div class="flex flex-row items-center gap-4">
      <div class="mx-auto">
        <div class="relative my-4" @click="openQQ('3108914904')">
          <div class="absolute -inset-2">
            <div
                class="w-28 h-full max-w-sm mx-auto lg:mx-0 opacity-70 blur-lg bg-gradient-to-r from-orange-700 via-gray-200 to-zinc-200">
            </div>
          </div>
          <img src="https://q1.qlogo.cn/g?b=qq&nk=3108914904&s=640"
               class="relative object-cover shrink-0 h-28 w-28 z-10 rounded-xl">
        </div>
        <p class="text-2xl font-bold text-white">
          张振明
        </p>
        <div class="text-gray-400">
          队员
        </div>
      </div>
      <div class="mx-auto">
        <div class="relative my-4" @click="openQQ('2967962017')">
          <div class="absolute -inset-2">
            <div
                class="w-28 h-full max-w-sm mx-auto lg:mx-0 opacity-70 blur-lg bg-gradient-to-r from-cyan-200 via-amber-500 to-cyan-300">
            </div>
          </div>
          <img src="https://q1.qlogo.cn/g?b=qq&nk=2967962017&s=640"
               class="relative object-cover shrink-0 h-28 w-28 z-10 rounded-xl">
        </div>
        <p class="text-2xl font-bold text-white">
          胡锦辉
        </p>
        <div class="text-gray-400">
          队员
        </div>
      </div>
      <div class="mx-auto">
        <div class="relative my-4" @click="openQQ('1643276687')">
          <div class="absolute -inset-2">
            <div
                class="w-28 h-full max-w-sm mx-auto lg:mx-0 opacity-70 blur-lg bg-gradient-to-r from-amber-200 via-amber-500 to-amber-300">
            </div>
          </div>
          <img src="https://q1.qlogo.cn/g?b=qq&nk=1643276687&s=640"
               class="relative object-cover shrink-0 h-28 w-28 z-10 rounded-xl">
        </div>
        <p class="text-2xl font-bold text-white">
          周浩然
        </p>
        <div class="text-gray-400">
          队员
        </div>
      </div>
      <div class="mx-auto">
        <div class="relative my-4" @click="openQQ('2904178430')">
          <div class="absolute -inset-2">
            <div
                class="w-28 h-full max-w-sm mx-auto lg:mx-0 opacity-70 blur-lg bg-gradient-to-r from-gray-200 via-slate-300 to-fuchsia-100">
            </div>
          </div>
          <img src="https://q1.qlogo.cn/g?b=qq&nk=2904178430&s=640"
               class="relative object-cover shrink-0 h-28 w-28 z-10 rounded-xl">
        </div>
        <p class="text-2xl font-bold text-white">
          聂惠懿
        </p>
        <div class="text-gray-400">
          队员
        </div>
      </div>
    </div>
  </section>
</template>


<script setup lang="ts">

import router from "@/router";
const openQQ = (qq:string) => {
  // window.open(`http://wpa.qq.com/msgrd?v=3&uin=${qq}&site=qq&menu=yes`)
  window.open(`tencent://message/?Menu=yes&uin=${qq}&Site=qq&Service=201&sigT=A6F2D2D3}`)

}

</script>
<style scoped>

</style>
