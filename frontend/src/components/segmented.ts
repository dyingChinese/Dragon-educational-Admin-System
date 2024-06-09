import {
    isNumber,
    isString,
} from '@element-plus/utils/util'
// import {
//     buildProps,
//     definePropType
// } from '@vue'

import {useAriaProps, useSizeProp} from 'element-plus'
import {CHANGE_EVENT, UPDATE_MODEL_EVENT} from 'element-plus'

import type {Option} from './types'
import type {ExtractPropTypes} from 'vue'
import type Segmented from './Segmented.vue'
import {buildProps, definePropType} from "element-plus/es/utils";

export function debugWarn(err: Error): void
export function debugWarn(scope: string, message: string): void
export function debugWarn(scope: string | Error, message?: string): void {
    if (import.meta.env.MODE !== 'production') {
        const error: Error = isString(scope)
            ? new ElementPlusError(`[${scope}] ${message}`)
            : scope
        // eslint-disable-next-line no-console
        console.warn(error)
    }
}

export const segmentedProps = buildProps({
    /**
     * @description options of segmented
     */
    options: {
        type: definePropType<Option[]>(Array),
        default: () => [],
    },
    /**
     * @description binding value
     */
    modelValue: {
        type: [String, Number, Boolean],
        default: undefined,
    },
    /**
     * @description fit width of parent content
     */
    block: Boolean,
    /**
     * @description size of component
     */
    size: useSizeProp,
    /**
     * @description whether segmented is disabled
     */
    disabled: Boolean,
    /**
     * @description whether to trigger form validation
     */
    validateEvent: {
        type: Boolean,
        default: true,
    },
    /**
     * @description native input id
     */
    id: String,
    /**
     * @description native `name` attribute
     */
    name: String,
    ...useAriaProps(['ariaLabel']),
})

export type SegmentedProps = ExtractPropTypes<typeof segmentedProps>

export const segmentedEmits = {
    [UPDATE_MODEL_EVENT]: (val: any) => isString(val) || isNumber(val),
    [CHANGE_EVENT]: (val: any) => isString(val) || isNumber(val),
}
export type SegmentedEmits = typeof segmentedEmits

export type SegmentedInstance = InstanceType<typeof Segmented>
