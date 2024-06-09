<template>
  <table class="w-full  border schedule-table">
    <caption class="text-3xl mb-5">{{ scheduleConfig.title }}</caption>
    <thead>
    <tr>
      <td class="text-nowrap truncate bg-gray-400 text-blue-50 w-40">时间</td>
      <td class="text-nowrap truncate bg-gray-400 text-blue-50" v-for="item in scheduleConfig.week">{{ item }}</td>
    </tr>
    </thead>
    <tbody>
    <tr v-for="index in 12">
      <td>{{ scheduleConfig.time[index - 1] }}</td>
      <td v-for="day in 7">{{ scheduleConfig.course[day - 1][index - 1] }}</td>
    </tr>
    </tbody>
  </table>
</template>


<script setup lang="ts">
const scheduleConfig = {
  title: '课表',
  time: [
    '08:00 - 09:15',
    '09:20 - 10:05',
    '10:25 - 11:10',
    '11:10 - 12:00',
    '14:00 - 14:45',
    '14:50 - 15:35',
    '15:50 - 16:35',
    '16:40 - 17:25',
    '18:30 - 19:15',
    '19:20 - 20:05',
    '20:10 - 20:55',
    '21:00 - 21:45',
  ],
  week: [
    '周一',
    '周二',
    '周三',
    '周四',
    '周五',
    '周六',
    '周天'
  ],
  course: [
    ['语文', '数学', '英语', '物理', '化学', '自习', '阅读课', '', '社团活动', '班会', '科学实验', ''], // 周一
    ['历史', '地理', '生物', '政治', '体育', '', '音乐', '美术', '信息技术', '第二外语', '电影欣赏', ''], // 周二
    ['语文', '数学', '英语', '物理', '化学', '自习', '', '科学实验', '社团活动', '班会', '阅读课', ''], // 周三
    ['历史', '地理', '生物', '政治', '体育', '', '音乐', '美术', '信息技术', '第二外语', '电影欣赏', ''], // 周四
    ['语文', '数学', '英语', '物理', '化学', '自习', '阅读课', '', '社团活动', '班会', '科学实验', ''], // 周五
    ['历史', '地理', '生物', '政治', '体育', '', '音乐', '美术', '信息技术', '第二外语', '电影欣赏', ''], // 周六
    ['自习', '自习', '自习', '自习', '自习', '', '自习', '自习', '班会', '班会', '班会', '']  // 周日
  ],
}


</script>
<style scoped>
.schedule-table {
  width: 100%;
  border-collapse: collapse;
}

.schedule-table th, .schedule-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

.schedule-table th {
  background-color: #f2f2f2;
}
</style>
