import {axiosInstance} from "@/api";


export const userLogin = (params: { username: string, password: string }) => {
    return axiosInstance({
        url: '/api/login',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: params
    })
}
