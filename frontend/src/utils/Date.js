export function formatDate(isoDateString) {
    // 创建一个新的Date对象
    var date = new Date(isoDateString);

    // 获取年、月、日、小时、分钟、秒
    var year = date.getFullYear();
    var month = (date.getMonth() + 1).toString().padStart(2, '0'); // 月份是从0开始的
    var day = date.getDate().toString().padStart(2, '0');
    var hours = date.getHours().toString().padStart(2, '0');
    var minutes = date.getMinutes().toString().padStart(2, '0');
    var seconds = date.getSeconds().toString().padStart(2, '0');

    // 格式化日期和时间
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}
