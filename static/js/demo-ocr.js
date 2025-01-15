// 页面加载时，执行
var targetFile = null;
window.onload = function () {
    $('#detect_img').attr("width", "");
    $('#detect_img').attr("height", "");
}

$("#rapid_ocr").on('change', function () {
    targetFile = document.getElementById("rapid_ocr").files[0];
    requestOCR();
});

$("html").on("dragover", function (event) {
    event.preventDefault();
    event.stopPropagation();
    $(this).addClass('dragging');
});

$("html").on("dragleave", function (event) {
    event.preventDefault();
    event.stopPropagation();
    $(this).removeClass('dragging');
});

$("html").on("drop", function (event) {
    event.preventDefault();
    event.stopPropagation();
    let trans = event.originalEvent.dataTransfer;
    handleData(trans);
});

$('html').on('paste', function (e) {
    let trans = e.originalEvent.clipboardData;
    handleData(trans);
});

function handleData(trans) {
    if (trans.items) {
        for (let i = 0; i < trans.items.length; i++) {
            // If dropped items aren't files, reject them
            if (trans.items[i].kind === 'file') {
                targetFile = trans.items[i].getAsFile();
                console.log(`handleData: items[${i}].name = ${targetFile.name}`);
                requestOCR();
                return;
            }
        }
    } else {
        // Use DataTransfer interface to access the file(s)
        for (let i = 0; i < trans.files.length; i++) {
            targetFile = trans.files[i];
            console.log(`handleData: files[${i}].name = ${targetFile.name}`);
            requestOCR();
            return;
        }
    }
}

function requestOCR() {
    if (!targetFile) {
        return;
    }
// 判断图像格式是否匹配
    let imageName = targetFile.name;
    let index = imageName.lastIndexOf('.');
    let extName = imageName.substr(index + 1);
    let imgArr = ['jpg', 'bmp', 'png', 'jpeg'];
    if (!(imgArr.includes(extName.toLocaleLowerCase()))) {
        alert("图像文件格式不支持！");
        return;
    }
// 判断图像大小是否符合
    let imageSize = targetFile.size / 1024 / 1024;
    if (imageSize >= 3) {
        alert("图像大小超过3M！");
        return;
    }

    var reader = new FileReader();
    reader.onload = function (e) {
        var upload_data = {"file": reader.result};
        $.ajax(
            {
                url: "/demo/ocr",
                type: "POST",
                data: JSON.stringify(upload_data),
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',

                beforeSend: function () {
                    $("#detect_img").attr('src', reader.result);
                    $("#detect_img").attr("width", "95%");
                    $("#detect_img").attr("height", "100%");

                    $("#wrapper").show();
                    $("#locTable").hide();
                    $("#rec_res").html("文本识别结果");
                },

                success: function (data) {
                    $("#wrapper").hide();
                    if (data) {
                        if (data['image']) {
                            $("#detect_img").attr('src', 'data:image/jpeg;base64,' + data['image']);
                            $('#detect_img').show();
                        }

                        if (data["total_elapse"]) {
                            document.getElementById("rec_res").textContent = "文 本 识 别 结 果(识别时间：" + String(data["total_elapse"]) + "s)";
                            $("#rec_res").show();
                        }

                        if (data["rec_res"]) {
                            var rec_res = JSON.parse(data["rec_res"]);

                            if (data['elapse_part']) {
                                var elapse_list = data['elapse_part'].split(',');
                            } else {
                                var elapse_list = [0, 0, 0];
                            }
                            var dataHtml = "";
                            dataHtml += "<tr>" +
                                '<th align="center">文本检测时间:<br>' + elapse_list[0] + '秒</th>' +
                                '<th align="center">方向识别时间:<br>' + elapse_list[1] + '秒</th>' +
                                '<th align="center">文字识别时间:<br>' + elapse_list[2] + '秒</th>' +
                                "</tr>";
                            dataHtml += "<tr>" +
                                '<th bgcolor="#C0C0C0" align="center">序号</th>' +
                                '<th bgcolor="#C0C0C0" align="center">识别结果</th>' +
                                '<th bgcolor="#C0C0C0" align="center">置信度</th>' +
                                "</tr>"
                            for (let i = 0; i < rec_res.length; i++) {
                                const element = rec_res[i];
                                let num = element[0];
                                let rec_result = element[1];
                                let score = Number(element[2]);
                                score = score.toFixed(4);

                                dataHtml += "<tr>" +
                                    '<td align="center">' + num + '</td>' +
                                    '<td align="center">' + rec_result + '</td>' +
                                    '<td align="center">' + score + '</td>' +
                                    "</tr>"
                            }
                            document.getElementById("locTable").innerHTML = dataHtml;
                            $("#locTable").show();
                        }
                    }


                }
            }
        );
    }
    reader.readAsDataURL(targetFile)
}