import {createRouter, createWebHistory, RouteRecordRaw} from "vue-router";
import GlobalLayout from "@/layout/GlobalLayout.vue"
import HomeView from "@/view/HomeView.vue"
import {HomeViewRoutes} from "@/router/components/HomeView/HomeViewRoutes.ts"


const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Home',
        redirect: "/Home",
        component: GlobalLayout,
        children: [
            {
                path: "/HomeView",
                components: {
                    default: HomeView,
                    globalLayoutAside: () => import("@/layout/components/GlobalLayoutAside"),
                    globalLayoutHeader: () => import("@/layout/components/GlobalLayoutHeader.vue"),
                    globalLayoutFooter: () => import("@/layout/components/GlobalLayoutFooter.vue")
                },
                children: HomeViewRoutes
            }
        ]
    },
    {
        path: '/about',
        name: 'About',
        component: () => import('@/view/About/index.vue')
    },
    {
        path: "/login",
        name: "login",
        component: () => import("@/view/Login/login.vue")
    },
    {
        path: "/register",
        name: "register",
        component: () => import("@/view/Login/register.vue")
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
