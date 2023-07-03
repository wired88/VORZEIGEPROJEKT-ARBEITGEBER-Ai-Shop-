// scroll Animation for homePage //
const tagBox = document.querySelector('.product-text');

$.ajax({ // hier wird eine verbindung mit ajx hergestellt
    type: 'GET', // wir signalisieren eine get anfrage.
    url: '', // der url wird angegeben
    success: function (response) { // bei success wird die func ausgeführt
        console.log('scroll_up', response.text) // und success wird in der konsole ausgegeben
        tagBox.textContent = response.text
    },
    error: function(error){ // bei error ds gleiche
        console.log('scroll_down', error)
    }

},1000);




























const observer = new IntersectionObserver((entries) => {  //1//
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting) { // wenn über die section gescrollt wird, ... //
            //entry.target.classList.add('show'); // wird die klasse 'show' hinzugefügt. //
            entry.target.style.opacity= '1';
            entry.target.style.filter= 'blur(0)';
            entry.target.style.transform= 'translateX(0)';
            entry.target.style.display= 'flex';
        } else {
            //entry.target.classList.remove('show');
            entry.target.style.opacity= '0';
            entry.target.style.filter= 'blur(5px)';
            entry.target.style.transform= 'translateX(-100%)';
           // wird nicht mehr drübergescrollt wird die klasse wieder entfernt, sodass man den effekt immer wieder hat. //
        }
    });
});

const hiddenElements = document.querySelectorAll('.swipe_box, .lower_header_text, .navbar_a');
hiddenElements.forEach((el) => observer.observe(el));












/*
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            console.log(entry)
            entry.target.classList.add('show');
            entry.target.classList.remove('hidden');
        } else {
            entry.target.classList.remove('show');
            entry.target.classList.add('hidden');
        }
    });
});

const hiddenElements = document.querySelectorAll('#test');
hiddenElements.forEach((el) => observer.observe(el));
*/

//1 zunächst wird ein <intersectionObserver erstellt welcher überprüft welche objekte gerade im sichtfeld des bildschirms sind //
//2, wenn objekte der klasse hidden den sichtbaren brereich betreten, wird die klasse Show hinzugefügt und sobald sie nicht mehr im sichtfeld ist wieder entfernt//
//3