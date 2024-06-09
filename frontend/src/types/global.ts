export interface UserGroup {
    id: number;
    name: string;
}

export interface UserPermission {
    id: number;
    name: string;
    codename: string;
}

export interface User {
    id: number;
    official_id: string;
    username: string;
    role?: number;
    status: number;
    nickname: string;
    avatar?: string;
    mobile?: string;
    email?: string;
    gender?: string;
    description?: string;
    create_time: string;
    last_update_time?: string;
    political_affiliation?: string;
    ethnicity?: string;
    groups?: UserGroup[];
    permissions?: UserPermission[];
    dormitory?: Dormitory;
    last_login?: string;
    is_superuser?: boolean;
    is_staff?: boolean;
    is_active?: boolean;
    date_joined?: string;
}

export interface Dormitory {
    id: number;
    user_name: string;
    room_number: string;
    capacity: number;
    gender_allowed: string;
    address: string;
    emergency_contact?: string;
    emergency_contact_phone?: string;
    health?: string;
    warden?: number;
    warden_name?: string;
}

export interface UserSubTableSTU {
    id: number; // 由于是一对一关系，这里假设你有一个User接口
    institute: string; // 学院名称
    grade: string; // 年级
    domain: string; // 专业领域
    aclass: string; // 班级
    duration: number; // 学制
    enrollment_date: string | null; // 入学年份
    graduation_time: string | null; // 毕业年份
    grade_point: number | null; // 学分绩点
    graduation: string | null; // 毕业去向
}


export interface UserSubTablesTEA {
    id: number; // 由于是一对一关系，这里假设你有一个User接口
    title: string | null; // 教师职称
    department: string | null; // 所属部门
    position: string | null; // 职位
    phone_number: string | null; // 联系电话
    email: string | null; // 电子邮件地址
    office_location: string | null; // 办公室位置
    research_interests: string | null; // 研究兴趣
}

export interface Aclass {
    id: number;
    institute: string,
    domain: string,
    grade: string,
    aclass: string,
    count: number,
    average: number,
    duration: number
}

export interface Collage {

    institute: string,
    domainCount: number,
    stuNum: number,
    id: number

}

export interface Course {
    id: number;
    name: string;
    description: string;
    credits: number;
    location: string;
    time: string;
    type: string;
    created_at: string;
    official_code: string;
    teacher: [],
    students: []
}

export interface DormitoryStatic {
    capacity: number,
    gender_allowed: string,
    health: string,
    capacityNum: number,
    genderNum: number,
    healthNum: number,
    healthStatusArray: []
    id: number
}
