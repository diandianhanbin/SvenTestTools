/**
 * Created by SvenWeng on 16/6/15.
 */
$(document).ready(function () {
    DOExportBug();
    charts();
});

function getallbug() {
    /**
     * 获取所有Bug的方法
     * 获取之后调用修改样式的方法
     */
    $.getJSON('/testtools/getallbug/', function (data) {
        for (var i = 0; i < data.length; i++) {
            $("#bugbody").append(
                "<tr id='" + i + "'><td>" + data[i]['ID'] + "</td><td>" + data[i]['Terminal'] + "</td><td>" + data[i]['BugTitle'] + "</td><td>" + data[i]['Developer'] + "</td><td>" + changeBugStatusName(data[i]['Status']) + "</td><td><a href='/testtools/bugdetail/" + data[i]['ID'] + "' target='_blank'>" + "明细" + "</a></td></td></tr>"
            );
        }
        setButtonCSS();
        getBugRecordAccordingCondition();
        changeTrColor();
    });
}

function getnewbugelements() {
    /**
     * 新建缺陷时从配置文件读取内容填充
     */
    $.getJSON('/testtools/getnewbugelements', function (data) {
        console.info(data);
        for (var i = 0; i < data['terminal'].length; i++) {
            $("#terminal").append(
                "<option value='" + data['terminal'][i][0] + "'>" + data['terminal'][i][1] + "</option>"
            )
        }
        for (var i = 0; i < data['developer'].length; i++) {
            $("#developer").append(
                "<option value='" + data['developer'][i][0] + "'>" + data['developer'][i][1] + "</option>"
            )
        }
        for (var i = 0; i < data['tester'].length; i++) {
            $("#tester").append(
                "<option value='" + data['tester'][i][0] + "'>" + data['tester'][i][1] + "</option>"
            )
        }
        for (var i = 0; i < data['bugstatus'].length; i++) {
            $("#bugstatus").append(
                "<option value='" + data['bugstatus'][i][0] + "'>" + data['bugstatus'][i][1] + "</option>"
            )
        }
        for (var i = 0; i < data['project'].length; i++) {
            $("#project").append(
                "<option value='" + data['project'][i] + "'>" + data['project'][i] + "</option>"
            );
        }
    })
}

function getOneBug(bugid) {
    /**
     * 获取单个缺陷的内容
     */
    $.getJSON('/testtools/getonebug/' + bugid, function (data) {
        console.info(data);
        $("#bugTitle").val(data['BugTitle']);
        $("#bugDescription").val(data['BugDescription']);
        $("#bugStep").val(data['BugStep']);
        $("#bugstatus").val(data['Status']);
        $("#developer").val(changeDeveloper(data['Developer']));
        $("#tester").val(data['Tester']);
        $("#terminal").val(changeTerminal(data['Terminal']));
        $("#project").val(data['Project'])
    })
}

function setBadge(badgeNum) {
    /**
     * 设置徽章内容
     * @param {int} badgeNum   徽章的数量
     */
    for (var i = 0; i < badgeNum.length; i++) {
        var j = i + 1;
        ele = "status" + j;
        $("#" + ele).text(badgeNum[i])
    }
}

function setButtonCSS() {
    /**
     * 设置bug状态的按钮样式
     */
    $("#button1").addClass("btn btn-danger");
    $("#button2").addClass("btn btn-warning");
    $("#button3").addClass("btn btn-success");
    $("#button4").addClass("btn btn-info");
}


function getBugRecordAccordingCondition() {
    /**
     * 点击按钮获取不同状态的缺陷归集
     */
    $("#statusButton button").on("click", function () {
        // 点击按钮的方法
        // alert($(this).attr("id"))
        var buttonid = $(this).attr("id");
        var project = $("#selectProject").val();
        var data = {
            "BugStatus": buttonid,
            "Project": project
        };
        $.get("/testtools/getbugaccordingtocondition/", data, function (result) {
            $("#bugbody tr").remove();
            for (var i = 0; i < result.length; i++) {
                $("#bugbody").append(
                    "<tr id='" + i + "'><td>" + result[i]['ID'] + "</td><td>" + result[i]['Terminal'] + "</td><td>" + result[i]['BugTitle'] + "</td><td>" + result[i]['Developer'] + "</td><td>" + changeBugStatusName(result[i]['Status']) + "</td><td><a href='/testtools/bugdetail/" + result[i]['ID'] + "' target='_blank'>" + "明细" + "</a></td></td></tr>"
                )
            }
            changeOnlyColor();
        })
    });
    $("#selectProject").change(function () {
        // select变动的方法
        var project = $(this).val();
        var data = {
            "Project": project
        };
        $.get("/testtools/getbugaccordingtocondition/", data, function (result) {
            $("#bugbody tr").remove();
            for (var i = 0; i < result.length; i++) {
                $("#bugbody").append(
                    "<tr id='" + i + "'><td>" + result[i]['ID'] + "</td><td>" + result[i]['Terminal'] + "</td><td>" + result[i]['BugTitle'] + "</td><td>" + result[i]['Developer'] + "</td><td>" + changeBugStatusName(result[i]['Status']) + "</td><td><a href='/testtools/bugdetail/" + result[i]['ID'] + "' target='_blank'>" + "明细" + "</a></td></td></tr>"
                )
            }
            changeTrColor(); // 改变颜色要放在请求数据成功后调用
        });
    });


}

function changeTrColor() {
    /**
     * 根据缺陷状态改变表格中tr标签的背景颜色
     * 获取不同缺陷状态的数字
     */
    // 缺陷状态的计数器
    var weijiejue = 0;
    var yixiufu = 0;
    var yiyanzheng = 0;
    var feiwenti = 0;
    $("#bugbody tr").each(function (index, item) {
        // console.log(index, $(item).children("td:eq(4)").text());
        // console.log($(item).children("td:eq(4)").text());
        var ite = $(item).children("td:eq(4)").text();
        switch (ite) {
            case "未解决":
                $("#" + index).addClass("danger");
                weijiejue = weijiejue + 1;
                break;
            case "已修复":
                $("#" + index).addClass("warning");
                yixiufu = yixiufu + 1;
                break;
            case "已验证":
                $("#" + index).addClass("success");
                yiyanzheng = yiyanzheng + 1;
                break;
            case "非问题":
                $("#" + index).addClass("success");
                feiwenti = feiwenti + 1;
                break;
        }
    });
    $("#button1 span").text(weijiejue);
    $("#button2 span").text(yixiufu);
    $("#button3 span").text(yiyanzheng);
    $("#button4 span").text(feiwenti);
}

function changeOnlyColor() {
    $("#bugbody tr").each(function (index, item) {
        // console.log(index, $(item).children("td:eq(4)").text());
        // console.log($(item).children("td:eq(4)").text());
        var ite = $(item).children("td:eq(4)").text();
        switch (ite) {
            case "未解决":
                $("#" + index).addClass("danger");
                break;
            case "已修复":
                $("#" + index).addClass("warning");
                break;
            case "已验证":
                $("#" + index).addClass("success");
                break;
            case "非问题":
                $("#" + index).addClass("success");
                break;
        }
    });
}

function DOExportBug() {
    $("#DoExport").on('click', function () {
        var exporttype = $('input:radio[name=exportbug]:checked').val();
        bugids = [];
        $("#bugbody tr").each(function (index, item) {
            var ite = $(item).children("td:eq(0)").text();
            bugids.push(ite)
        });
        sendData = {
            "exporttype": exporttype,
            "bugids": bugids
        };
        console.log(sendData);

        $.get('/testtools/exportbug/', sendData, function (rstData) {
            console.log(rstData);
            if (rstData['errstatus'] == 'ERROR') {
                alert(rstData['errmsg'])
            } else if (rstData['errstatus'] == 'OK') {
                // window.open('缺陷导出表.xls')
                alert(rstData['errmsg']);
                $.get('/testtools/downloadbugs/')
            }
        })
    })
}

function charts() {
    $("#charts").on('click', function () {
        var project = $("#selectProject").val();
        $("#body").html("<div id='zhexiantu' style='width:800px;height:600px'></div>");
        sendData = {
            "project": project
        };
        $.get('/testtools/getcharts/', sendData, function (rstData) {
            console.log(rstData);
            var myChart = echarts.init(document.getElementById('zhexiantu'));

            option = {
                title: {
                    text: rstData['projectName']+"——缺陷趋势图"
                },
                tooltip: {
                    trigger: 'axis'
                },
                // legend: {
                //     data: rstData['dates']
                // },
                toolbox: {
                    feature: {
                        saveAsImage: {}
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        boundaryGap: false,
                        data: rstData['dates']
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: rstData['EchartData']
            };

            myChart.setOption(option);
        });


    })
}


function changeBugStatusName(data) {
    /**
     * 缺陷状态码和文案的转换
     * @param {string} data 缺陷的状态码
     * @return {string} 缺陷的文案
     */
    switch (data) {
        case '1':
            return "未解决";
            break;
        case "2":
            return "已修复";
            break;
        case "3":
            return "已验证";
            break;
        case "4":
            return "非问题";
            break;
        default:
            return "状态未知"
    }
}


function changeDeveloper(data) {
    /**
     *开发人员姓名和状态码的转换
     * @param {string} data 开发人员的姓名
     * @return {string} 开发人员姓名对应的状态码
     */
    switch (data) {
        case "徐成勋":
            return "xucx";
            break;
        case "吴道万":
            return "wudw";
            break;
        case "张帅军":
            return "zhangsj";
            break;
        case "罗慧":
            return "luoh";
            break;
        case "李小斌":
            return "lixb";
            break;
        case "阮荣军":
            return "ruanrj";
            break;
        case "熊鹏":
            return "xiongp";
            break;
        case "黄强":
            return "huangq";
            break;
        case "郑总":
            return "zhengzong";
            break;
    }
}


function changeTerminal(data) {
    switch (data) {
        case "Web":
            return "web";
            break;
        case "Android":
            return "android";
            break;
        case "其他":
            return "other";
            break;
        case "IOS":
            return "ios";
            break;
        case "IOS/Android":
            return "ios/android";
            break;
        case "HTML5":
            return "html5";
            break;
        case "后台":
            return "houtai";
            break;
    }
}


