const fileInput = document.getElementById('documents');
const fileList = document.getElementById('fileList');
const uploadedFiles = new Set();

fileInput.addEventListener('change', handleFileSelect);

function handleFileSelect(event) {
    const files = event.target.files;
    
    for (const file of files) {
        if (!uploadedFiles.has(file.name)) {
            uploadedFiles.add(file.name);
            addFileToList(file);
        }
    }
}

function addFileToList(file) {
    const fileItem = document.createElement('div');
    fileItem.className = 'file-item';
    
    const fileName = document.createElement('span');
    fileName.textContent = file.name;
    
    const removeButton = document.createElement('button');
    removeButton.className = 'remove-file';
    removeButton.textContent = '×';
    removeButton.onclick = () => {
        fileItem.remove();
        uploadedFiles.delete(file.name);
    };
    
    fileItem.appendChild(fileName);
    fileItem.appendChild(removeButton);
    fileList.appendChild(fileItem);
}

function handleSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const projectData = {
        title: formData.get('title'),
        description: formData.get('description'),
        deadline: formData.get('deadline'),
        files: Array.from(uploadedFiles)
    };

    console.log('Project Created:', projectData);
    
    alert('Project created successfully!');
    
    event.target.reset();
    fileList.innerHTML = '';
    uploadedFiles.clear();
    window.location.href="Proff.html";
}