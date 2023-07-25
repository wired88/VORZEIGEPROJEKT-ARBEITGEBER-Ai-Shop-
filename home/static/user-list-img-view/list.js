

const hover_divs = document.querySelectorAll('.category_image_container');
const hidden_divs = document.querySelectorAll('.hover_visible_options_container');

hover_divs.forEach((hover_div, index) => {
    const hidden_div = hidden_divs[index];



    // [hidden_div, hover_div].addEventListener ist nicht zulässig da diese methode cnicht über ein arry iterieren kann.7
    // stattdessen muss erst ein array mit den gewünschten elementen erstellt und über diese 'geloopt'/iteriert werden.
    [hidden_div, hover_div].forEach((element) => {
        element.addEventListener('mouseover', function(event) {
            hidden_div.style.opacity = '1';
            hidden_div.style.filter = 'blur(0)';
            hidden_div.style.transform = 'translateY(0)';
        });
        element.addEventListener('mouseout', function(event) {
            hidden_div.style.opacity = '0';
            hidden_div.style.filter = 'blur(5px)';
            hidden_div.style.transform = 'translateY(-100%)';
        });
    });
});


