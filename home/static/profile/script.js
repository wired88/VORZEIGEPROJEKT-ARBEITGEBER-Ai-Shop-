

window.onload = function() {
    let userChangePage = document.querySelectorAll('.content_profile, .pw_change_page');

    let changePasswordButton = document.getElementById('change_password_button');
    let changeProfilePageButton = document.getElementById('change_profile_button');

    changePasswordButton.addEventListener('click', function() {
        console.log('clicked');
        userChangePage[0].style.display = 'none';
        const profile = document.querySelectorAll('.content_profile > *');
        profile.forEach(function(element) {
            element.style.display = 'none';
        });
        userChangePage[1].style.display = 'block';
        const password = document.querySelectorAll('.pw_change_page > *');
        password.forEach(function(element) {
            element.style.display = 'block';
        });
    });

    changeProfilePageButton.addEventListener('click', function() {
        userChangePage[1].style.display = 'none';
        const password_change = document.querySelectorAll('.pw_change_page > *');
        password_change.forEach(function(element) {
            element.style.display = 'none';
        });
        userChangePage[0].style.display = 'block';
        const profile_change = document.querySelectorAll('.content_profile > *');
        profile_change.forEach(function(element) {
            element.style.display = 'block';
        });
    });
}
