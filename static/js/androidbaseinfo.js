/**
 * Created by SvenWeng on 16/6/29.
 */
$(document).ready(function () {
    // $.get("/testtools/getandroidbaseinfo/")
    $("#getinfo").on('click', function () {
        $("#content").html(
            '<div class="col-md-2" id="dad1"><div><ul class="list-group" id="index"></ul></div></div><div class="col-md-10" id="dad2"><div id="infobody"></div></div>'
        );
        $("#dad1").html('<div><ul class="list-group" id="index"></ul></div>');
        $("#dad2").html('<div id="infobody"></div>');
        $.get("/testtools/getandroidbaseinfo/", function (data) {
            console.log(data);
            for (var i in data) {
                $("#infobody").after(
                    "<div class='panel panel-info'>" +
                    "<div class='panel-heading' id='" + i + "'>" + changeTitle(i) + "</div>" +
                    "<div class='panel-body'>" + exportList(data[i]) + "</div>" +
                    "</div>"
                );
                $("#index").after(
                    '<li class="list-group-item"><a href="#' + i + '">' + changeTitle(i) + '</a></li>'
                )
            }
        })
    });
    $("#getcurpknm").click(function () {getCurPknm();});
    $("#getthirdpknm").click(function () {getThirdPknm();})
});


function exportList(data) {
    var liList = '';
    for (var i = 0; i < data.length; i++) {
        liList = liList + "<li class='list-group-item'>" + data[i] + "</li>";
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

function getCurPknm() {
    $("#texiao").show();
    $.get('/testtools/getcurpknm/', function (data) {
        if (data['status'] == "OK") {
            $("#content").html(
                "<div class='panel panel-info'>" +
                "<div class='panel-heading'>" + data['msg'] + "</div>" +
                "<div class='panel-body'>" + "当前运行的程序包名为: " + data['package_name'] + "<br>当前的Activity为: " + data['activity_name'] + "</div>" +
                "</div>"
            )
        }else if (data['status'] == "ERROR"){
            alert(data['msg'])
        }
    }).success($("#texiao").hide())
}

function getThirdPknm() {
    $("#texiao").show();
    $.get('/testtools/getthirdpknm/', function (data) {
        if (data['status'] == "OK"){
            $("#content").html(
                "<div class='panel panel-info'>" +
                "<div class='panel-heading' id='pknum'></div>" +
                "<div class='panel-body'>" +'<ul class="list-group" id="pknmlist"></ul>'+ "</div>" +
                "</div>"
            );
            for (var i=0;i<data['thirdNames'].length;i++){
                $("#pknmlist").append(
                    '<li class="list-group-item">'+(i+1)+"、 "+data['thirdNames'][i]+'</li>'
                )
            }
            $("#pknum").text("该手机一共安装了  "+data['thirdNames'].length+"  个第三方应用")
        }else if (data['status'] == "ERROR"){
            alert(data['msg'])
        }
    }).success($("#texiao").hide())
}