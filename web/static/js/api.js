// Espera a que el documento HTML esté completamente cargado y listo para manipularse
$(document).ready(function(evt){

    // Agrega un controlador de eventos al elemento con el id "consulta"
    $("#consulta").click(function(evt) {        

        // Realiza una solicitud GET a la URL "https://jsonplaceholder.typicode.com/users" para obtener datos de usuarios
        $.get("https://jsonplaceholder.typicode.com/users", function(data){

            // Imprime los datos obtenidos de la API en la consola del navegador para fines de depuración
            console.log(data);

            // Elimina todos los elementos hijos del elemento con el id "ranking". Esto limpia la tabla antes de agregar nuevos datos para evitar duplicados.
            $("#ranking").empty();

            // Itera sobre los datos de usuarios obtenidos de la API
            $.each(data, function(i, user){

                // Para cada usuario, agrega una nueva fila a la tabla con los detalles del usuario (id, nombre y correo electrónico)
                $("#ranking").append(`<tr><td style="border: 1px solid">${user.id}</td>
                <td style="border: 1px solid">${user.name}</td>
                <td style="border: 1px solid">${user.email}</td></tr>`);
            });
        });
    });
});

// api valor del USD a CLP
$(document).ready(function(){
    // Evento al hacer click en el botón
    $("#consultaDolar").click(function(){
        // Realizar la solicitud AJAX
        $.getJSON('https://mindicador.cl/api', function(data) {
            var dailyIndicators = data;
            // Obtenemos el valor del dólar desde la respuesta de la API
            var valorDolar = dailyIndicators.dolar.valor;
            // Mostramos el valor del dólar en el párrafo especificado
            $("#valorDolar").html('El valor actual del dólar a peso chileno es: $' + valorDolar.toFixed(2));
        }).fail(function(jqXHR, textStatus, errorThrown) {
            console.log('Error al consumir la API:', textStatus, errorThrown);
        });
    });
});




