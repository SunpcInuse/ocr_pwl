document.getElementById('submit').addEventListener('click', function () {
    const files = document.getElementById('fileInput').files;
    if (files.length === 0) {
        alert('请选择文件！');
        return;
    }
    const formData = new FormData();
    // const positionX = document.getElementById('positionX').value;
    // const positionY = document.getElementById('positionY').value;
    const filenamePrefix = document.getElementById('filenamePrefix').value;
    if (filenamePrefix.length === 0) {
        alert('请输入文件名称！');
        return;
    }
    // 获取<select>元素
    // var selectElement = document.getElementById('PaperSize');

// 获取选中的<option>的值
    // var selectedValue = selectElement.value;
    // console.info(selectedValue);
    // console.log("X偏移", positionX);
    // console.log("Y偏移", positionY);
    // console.log("文件名称标识", filenamePrefix);
    // formData.append('positionX', positionX);
    // formData.append('positionY', positionY);
    formData.append('filenamePrefix', filenamePrefix);
    // formData.append('selectedValue', selectedValue);

    for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
        // console.log(files[i])
    }
    // console.log(formData);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/demo/upload_layout', true);
    // alert('文件上传成功,正在识别！');
     $('#loading').show();
    xhr.onload = function () {
        if (xhr.status === 200) {

            downloadDOCX(filenamePrefix);
        } else {
            alert('文件上传失败！,请检查文件及文件格式');
            $('#loading').hide();
        }
    };
    xhr.send(formData);
});


// fileInput
// document.getElementById('uploadBtn').addEventListener('click', function() {
//     document.getElementById('imageUpload').click();
// });


function iG(event) {
    console.log("执行图像画布");
    gallery.innerHTML = ''; // 清空预览区域

    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!file.type.match('image.*')) {
            continue; // 不是图像文件，跳过
        }

        const reader = new FileReader();
        reader.onload = (function (file) {
            return function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.title = file.name;
                gallery.appendChild(img); // 显示预览图像
            };
        })(file);

        reader.readAsDataURL(file);
    }
}


function downloadDOCX(filenamePrefix) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/demo/download_layout?filename=' + filenamePrefix, true);
    xhr.responseType = 'blob';


    xhr.onload = function () {
        if (xhr.status === 200) {
            $('#loading').hide();

            const blob = xhr.response;
            const url = window.URL.createObjectURL(blob);

            // 创建一个临时的链接用于下载word
            const a = document.createElement('a');
            a.href = url;
            a.download = filenamePrefix + '.docx';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);

            // 显示PDF
            displayDOCX(blob);
            // 释放URL对象
            window.URL.revokeObjectURL(url);
        } else {
            alert('下载文件失败！');
        }
    };
    xhr.send();
}

//function displayDOCX(blob) {
//    const url = window.URL.createObjectURL(blob);
//    const docxViewer = document.getElementById('docxViewer');
//}

function displayDOCX(blob) {
    // 如果Word文件已下载并且需要展示在iframe中
    const docxViewer = document.getElementById('docxViewer');

    // 使用Mammoth.js处理并显示Word内容
    const reader = new FileReader();
    reader.onload = function (e) {
        var arrayBuffer = e.target.result;

        mammoth.extractRawText({ arrayBuffer: arrayBuffer })
            .then(function (result) {
                // 将解析后的文本放入iframe
                docxViewer.srcdoc = result.value;
            })
            .catch(function (err) {
                console.error('Error processing Word file:', err);
            });
    };
    reader.readAsArrayBuffer(blob);
}

document.getElementById('fileInput').addEventListener('change', function (event) {
    const gallery = document.getElementById('imageGallery');
    gallery.innerHTML = ''; // 清空预览区域

    const files = event.target.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!file.type.match('image.*')) {
            continue; // 不是图像文件，跳过
        }

        const reader = new FileReader();
        reader.onload = (function (file) {
            return function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.title = file.name;
                gallery.appendChild(img); // 显示预览图像
            };
        })(file);

        reader.readAsDataURL(file);
    }
});
