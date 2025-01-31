$(document).ready(function () {

$("#slider").on("input", function () {
    $("#sliderValue").text($(this).val()); // Update value next to slider
});

$('#submitFiles').on('click', function () {
    const file1 = $('#file1')[0].files[0];
    const file2 = $('#file2')[0].files[0];
    const file3 = $('#file3')[0].files[0];  // Optional file3
    const file4 = $('#file4')[0].files[0];  // Optional file4

    console.log("file 1 :",file1);
    console.log("FIle 2 :",file2);
    const sliderValue = $('#slider').val(); // Get slider value

    console.log("Selected Slider Value:", sliderValue); // Debugging

    if (!file1 || !file2) {
        alert('Please select both files.');
        return;
    }

    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);
    formData.append('sliderValue', sliderValue);

    if (file3) {
        formData.append('file3', file3);
    }

    if (file4) {
        formData.append('file4', file4);
    }


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
                console.log("Download URL:", response.download_url);

                // If the response is successful, handle the file download
                const downloadLink = document.createElement('a');
                downloadLink.href = response.download_url;  // URL to the file
                downloadLink.download = response.download_name; // Suggested filename for download
                document.body.appendChild(downloadLink);
                downloadLink.click();  // Trigger the download
                document.body.removeChild(downloadLink);  // Clean up
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



$('#submitFiles2').on('click', function () {
    const file1 = $('#file1')[0].files[0];
    const file2 = $('#file2')[0].files[0];
    const file3 = $('#file3')[0].files[0];  // Optional file3
    const file4 = $('#file4')[0].files[0];  // Optional file4

    console.log("file 1 :",file1);
    console.log("FIle 2 :",file2);
    const sliderValue = $('#slider').val(); // Get slider value

    console.log("Selected Slider Value:", sliderValue); // Debugging

    // if (!file1 || !file2) {
    //     alert('Please select both files.');
    //     return;
    // }

    const formData = new FormData();
    // formData.append('file1', file1);
    // formData.append('file2', file2);
    formData.append('sliderValue', sliderValue);

    if (file1) {
        formData.append('file1', file1);
    }

    if (file2) {
        formData.append('file2', file2);
    }

    if (file3) {
        formData.append('file3', file3);
    }

    if (file4) {
        formData.append('file4', file4);
    }


    // AJAX call to upload files and trigger download
    $.ajax({
    url: 'http://127.0.0.1:5000/bookingcomreport',
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    // xhrFields: {
    //     responseType: 'blob'  // Ensure the response is treated as a binary file
    // },
    success: function(response) {
            if (response.status) {
                console.log("Download URL:", response.download_url);

                // If the response is successful, handle the file download
                const downloadLink = document.createElement('a');
                downloadLink.href = response.download_url;  // URL to the file
                downloadLink.download = response.download_name; // Suggested filename for download
                document.body.appendChild(downloadLink);
                downloadLink.click();  // Trigger the download
                document.body.removeChild(downloadLink);  // Clean up
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

$('#submitFiles3').on('click', function () {
    const file1 = $('#file1')[0].files[0];
    const file2 = $('#file2')[0].files[0];
    const file3 = $('#file3')[0].files[0];  // Optional file3
    const file4 = $('#file4')[0].files[0];  // Optional file4

    console.log("file 1 :",file1);
    console.log("FIle 2 :",file2);
    // const sliderValue = $('#slider').val(); // Get slider value

    // console.log("Selected Slider Value:", sliderValue); // Debugging

    // if (!file1 || !file2) {
    //     alert('Please select both files.');
    //     return;
    // }

    const formData = new FormData();
    // formData.append('file1', file1);
    // formData.append('file2', file2);
    // formData.append('sliderValue', sliderValue);

    if (file1) {
        formData.append('file1', file1);
    }

    if (file2) {
        formData.append('file2', file2);
    }

    if (file3) {
        formData.append('file3', file3);
    }

    if (file4) {
        formData.append('file4', file4);
    }


    // AJAX call to upload files and trigger download
    $.ajax({
    url: 'http://127.0.0.1:5000/cancelled',
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    // xhrFields: {
    //     responseType: 'blob'  // Ensure the response is treated as a binary file
    // },
    success: function(response) {
            if (response.status) {
                console.log("Download URL:", response.download_url);

                // If the response is successful, handle the file download
                const downloadLink = document.createElement('a');
                downloadLink.href = response.download_url;  // URL to the file
                downloadLink.download = response.download_name; // Suggested filename for download
                document.body.appendChild(downloadLink);
                downloadLink.click();  // Trigger the download
                document.body.removeChild(downloadLink);  // Clean up
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

});
