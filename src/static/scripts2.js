$(document).ready(function() {
    // Initialize Select2
    $("#propertySelect").select2({
        placeholder: "Search or select a property...",
        allowClear: true,
        width: '100%',
        minimumResultsForSearch: 0
    });

    // Update slider value display
    $("#slider").on('input', function() {
        $("#sliderValue").text($(this).val());
    });

    function getFormData() {
        // Get mandatory values
        const propertyName = $("#propertySelect").val();
        const startDate = $("#startDate").val();
        const endDate = $("#endDate").val();
        const sliderValue = $("#slider").val();

        // Validate mandatory fields
        if (!propertyName || !startDate || !endDate) {
            showModal("Please fill in all fields:\n- Property Name\n- Start Date\n- End Date",false);
            return null;
        }

        // Create FormData object
        const formData = new FormData();

        // Add mandatory fields
        formData.append('property', propertyName);
        formData.append('startDate', startDate);
        formData.append('endDate', endDate);
        formData.append('sliderValue', sliderValue);

        // Add optional file fields if they exist
        const fileInputs = {
            'file1': $('#file1')[0].files[0],
            'file2': $('#file2')[0].files[0]
        };

        // Append files only if they are selected
        for (const [key, file] of Object.entries(fileInputs)) {
            if (file) {
                formData.append(key, file);
            }
        }

        return formData;
    }

    // Example usage with your buttons
    $("#submitFiles").on("click", function(e) {
        e.preventDefault();

        let checkmark = $("#includeExtra").is(":checked") ? "Yes" : "No";

        const formData = getFormData();
        formData.append('checkmark', checkmark);
        
        if (formData) {
            // Example of how to use the formData
            console.log("Form data contents:");
            for (const pair of formData.entries()) {
                console.log(pair[0] + ': ' + pair[1]);
            }

            // Example AJAX call
            
            $.ajax({
                url: 'http://127.0.0.1:5000/upload',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                beforeSend: function() {
                    // Show loading spinner
                    document.getElementById('loadingSpinner').style.display = 'block';
                },
                success: function(response) {
                    console.log("Response status:", response.status);
                    // Handle success case - response with status true
                    if (response.status === true) {
                        const downloadLink = document.createElement('a');
                        downloadLink.href = response.download_url;
                        downloadLink.download = response.download_name;
                        document.body.appendChild(downloadLink);
                        downloadLink.click();
                        document.body.removeChild(downloadLink);
                        
                        showModal('File downloaded successfully!', true);
                    } 
                    // Handle failure case - response with status false
                    else {
                        showModal(response.message || 'Required files are missing', false);
                    }
                },
                error: function(xhr, status, error) {
                    // Handle error responses (400, 500, etc.)
                    if (xhr.responseJSON) {
                        showModal(xhr.responseJSON.message || 'An error occurred', false);
                    } else {
                        showModal('An error occurred: ' + error, false);
                    }
                },
                complete: function() {
                    // Hide loading spinner
                    document.getElementById('loadingSpinner').style.display = 'none';
                }
            });
        }
    });

    $('#submitFiles2').on('click', function () {
        const formData = getFormData();
    
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
                if (response.status === true) {
                    console.log("Download URL:", response.download_url);

                    // If the response is successful, handle the file download
                    const downloadLink = document.createElement('a');
                    downloadLink.href = response.download_url;  // URL to the file
                    downloadLink.download = response.download_name; // Suggested filename for download
                    document.body.appendChild(downloadLink);
                    downloadLink.click();  // Trigger the download
                    document.body.removeChild(downloadLink);  // Clean up
                    showModal('File downloaded successfully' , true);
                } else {
                    // Handle failure scenario (e.g., show an error message)
                    showModal(response.message || 'Required files are missing');
                }
        },
        error: function(xhr, status, error) {
            // Handle error responses (400, 500, etc.)
            if (xhr.responseJSON) {
                showModal(xhr.responseJSON.message || 'An error occurred', false);
            } else {
                showModal('An error occurred: ' + error, false);
            }
        },
        complete: function() {
            // Hide loading spinner
            document.getElementById('loadingSpinner').style.display = 'none';
        }

    });
    });

    $('#submitFiles3').on('click', function () {
    
        const formData = getFormData();

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
                if (response.status === true) {
                    console.log("Download URL:", response.download_url);

                    // If the response is successful, handle the file download
                    const downloadLink = document.createElement('a');
                    downloadLink.href = response.download_url;  // URL to the file
                    downloadLink.download = response.download_name; // Suggested filename for download
                    document.body.appendChild(downloadLink);
                    downloadLink.click();  // Trigger the download
                    document.body.removeChild(downloadLink);  // Clean up
                    showModal('File downloaded successfully' , true);
                } else {
                    // Handle failure scenario (e.g., show an error message)
                    showModal(response.message || 'Required files are missing');
                }
        },
        error: function(xhr, status, error) {
            // Handle error responses (400, 500, etc.)
            if (xhr.responseJSON) {
                showModal(xhr.responseJSON.message || 'An error occurred', false);
            } else {
                showModal('An error occurred: ' + error, false);
            }
        },
        complete: function() {
            // Hide loading spinner
            document.getElementById('loadingSpinner').style.display = 'none';
        }

    });
    });

    // Add date validation
    $("#startDate, #endDate").on("change", function() {
        const startDate = new Date($("#startDate").val());
        const endDate = new Date($("#endDate").val());
        
        if (endDate < startDate) {
            showModal("End date cannot be earlier than start date" , false);
            $(this).val(""); // Clear the invalid date
        }
    });
    

    function showModal(message, isSuccess = true) {
        const modal = document.getElementById('notificationModal');
        const modalIcon = document.getElementById('modalIcon');
        const modalMessage = document.getElementById('modalMessage');
    
        // Set icon based on status
        modalIcon.innerHTML = isSuccess ? '✅' : '❌';
        modalIcon.className = 'modal-icon ' + (isSuccess ? 'success-icon' : 'error-icon');
        
        // Set message
        modalMessage.textContent = message;
        
        // Show modal
        modal.style.display = 'block';
    
        // Auto-hide after 3 seconds for success messages
        if (isSuccess) {
            setTimeout(() => {
                modal.style.display = 'none';
            }, 3000);
        }
    }
    
    // Close modal when clicking the X
    document.querySelector('.close-modal').onclick = function() {
        document.getElementById('notificationModal').style.display = 'none';
    }
    
    // Close modal when clicking outside
    window.onclick = function(event) {
        const modal = document.getElementById('notificationModal');
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});