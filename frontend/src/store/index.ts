import {defineStore} from "pinia"
import {ref} from "vue"
import {User} from "@/types/global.ts"

export const useHomeASideStore = defineStore("useHomeASideStore", {

    state: () => ({activeIndex: "/"}),
    actions: {}
})


export const useUserStore = defineStore("useUserStore", () => {
        const state = ref<User | { refresh, access }>({
            id: -1,
            groups: [],
            user_permissions: [],
            last_login: "",
            is_superuser: false,
            first_name: "",
            last_name: "",
            is_staff: false,
            is_active: false,
            date_joined: "",
            username: "",
            role: "",
            status: -1,
            nickname: "",
            avatar: "",
            mobile: "",
            email: "",
            gender: "",
            description: "",
            create_time: "",
            official_id: "",
            last_update_time: "",
            political_affiliation: "",
            ethnicity: "",
            dormitory: {},
            access: '',
            refresh: ''
        })
        const updateUserInfo = (params: User) => {
            const data = {...state.value, ...params}
            state.value = data
            return data
        }

        const updatePoint = (index: string, newVal) => {
            state.value[index] = newVal;
        }

        const getRole = () => {
            return state.value.role
        }
        const getGroups = () => {
            return state.value.groups
        }

        const getPermissions = () => {
            return state.value.user_permissions
        }

        const getDormitory = () => {
            return state.value.dormitory;
        }

        const getSimplyUserInfo = () => {
            return {
                id: state.value.id,
                username: state.value.username,
                nickname: state.value.nickname,
                avatar: state.value.avatar,
                mobile: state.value.mobile,
                email: state.value.email,
                gender: state.value.gender
            }
        }
        return {
            state, updateUserInfo, updatePoint, getRole, getGroups, getPermissions, getDormitory, getSimplyUserInfo
        }
    }, {
        persist: true
    }
)
