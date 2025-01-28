$('#submitFiles').on('click', function () {
    const file1 = $('#file1')[0].files[0];
    const file2 = $('#file2')[0].files[0];

    console.log("file 1 :",file1);
    console.log("FIle 2 :",file2);

    if (!file1 || !file2) {
        alert('Please select both files.');
        return;
    }

    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);

    // AJAX call to upload files and trigger download
    $.ajax({
    url: 'http://127.0.0.1:5000/upload',
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    // xhrFields: {
    //     responseType: 'blob'  // Ensure the response is treated as a binary file
    // },
    success: function(response) {
            if (response.status) {
                console.log("download url :",response.download_url);
                // If the response is successful, handle the file download
                var downloadLink = document.createElement('a');
                console.log("downloadlink :",downloadLink);
                downloadLink.href = response.download_url;  // URL to the file
                downloadLink.download = response.download_name; // Suggested filename for download
                downloadLink.click();  // Trigger the download
            } else {
                // Handle failure scenario (e.g., show an error message)
                alert(response.message);
            }
    },
    error: function(xhr, status, error) {
            // Handle error scenario
            alert('An error occurred: ' + error);
    }

});
});