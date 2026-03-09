document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const previewImage = document.getElementById('preview-image');
    const dropContent = document.getElementById('drop-content');

    if (dropArea) {
        dropArea.addEventListener('click', () => fileInput.click());

        fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(name => {
            dropArea.addEventListener(name, e => { e.preventDefault(); e.stopPropagation(); });
        });

        dropArea.addEventListener('drop', e => {
            const file = e.dataTransfer.files[0];
            fileInput.files = e.dataTransfer.files;
            handleFile(file);
        });

        function handleFile(file) {
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    previewImage.src = e.target.result;
                    previewImage.style.display = 'block'; 
                    dropContent.style.display = 'none';   
                };
                reader.readAsDataURL(file);
            }
        }
    }
});