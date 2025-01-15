document.getElementById('uploadButton').addEventListener('click', function() {
    const fileName = document.getElementById('fileName').value;
    const fileInput = document.getElementById('fileUpload');
    const file = fileInput.files[0];

    if (!file) {
        alert('请上传文件！');
        return;
    }

    // 创建FormData对象以便上传文件
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', fileName);

    // 使用fetch上传文件并获取识别结果
    fetch('/upload-and-recognize', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 显示图像
            document.getElementById('resultImage').src = data.imageUrl;
        } else {
            alert('识别失败');
        }
    })
    .catch(error => {
        console.error('上传失败', error);
    });
});
