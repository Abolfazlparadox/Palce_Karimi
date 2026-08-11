document.addEventListener("DOMContentLoaded", function () {

    // Palace Karimi Office (Sabzevar Coordinates)
    const lat = 36.20398606913347;
    const lng = 57.69571887590756;

    // ایجاد نقشه
    const map = L.map('leaflet-map').setView([lat, lng], 17);

    // نقشه OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // آیکون اختصاصی
    const marker = L.icon({
        iconUrl: '/static/img/logo.webp',
        iconSize: [45, 45],
        iconAnchor: [22, 45],
        popupAnchor: [0, -40]
    });

    // مارکر
    L.marker([lat, lng], { icon: marker })
        .addTo(map)
        .bindPopup(`
            <div style="text-align:center;">
                <strong>Palace Karimi</strong><br>
                Premium Saffron & Pistachio Exporter
            </div>
        `)
        .openPopup();

});