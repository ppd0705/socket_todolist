
var e = function (sel) {
    return document.querySelector(sel)
}

var log = function() {
    console.log.apply(console, arguments)
}

var timeString = function (timestamp) {
    var d = new Date(timestamp * 1000)
    return d.toLocaleString()
}


var ajax = function (method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            // r.response 接收 HTTP BODY 中的数据
            responseCallback(r.response)
        }
    }
    // 数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}





