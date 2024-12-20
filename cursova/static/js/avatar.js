document.getElementById('change-avatar-btn').addEventListener('click', function() {
        // Показуємо вікно вибору файлу
        document.getElementById('profile-image-input').click();
    });

    // Коли файл обраний, показуємо форму для завантаження
    document.getElementById('profile-image-input').addEventListener('change', function() {
        if (this.files && this.files[0]) {
            // Відображаємо форму для завантаження
            document.getElementById('profile-image-form').style.display = 'block';
            document.getElementById('hidden-profile-image').files = this.files;
        }
    });