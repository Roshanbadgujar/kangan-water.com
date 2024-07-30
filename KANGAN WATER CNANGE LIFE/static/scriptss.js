document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();

        xhr.open('POST', '/submit_form', true);
        xhr.onload = function () {
            if (xhr.status === 200) {
                // Redirect to submissions page upon successful form submission
                window.location.href = '/submissions';
            }
        };

        xhr.send(formData);
    });
});
document.getElementById("menu-button").addEventListener("click", function() {
    document.getElementById("slider-menu").style.display = "block";
});

document.getElementById("close-button").addEventListener("click", function() {
    document.getElementById("slider-menu").style.display = "none";
});
document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll("nav ul li a");

    navLinks.forEach(link => {
        link.addEventListener("mouseover", function() {
            link.style.color = "#ff6347"; // Change to desired hover color
        });

        link.addEventListener("mouseout", function() {
            link.style.color = "#fff";
        });
    });
});
let slideIndex = 1;
        showSlides(slideIndex);

        function plusSlides(n) {
            showSlides(slideIndex += n);
        }

        function currentSlide(n) {
            showSlides(slideIndex = n);
        }

        function showSlides(n) {
            let i;
            let slides = document.getElementsByClassName("slides")[0].children;
            let dots = document.getElementsByClassName("dot");
            if (n > slides.length) {slideIndex = 1}
            if (n < 1) {slideIndex = slides.length}
            for (i = 0; i < slides.length; i++) {
                slides[i].style.display = "none";
            }
            for (i = 0; i < dots.length; i++) {
                dots[i].className = dots[i].className.replace(" active", "");
            }
            slides[slideIndex-1].style.display = "block";
            dots[slideIndex-1].className += " active";
        }