/**
 * Created by SvenWeng on 16/6/29.
 */
$(document).ready(function () {
    // $.get("/testtools/getandroidbaseinfo/")
    $("#getinfo").on('click', function () {
        $("#dad1").html('<div><ul class="list-group" id="index"></ul></div>');
        $("#dad2").html('<div id="infobody"></div>');
        $.get("/testtools/getandroidbaseinfo/", function (data) {
            console.log(data);
            for (var i in data) {
                $("#infobody").after(
                    "<div class='panel panel-info'>" +
                    "<div class='panel-heading' id='"+i+"'>"+changeTitle(i)+"</div>" +
                    "<div class='panel-body'>"+ exportList(data[i])+"</div>" +
                    "</div>"
                );
                $("#index").after(
                    '<li class="list-group-item"><a href="#'+i+'">'+changeTitle(i)+'</a></li>'
                )
            }
        })
    })
});

function exportList(data) {
    var liList = '';
    for (var i=0;i<data.length;i++) {
        liList = liList + "<li class='list-group-item'>"+data[i]+"</li>";
    }
    var rstList = "<ul class='list-group'>" + liList + "</ul>";
    return rstList;
}

function changeTitle(title) {
    switch (title) {
        case 'cpuinfo':
            return "CPU信息";
            break;
        case "meminfo":
            return "内存信息";
            break;
        case "batteryinfo":
            return "电池信息";
            break;
        case "baseinfo":
            return "手机基础信息";
            break;
    }
}