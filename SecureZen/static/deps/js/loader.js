
    // Function to control the display of the loader
    function displayLoader(shouldDisplay) {
        var loader = document.getElementById('uploader');
        if (loader) {
            loader.style.display = shouldDisplay ? 'block' : 'none';
        } else {
            console.error("Loader element not found.");
        }
    }

    // Function to hide the result section
    function hideResultSection() {
        var result = document.getElementById('result');
        if (result) {
            result.style.display = 'none';
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        var form = document.getElementById('myForm');

        if (form) {
            form.addEventListener('submit', function(event) {
                displayLoader(true);
                hideResultSection();
                // Show the loader before the form is submitted
            });
        } else {
            console.error("Form element not found on page load.");
        }

        // Initial check to see if loader should be displayed
        // Assuming that the loader should be hidden on initial page load
        displayLoader(false);

        var result = document.getElementById('result');
        var error = document.querySelector('.text-danger');
        
        // Assuming you want to hide the loader if there's a result or an error on page load
        if (result || error) {
            displayLoader(false);
        }
    });
