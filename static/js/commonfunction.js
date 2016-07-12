/**
 * Created by SvenWeng on 16/7/6.
 */
$(document).ready(
    function () {
        $("#install").on('click', function () {
            $("#texiao").show();
            var apkaddress = $("#apkaddress").val();
            var iscovered = $("#iscovered").is(':checked');
            data = {
                'iscovered': iscovered,
                'apkaddress': apkaddress
            };
            $.get('/testtools/apkinstall', data, function (RstData) {
                if (RstData['status'] == "OK") {
                    $("#flash").html(
                        '<div class="alert alert-success alert-dismissible" role="alert">' +
                        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                        '<span aria-hidden="true">&times;</span></button>' + RstData['msg'] + '</div>'
                    );
                } else if (RstData['status'] == "ERROR") {
                    $("#flash").html(
                        '<div class="alert alert-danger alert-dismissible" role="alert">' +
                        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                        '<span aria-hidden="true">&times;</span></button>' + RstData['msg'] + '</div>'
                    );
                }
                $("#texiao").hide()
            })
        })
    }
);


