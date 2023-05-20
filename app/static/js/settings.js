document.querySelectorAll('.edit-button').forEach(function(button) {
    button.addEventListener('click', function() {
        const tr = this.parentElement.parentElement;
        const settingValueElement = tr.querySelector('.setting-value');
        const settingInputElement = tr.querySelector('.setting-input');

        settingInputElement.value = settingValueElement.textContent;

        settingValueElement.style.display = 'none';
        settingInputElement.style.display = '';

        this.style.display = 'none';
        tr.querySelector('.save-button').style.display = '';

        // make the input field editable
        settingInputElement.readOnly = false;
    });
});

document.querySelectorAll('.save-button').forEach(function(button) {
    button.addEventListener('click', async function() {
        const tr = this.parentElement.parentElement;
        const settingName = tr.children[0].textContent;
        const settingValueElement = tr.querySelector('.setting-value');
        const settingInputElement = tr.querySelector('.setting-input');

        const newValue = settingInputElement.value;

        settingValueElement.textContent = newValue;

        settingInputElement.style.display = 'none';
        settingValueElement.style.display = '';

        this.style.display = 'none';
        tr.querySelector('.edit-button').style.display = '';

        // make the input field uneditable
        settingInputElement.readOnly = true;

        // send the updated setting value to your server
        const response = await fetch('/save_setting', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `setting_name=${encodeURIComponent(settingName)}&setting_value=${encodeURIComponent(newValue)}`,
        });

        if (!response.ok) {
            console.error('Failed to save setting', response);
        }
    });
});