document.addEventListener('DOMContentLoaded', function () {
    const currencyFields = document.querySelectorAll('input.currency');

    currencyFields.forEach(field => {
        field.addEventListener('input', function (event) {
            // Eliminar todos los caracteres que no sean números
            let value = event.target.value.replace(/\D/g, '');

            // Formatear el número con separadores de miles usando puntos
            let formattedValue = value.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

            // Actualizar el valor del campo de entrada
            event.target.value = formattedValue;
        });
    });
});
