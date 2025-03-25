document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('nav a');
    const card = document.querySelector('.card');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);

            if (targetSection) {
                event.preventDefault();
                card.scrollTop = targetSection.offsetTop - card.offsetTop;
            }
        });
    });
});

function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

// Mapbox Initialization
document.addEventListener('DOMContentLoaded', function () {
    mapboxgl.accessToken = 'pk.eyJ1IjoicmFoaW4wMiIsImEiOiJjbThhOHMyZXcxZDN5MnhzYzcycGFkeTJwIn0.U3L_6EUIsD1VmuqjrAwBYg';

    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [-0.28070274058493555, 51.77573335660947],
        zoom: 10,
        attributionControl: false
    });

    map.addControl(new mapboxgl.NavigationControl());

    function addMarker(coords, popupText) {
        new mapboxgl.Marker()
            .setLngLat(coords)
            .setPopup(new mapboxgl.Popup().setHTML(`<b>${popupText}</b>`))
            .addTo(map);
    }

    addMarker([-0.2231, 51.7634], "We are based in Hatfield");
    addMarker([-0.20855686113062374, 51.803775472981485], "We are based in Welwyn Garden City");
    addMarker([-0.3428, 51.7527], "We are based in St Albans");
});
