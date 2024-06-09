import {defineComponent, ref, h} from "vue";
import {ElMenu, ElSubMenu, ElMenuItemGroup, ElMenuItem, ElIcon} from "element-plus";
import AsideRouter from "@/router/components/HomeView/AsideRouter.json"
import styles from "./AsideRouter.module.scss"
import {
    HomeFilled,
    User,
    Setting,
    Document,
    Location,
    OfficeBuilding,
    DataBoard,
    Memo, Avatar
} from "@element-plus/icons-vue"
import {useUserStore} from "@/store/index.ts";
import {useRouter} from "vue-router"
import {hasPermission} from "@/utils/permission.ts";



const iconMap = {
    Memo,
    Setting,
    DataBoard,
    HomeFilled,
    OfficeBuilding,
    User,
    Document,
    Location,
    Avatar
}


const hasRouterAside = (path: string) => {
    const permissionsMap = {
        'user': {group: ['教务管理员'], permission: 'view_user'},
        'dorm': {group: ['宿舍管理员'], permission: 'view_dormitory'},
        'statistics': {group: ['教务管理员'], permission: '', always: true},
        'admin': {group: ['超级管理员'], permission: ''},
        'setting': {group: [], permission: '', always: true},
    };
    const {group, permission, always} = permissionsMap[path.split('/')[1]];
    if (always) return true;
    if (group.length === 0 && !permission) return true;

    return hasPermission(group, permission);
}
const TitleSlot = (item) => {
    if (item.icon) {
        return (<><ElIcon>
            {
                h(iconMap[item.icon])
            }
        </ElIcon><span>{item.name}</span></>)
    }
    return (<span>{item.name}</span>)
}
const ElSubMenuDefaultSlot = (item) => {
    return (
        <ElMenuItemGroup>
            {
                item.children.map(child => (
                    <ElMenuItem key={child.path} index={child.path}>
                        <span>{child.name}</span>
                    </ElMenuItem>
                ))
            }
        </ElMenuItemGroup>
    )
}

export default defineComponent({
    name: "GlobalLayoutAside",
    setup(props, ctx) {

        const activeIndex = useRouter().currentRoute.value.path
        const handleSelect = (key: string, keyPath: string[]) => {
            console.log(key, keyPath)
        }
        return () => (
            <ElMenu active-text-color="#404040" background-color="#f6f7f9" className={styles.elMenuVerticalDemo}
                    default-active={activeIndex} router text-color="#404040" onSelect={handleSelect} unique-opened>
                {
                    AsideRouter.map(item => {
                        if (item.children) {
                            if (item.children.some(child => hasRouterAside(child.path))) {
                                return (
                                    <ElSubMenu key={item.path} index={item.path}>
                                        {{
                                            title: () => TitleSlot(item),
                                            default: () => ElSubMenuDefaultSlot(item)
                                        }}
                                    </ElSubMenu>
                                )
                            }
                            return <></>
                        }
                        return (<ElMenuItem key={item.path} index={item.path}>
                            {
                                item.icon ? <ElIcon>
                                    {h(iconMap[item.icon])}
                                </ElIcon> : <></>
                            }
                            <span>{item.name}</span>
                        </ElMenuItem>)

                    })
                }
            </ElMenu>
        );
    },
});

