/**
 * Created by SvenWeng on 16/7/8.
 */
$(document).ready(function () {
        changeBtnStatus()
    }
);


function changeBtnStatus() {
    $("#btncheck").click(function () {
        var btnText = $("#btncheck").text();
        if (btnText == "开始监控") {
            $("#btncheck").text('停止监控');
            $("#btncheck").removeClass().addClass('btn btn-danger');
            getCheckBox()
        } else if (btnText == "停止监控") {
            $("#btncheck").text('开始监控');
            $("#btncheck").removeClass().addClass('btn btn-default');
        }
    })
}


function getCheckBox() {
    // 获取选中的checkbox
    var arr = [];
    $("[type='checkbox'][checked]").each(function () {
        arr.push($(this).val())
    });
    var timestamp = new Date().getTime();
    check_data = {
        "timestamp": timestamp,
        "checkedarr": arr
    };
    return check_data
}

