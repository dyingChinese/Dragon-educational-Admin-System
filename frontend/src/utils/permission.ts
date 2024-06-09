import {UserGroup} from "@/types/global.ts";
import {useUserStore} from "@/store";

export const hasPermission = (groupArr: UserGroup[], isPermission?: string = null) => {
    const userStore = useUserStore()
    const groups = userStore.getGroups();
    const permissions = userStore.getPermissions();
    const isAdmin = groups.some(group => group.name === '超级管理员');

    if (isAdmin) return true;

    const hasRequiredGroup = groupArr.some(group => groups.some(userGroup => userGroup.name === group));
    const hasRequiredPermission = isPermission ? permissions.some(permission => permission.codename === isPermission) : false;
    return hasRequiredGroup || hasRequiredPermission;
}
