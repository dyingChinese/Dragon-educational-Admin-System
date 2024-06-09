import type {AxiosInstance, AxiosRequestConfig, AxiosResponse} from 'axios'
import {Ref, ShallowRef, ref, shallowRef} from "vue";
import {noop, until} from '@vueuse/shared'
import axios, {AxiosError} from 'axios'
import Qs from "qs"
import router from "@/router/index.ts"
// import router from "@/router/index.ts"

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const axiosInstance: AxiosInstance = axios.create({
    baseURL: import.meta.env.MODE ? '' : "",
    method: "GET",
    timeout: 3000,
    withCredentials: true,
    timeoutErrorMessage: "请求超时",
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCookie('csrftoken'),
        Authorization: localStorage.getItem("AUTH_TOKEN") || ""
    },
    validateStatus: function (status) {
        return status >= 200 && status < 300
    },
    paramsSerializer: function (params) {
        return Qs.stringify(params, {arrayFormat: "comma"})
    },
    transformRequest: [(data, headers) => {
        if (headers["Content-Type"] === "application/x-www-form-urlencoded") {
            return data
        } else if (headers["Content-Type"] === "application/json") {
            try {
                return JSON.stringify(data)
            } catch (e) {
                console.log(e)
            }
        }
    }]
})


//请求拦截器
axiosInstance.interceptors.request.use(_request => {
    if (_request.url === "/login" || _request.url === "/register") {
        return _request
    }
    const token = localStorage.getItem("AUTH_TOKEN")
    if (!token) {
        _request.headers.Authorization = token
    }
    return _request
})

//响应拦截器
axiosInstance.interceptors.response.use(_response => {
    if (_response.status === 400 || _response.data.code === 400401) {
        localStorage.clear()
        router.push("/login")
    }

    return _response
})

export interface UseAxiosReturn<T, R = AxiosResponse<T>, _D = any> {
    /**
     * Axios Response
     */
    response: ShallowRef<R | undefined>

    /**
     * Axios response data
     */
    data: Ref<T | undefined>

    /**
     * Indicates if the request has finished
     */
    isFinished: Ref<boolean>

    /**
     * Indicates if the request is currently loading
     */
    isLoading: Ref<boolean>

    /**
     * Indicates if the request was canceled
     */
    isAborted: Ref<boolean>

    /**
     * Any errors that may have occurred
     */
    error: ShallowRef<unknown | undefined>

    /**
     * Aborts the current request
     */
    abort: (message?: string | undefined) => void

    /**
     * Alias to `abort`
     */
    cancel: (message?: string | undefined) => void

    /**
     * Alias to `isAborted`
     */
    isCanceled: Ref<boolean>
}

export interface StrictUseAxiosReturn<T, R, D> extends UseAxiosReturn<T, R, D> {
    /**
     * Manually call the axios request
     */
    execute: (url?: string | AxiosRequestConfig<D>, config?: AxiosRequestConfig<D>) => Promise<StrictUseAxiosReturn<T, R, D>>
}

export interface EasyUseAxiosReturn<T, R, D> extends UseAxiosReturn<T, R, D> {
    /**
     * Manually call the axios request
     */
    execute: (url: string, config?: AxiosRequestConfig<D>) => Promise<EasyUseAxiosReturn<T, R, D>>
}

export interface UseAxiosOptions<T = any> {
    /**
     * Will automatically run axios request when `useAxios` is used
     *
     */
    immediate?: boolean

    /**
     * Use shallowRef.
     *
     * @default true
     */
    shallow?: boolean

    /**
     * Abort previous request when a new request is made.
     *
     * @default true
     */
    abortPrevious?: boolean

    /**
     * Callback when error is caught.
     */
    onError?: (e: unknown) => void

    /**
     * Callback when success is caught.
     */
    onSuccess?: (data: T) => void

    /**
     * Initial data to use
     */
    initialData?: T

    /**
     * Sets the state to initialState before executing the promise.
     */
    resetOnExecute?: boolean

    /**
     * Callback when request is finished.
     */
    onFinish?: () => void
}

export function useAxios<T = any, R = AxiosResponse<T>, D = any>(url: string, config?: AxiosRequestConfig<D>, options?: UseAxiosOptions): StrictUseAxiosReturn<T, R, D> & Promise<StrictUseAxiosReturn<T, R, D>>
export function useAxios<T = any, R = AxiosResponse<T>, D = any>(url: string, instance?: AxiosInstance, options?: UseAxiosOptions): StrictUseAxiosReturn<T, R, D> & Promise<StrictUseAxiosReturn<T, R, D>>
export function useAxios<T = any, R = AxiosResponse<T>, D = any>(url: string, config: AxiosRequestConfig<D>, instance: AxiosInstance, options?: UseAxiosOptions): StrictUseAxiosReturn<T, R, D> & Promise<StrictUseAxiosReturn<T, R, D>>
export function useAxios<T = any, R = AxiosResponse<T>, D = any>(config?: AxiosRequestConfig<D>): EasyUseAxiosReturn<T, R, D> & Promise<EasyUseAxiosReturn<T, R, D>>
export function useAxios<T = any, R = AxiosResponse<T>, D = any>(instance?: AxiosInstance): EasyUseAxiosReturn<T, R, D> & Promise<EasyUseAxiosReturn<T, R, D>>
export function useAxios<T = any, R = AxiosResponse<T>, D = any>(config?: AxiosRequestConfig<D>, instance?: AxiosInstance): EasyUseAxiosReturn<T, R, D> & Promise<EasyUseAxiosReturn<T, R, D>>
export function useAxios<T = any, R = AxiosResponse<T>, D = any>(...args: any[]): OverallUseAxiosReturn<T, R, D> & Promise<OverallUseAxiosReturn<T, R, D>> {
    const url: string | undefined = typeof args[0] === 'string' ? args[0] : undefined
    const argsPlaceholder = typeof url === 'string' ? 1 : 0
    const defaultOptions: UseAxiosOptions<T> = {
        immediate: !!argsPlaceholder,
        shallow: true,
        abortPrevious: true,
    }
    let defaultConfig: AxiosRequestConfig<D> = {}
    let instance: AxiosInstance = axiosInstance
    let options: UseAxiosOptions<T> = defaultOptions

    const isAxiosInstance = (val: any) => !!val?.request

    if (args.length > 0 + argsPlaceholder) {
        /**
         * 由于 （https://github.com/axios/axios/issues/737） 原因，无法在此处使用“instanceof”
         * 因此，我们正在检查对象上是否有“请求”，以查看它是否是
         * Axios 实例
         */
        if (isAxiosInstance(args[0 + argsPlaceholder]))
            instance = args[0 + argsPlaceholder]
        else
            defaultConfig = args[0 + argsPlaceholder]
    }

    if (args.length > 1 + argsPlaceholder) {
        if (isAxiosInstance(args[1 + argsPlaceholder]))
            instance = args[1 + argsPlaceholder]
    }
    if (
        (args.length === 2 + argsPlaceholder && !isAxiosInstance(args[1 + argsPlaceholder]))
        || args.length === 3 + argsPlaceholder
    )
        options = args[args.length - 1] || defaultOptions

    const {
        initialData,
        shallow,
        onSuccess = noop,
        onError = noop,
        immediate,
        resetOnExecute = false,
    } = options

    const response = shallowRef<AxiosResponse<T>>()
    const data = (shallow ? shallowRef : ref)<T>(initialData!) as Ref<T>
    const isFinished = ref(false)
    const isLoading = ref(false)
    const isAborted = ref(false)
    const error = shallowRef<unknown>()

    let abortController: AbortController = new AbortController()

    const abort = (message?: string) => {
        if (isFinished.value || !isLoading.value)
            return

        abortController.abort(message)
        abortController = new AbortController()
        isAborted.value = true
        isLoading.value = false
        isFinished.value = false
    }

    const loading = (loading: boolean) => {
        isLoading.value = loading
        isFinished.value = !loading
    }

    /**
     * Reset data to initialData
     */
    const resetData = () => {
        if (resetOnExecute)
            data.value = initialData!
    }

    const waitUntilFinished = () =>
        new Promise<OverallUseAxiosReturn<T, R, D>>((resolve, reject) => {
            until(isFinished).toBe(true)
                // eslint-disable-next-line ts/no-use-before-define
                .then(() => error.value ? reject(error.value) : resolve(result))
        })

    const promise = {
        then: (...args) => waitUntilFinished().then(...args),
        catch: (...args) => waitUntilFinished().catch(...args),
    } as Promise<OverallUseAxiosReturn<T, R, D>>

    let executeCounter = 0
    const execute: OverallUseAxiosReturn<T, R, D>['execute'] = (executeUrl: string | AxiosRequestConfig<D> | undefined = url, config: AxiosRequestConfig<D> = {}) => {
        error.value = undefined
        const _url = typeof executeUrl === 'string'
            ? executeUrl
            : url ?? config.url

        if (_url === undefined) {
            error.value = new AxiosError(AxiosError.ERR_INVALID_URL)
            isFinished.value = true
            return promise
        }
        resetData()

        if (options.abortPrevious !== false)
            abort()

        loading(true)

        executeCounter += 1
        const currentExecuteCounter = executeCounter
        isAborted.value = false

        instance(_url, {
            ...defaultConfig, ...typeof executeUrl === 'object' ? executeUrl : config,
            signal: abortController.signal
        })
            .then((r: any) => {
                if (isAborted.value)
                    return
                response.value = r
                const result = r.data
                data.value = result
                onSuccess(result)
            })
            .catch((e: any) => {
                error.value = e
                onError(e)
            })
            .finally(() => {
                options.onFinish?.()
                if (currentExecuteCounter === executeCounter)
                    loading(false)
            })
        return promise
    }

    if (immediate && url)
        (execute as StrictUseAxiosReturn<T, R, D>['execute'])()

    const result = {
        response,
        data,
        error,
        isFinished,
        isLoading,
        cancel: abort,
        isAborted,
        isCanceled: isAborted,
        abort,
        execute,
    } as OverallUseAxiosReturn<T, R, D>

    return {
        ...result,
        ...promise,
    }
}
