## 前端运行

> | 项目创建时间 2024年6月9日

### 前端环境

- [x] Node.js 20.10.0
- [x] npm 9.6.3 (pnpm 9.0.5)
- [x] Vue.js 3 组合式API
- [x] Vite 5.0+
- [x] TypeScript 5.2.2

### 前端基础依赖

- axios
- vue-router
- pinia
- element-plus
- TaiwindCSS
- VueUse

### 前端运行

```bash
# 安装依赖
pnpm install # 需要pnpm包管理器,可以通过npm install -g pnpm安装

# 运行
pnpm dev

# 打包
pnpm build
```

## ps:

1. 侧边栏为动静态混合渲染

   侧边栏动态渲染需要后端返回菜单数据, 通过路由守卫动态添加路由

   静态渲染需要在前端配置菜单数据(在每个路由下的JSON文件都视为静态路由读取)

2. 布局采用的是上中下左右布局,通过router的命名式路由使用

3. 项目中使用了pinia作为状态管理, 通过pinia的插件实现了持久化存储

4. 项目中使用了VueUse,axios, 实现了useAxios的封装,提供了响应式hook

5. 项目实现了按钮级权限控制, 通过路由守卫实现实现接口的权限校验,通过自定义指令实现按钮级权限控制,通过hasPermission指令实现按钮级权限控制

6. 部分过于复杂的逻辑, 通过自定义指令实现, 例如: v-permission, v-hasPermission

7. 项目中通过按需引入的方式,减少了打包体积

8. 对部分过于复杂的页面,通过tsx的方式实现,(样式使用CssModule) 例如: 项目中的侧边栏渲染

