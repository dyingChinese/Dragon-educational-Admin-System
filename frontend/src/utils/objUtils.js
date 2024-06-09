export function isObjectNotEmpty(obj) {
    // 检查对象是否既不是null也不是undefined
    if (obj !== null && typeof obj === 'object') {
        // 检查对象是否有属性
        return Object.keys(obj).length > 0;
    }
    // 如果不是对象或者为null，则返回false
    return false;
}
