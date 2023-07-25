window.onload = function() {
  console.log(unclicked_icon);
  console.log(clicked_icon);
  const button = document.querySelector('.mark_button');
  const image = document.querySelector('.mark_icon');

  const images = [unclicked_icon, clicked_icon];
  let currentImage = 0;

  button.addEventListener('click', () => {
    console.log('Image clicked');
    currentImage = (currentImage + 1) % images.length; // die nummer wird so lang erhöht bis sie die grenze der sich darin befindenden objekte erreicht. dann wird duch % images.length; der wert wieder auf 0 gesetzt.
    image.src = images[currentImage];
  });
}




