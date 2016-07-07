/**
 * Created by SvenWeng on 16/7/6.
 */
$(document).ready(
    function () {
        $("#install").on('click', function () {
            var apkaddress = $("#apkaddress").val();
            var iscovered = $("#iscovered").is(':checked');
            data = {
                'iscovered': iscovered,
                'apkaddress': apkaddress
            };
            $("#jindutiao").html(
              '<div class="progress" id="jindutiao"><div id="jindu" class="progress-bar progress-bar-info progress-bar-striped" role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100" style="width: 5%"><span class="sr-only">20% Complete</span></div></div>'
            );
            setTimeout(function(){$("#jindu").css("width", "30%");},2000);
            setTimeout(function(){$("#jindu").css("width", "70%");},4000);
            $.get('/testtools/apkinstall', data, function (RstData) {
                if (RstData['status'] == "OK") {
                    $("#flash").html(
                        '<div class="alert alert-success alert-dismissible" role="alert">' +
                        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                        '<span aria-hidden="true">&times;</span></button>' + RstData['msg'] + '</div>'
                    );
                    $("#jindu").css("width", "100%")
                } else if (RstData['status'] == "ERROR") {
                    $("#flash").html(
                        '<div class="alert alert-danger alert-dismissible" role="alert">' +
                        '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                        '<span aria-hidden="true">&times;</span></button>' + RstData['msg'] + '</div>'
                    );
                    $("#jindu").css("width", "100%")
                }
            })
        })
    }
);


