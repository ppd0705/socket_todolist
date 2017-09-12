var apiAll = function (id, callback) {
    var path = `/api/todo/all?id=${id}`
    ajax('GET', path, '', callback)
}

var apiAdd = function (form, callback) {
    var path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

var apiDelete = function (id, callback) {
    var path = `/api/todo/delete?id=${id}`
    ajax('GET', path, '', callback)
}

var apiFinish = function (id, callback) {
    var path = `/api/todo/finish?id=${id}`
    ajax('GET', path, '', callback)
}


var todoTemlate = function (todo) {
    var task = todo.task
    var id = todo.id
    var created_time = timeString(todo.created_time)
    var status = todo.status
    var t = `
        <tr class="todo-cell" data-id="${id}">
            <td>${id}</td>
            <td>${task}</td>
            <td>${created_time}</td>
            <td class="todo-status">${status}</td>
            <td><a  class="todo-finish click-a"  data-id="${id}">完成</a>/<a class="todo-delete click-a" data-id="${id}" >删除</a></td>
        </tr>
    `
    return t
}


var insertTodo = function (todo) {
    var todoCell = todoTemlate(todo)
    var todoList = e('#todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var loadsTodos = function () {
    var input = e('#id-input-todo')
    var user_id = input.dataset.id
    apiAll(user_id, function (r) {
        var todos = JSON.parse(r)
        for (var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertTodo(todo)
        }
    })
}

var bindEventAdd = function () {
    var b = e('#id-button-add')
    b.addEventListener('click', function () {
        var input = e('#id-input-todo')
        var task = input.value
        var user_id = input.dataset.id
        var form = {
            task: task,
            user_id: user_id
        }
        apiAdd(form, function (r) {
            var todo = JSON.parse(r)
            insertTodo(todo)
        })
    })
}

var bindEventDelete = function () {
    var todoList = e('#todo-list')
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-delete')) {
            var todoId = self.dataset.id
            apiDelete(todoId, function (r) {
                self.parentElement.parentElement.remove()
            })
        }
    })
}

var bindEventFinish = function () {
    var todoList = e('#todo-list')
    todoList.addEventListener('click', function (event) {
        var self = event.target
        if (self.classList.contains('todo-finish')) {
            var todoId = self.dataset.id
            apiFinish(todoId, function (r) {
                var todoCell = self.parentElement.parentElement
                var status = todoCell.querySelector('.todo-status')
                status.innerHTML = '完成'
            })
        }
    })
}


var bindEvents = function () {
    bindEventAdd()
    bindEventDelete()
    bindEventFinish()

}

var __main = function () {
    bindEvents()
    loadsTodos()
}

__main()