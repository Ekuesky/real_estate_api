document.addEventListener('DOMContentLoaded', function() {
    const widget = cloudinary.createUploadWidget(
        {
            cloudName: 'YOUR_CLOUD_NAME',
            uploadPreset: 'YOUR_UPLOAD_PRESET',
            multiple: false,
            resourceType: "image"
        },
        (error, result) => {
            if (!error && result && result.event === "success") {
                const input = document.querySelector('input[type="file"]');
                const preview = document.querySelector('.preview-image');

                // Update the preview image
                if (preview) {
                    preview.src = result.info.secure_url;
                } else {
                    const newPreview = document.createElement('img');
                    newPreview.src = result.info.secure_url;
                    newPreview.classList.add('preview-image');
                    document.querySelector('.current-file').appendChild(newPreview);
                }

                // Create a new hidden input to store the Cloudinary URL
                let hiddenInput = document.querySelector('input[name="cloudinary_url"]');
                if (!hiddenInput) {
                    hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'cloudinary_url';
                    input.parentNode.appendChild(hiddenInput);
                }
                hiddenInput.value = result.info.secure_url;
            }
        }
    );

    document.querySelectorAll('.cloudinary-button').forEach(button => {
        button.addEventListener('click', () => {
            widget.open();
        });
    });
});