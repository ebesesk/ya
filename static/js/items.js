var updateforms = document.querySelectorAll(".container-fluid.update")
// console.log(updateforms)
var delForms = document.querySelectorAll(".container-fluid.delete")


function resetForm(e) {
    var index = e.target.id.replace('form', '');
    var msg = document.querySelector('.msg'+index);
    msg.innerHTML = ''
}

function submitUpdateForm(e) {
    e.preventDefault();
    var queryString = $('#'+e.target.id).serialize();
    var url = '/videos/update?' + queryString
    fetch(url)
        .then((response) => response.json())
        .then(function(data) {
            var index = e.target.id.replace('form', '');
            var msgTag = document.querySelector('.msg'+index);
            msgTag.innerHTML = data.result;
        })
}

function submitDelForm(e) {
    e.preventDefault();
    var queryString = $('#'+e.target.id).serialize();
    var url = '/videos/delete?' + queryString;
    // console.log(url)
    fetch(url)
        .then(response => response.json())
        .then(function(data) {
            var index = e.target.id.replace('delForm', '');
            var msgTag = document.querySelector('.msg' + index);
            console.log(data.del[0]+'<br>')
            // msgTag.innerHTML = 'dddd'
            msg = 'deleted<br>' + data.del[0] + '<br>' + data.del[1] + '<br>' + data.del[2] + '<br>' + data.del[3]
            // console.log(msg)
            msgTag.innerHTML = msg
        })

}


for (var i = 0; i < updateforms.length; i++) {
    // console.log(updateforms[i], '<=====', i)
    updateforms[i].addEventListener("reset", resetForm);
    updateforms[i].addEventListener("submit", submitUpdateForm);
}

for (var i = 0; i < delForms.length; i++) {
    delForms[i].addEventListener("submit", submitDelForm);
}