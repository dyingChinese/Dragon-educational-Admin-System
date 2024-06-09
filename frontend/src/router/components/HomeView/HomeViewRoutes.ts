import {RouteRecordRaw} from "vue-router"


export const HomeViewRoutes: Array<RouteRecordRaw> = [
    {
        path: "/Home",
        name: "Home",
        component: () => import("@/view/HomeView/index.vue")
    },
    {
        path: "/schedule",
        name: "schedule",
        component: () => import("@/view/Schedule/index.vue")
    },
    {
        path: "/user",
        name: "user",
        redirect: "/user/student",
        children: [
            {
                path: "student",
                name: "student",
                component: () => import("@/view/InformationSystem/StuInfoSystem/index.vue")
            },
            {
                path: "teacher",
                name: "teacher",
                component: () => import("@/view/InformationSystem/TeacherSystem/index.vue")
            },
            {
                path: "course",
                name: "course",
                component: () => import("@/view/InformationSystem/CourseSystem/index.vue")
            },
            {
                path: "college",
                name: "college",
                component: () => import("@/view/InformationSystem/CollegeSystem/index.vue")
            },
            {
                path: "class",
                name: "class",
                component: () => import("@/view/InformationSystem/ClassSystem/index.vue")
            }
        ]
    },
    {
        path: "/dorm",
        name: "dorm",
        redirect: "/dorm/building",
        children: [
            {
                path: "building",
                name: "building",
                component: () => import("@/view/InformationSystem/DormSystem/BuildingSystem/index.vue")
            },
            {
                path: "room",
                name: "room",
                component: () => import("@/view/InformationSystem/DormSystem/RoomSystem/index.vue")
            }
        ]
    },
    {
        path:"/admin",
        name:"admin",
        redirect:"/admin/role",
        children:[
            {
                path:"role",
                name:"role",
                component:()=>import("@/view/Admin/Role/index.vue")
            },
            {
                path:"info",
                name:"info",
                component:()=>import("@/view/Admin/User/index.vue")
            }
        ]
    }
]
