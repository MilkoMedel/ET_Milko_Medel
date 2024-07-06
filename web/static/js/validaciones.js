
// permitir solo numeros y letra k en input rut
function isNumber(evt){
    let charCode = evt.which;

    // Permitir números (códigos de tecla entre 48 y 57) y la letra 'K' (código de tecla 75)
    if ((charCode >= 48 && charCode <= 57) || charCode === 75) {
        return true;
    } else {
        return false;
    }
}

// Función para validar un RUT
function checkRut(rut) {
    // Verificar si el campo RUT está vacío o tiene menos de dos caracteres
    if (rut.value.length <= 0 ) {
        // Si es así, mostrar un mensaje indicando que se debe ingresar un RUT válido
        
    }

    // Limpiar el valor del RUT ingresado (quitar puntos y guiones)
    let valor = clean(rut.value);

    // Separar el cuerpo del RUT y el dígito verificador
    let bodyRut = valor.slice(0, -1);
    let dv = valor.slice(-1).toUpperCase();

    // Formatear visualmente el RUT (agregar puntos y guión)
    rut.value = format(rut.value);

    // Calcular el dígito verificador utilizando el método del Módulo 11
    suma = 0;
    multiplo = 2;

    // Iterar sobre cada dígito del cuerpo del RUT
    for (i = 1; i <= bodyRut.length; i++) {
        // Obtener el producto del dígito por el multiplo correspondiente
        index = multiplo * valor.charAt(bodyRut.length - i);
        // Sumar al contador general
        suma = suma + index;

        // Consolidar el multiplo dentro del rango [2, 7]
        if (multiplo < 7) {
            multiplo = multiplo + 1;
        } else {
            multiplo = 2;
        }
    }

    // Calcular el dígito verificador esperado según el Módulo 11
    dvEsperado = 11 - (suma % 11);

    // Manejar casos especiales (0 y K)
    dv = dv == "K" ? 10 : dv;
    dv = dv == 0 ? 11 : dv;

    // Verificar si el cuerpo del RUT tiene menos de 7 caracteres
    if (bodyRut.length <= 7) {
        // Si es así, mostrar un mensaje indicando que el RUT es demasiado corto
        rut.setCustomValidity("El RUT debe tener 8 o más dígitos.");
    }

    // Verificar si el dígito verificador esperado no coincide con el ingresado
    if (dvEsperado != dv ) {
        // Si no coincide, mostrar un mensaje indicando que el RUT es incorrecto
        rut.setCustomValidity("RUT Inválido");
        //mensaje.innerHTML = 'El RUT ingresado: ' + rut.value + ' Es <strong>INCORRECTO</strong>.';
        return false;
        
    }else if(dv === "-"){
        // Si no coincide, mostrar un mensaje indicando que el RUT es incorrecto
        rut.setCustomValidity('');
        alert("campo vacio").show();
        return false;
    } else {
      // Si coincide, mostrar un mensaje indicando que el RUT es correcto
        rut.setCustomValidity('');
        return true;
        
    }
}

function format(rut) {
    rut = clean(rut);
    if (rut.length > 0) {
        var result = rut.slice(-4, -1) + '-' + rut.substr(rut.length - 1);
        for (var i = 4; i < rut.length; i += 3) {
            result = rut.slice(-3 - i, -i) + '.' + result;
        }
        return result;
    } else {
        return rut; // Si el campo está vacío, devuelve el valor vacío sin agregar el guion
    }
}

function clean (rut) {
    return typeof rut === 'string'
    ? rut.replace(/^0+|[^0-9kK]+/g, '').toUpperCase()
    : ''
}

// Función para calcular la edad a partir de una fecha de nacimiento
function calcularEdad(fechaNacimiento) {
    var hoy = new Date();
    var edad = (hoy.getFullYear() - fechaNacimiento.getFullYear());
    var mes = hoy.getMonth() - fechaNacimiento.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < fechaNacimiento.getDate())) {
        edad--;
    }
    return edad;
}

// Función para validar un correo electrónico con el dominio "@gmail.com"
function validarEmail(email) {
    var emailRegex = /^[^\s@]+@gmail\.com$/;
    return emailRegex.test(email);
}

// Función para validar la entrada de edad
function validarEdad(entrada) {
    return /^\d+$/.test(entrada) && parseInt(entrada) >= 18 && parseInt(entrada) <= 35;
}

// Función para validar la entrada de número de celular
function validarCelular(entrada) {
    return /^(\+?56)?-?9\d{8}$/.test(entrada);
}

$(document).ready(function(){
    // Función para validar apellidos y nombre
    $('#paterno, #nombre').each(function() {
        var inputField = $(this);
        inputField.on('input', function() {
            var currentValue = inputField.val().trim();
            if (currentValue.length < 3 || currentValue.length > 20) {
                inputField[0].setCustomValidity("Debe contener entre 3 y 20 caracteres.");
            } else if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+(?: [a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*)?$/.test(currentValue)) {
                inputField[0].setCustomValidity("Solo se permiten letras y espacios, separados por un espacio si son dos palabras.");
            } else {
                inputField[0].setCustomValidity("");
            }
        });
    });

    // Evento input para el campo de fecha de nacimiento
    $('#fecha').on('input', function() {
        var fechaNacimiento = new Date($(this).val());
        var edad = calcularEdad(fechaNacimiento);
        if (edad < 18 || edad > 35) {
            $(this)[0].setCustomValidity("Debe tener entre 18 y 35 años.");
        } else {
            $(this)[0].setCustomValidity("");
        }
    });

    // Evento input para el campo de correo electrónico
    $('#correo').on('input', function() {
        var email = $(this).val();
        if (!validarEmail(email)) {
            $(this)[0].setCustomValidity("Ingrese un correo electrónico válido con el dominio '@gmail.com'.");
        } else {
            $(this)[0].setCustomValidity("");
        }
    });

    // Evento input para el campo de contraseña
    $('#password').on('input', function() {
        var currentValue = $(this).val();
        if (currentValue.length < 6 || currentValue.length > 20) {
            $(this)[0].setCustomValidity("La contraseña debe contener entre 6 y 20 caracteres.");
        } else {
            $(this)[0].setCustomValidity("");
        }
    });

    // Evento keypress para el campo de edad
    $('#edad').on('keypress', function(event) {
        var charCode = event.which ? event.which : event.keyCode;
        if (charCode < 48 || charCode > 57) {
            event.preventDefault();
        }
    });

    // Evento input para el campo de edad
    $('#edad').on('input', function() {
        var entrada = $(this).val();
        if (!validarEdad(entrada)) {
            $(this)[0].setCustomValidity("La edad debe ser un número entre 18 y 35.");
        } else {
            $(this)[0].setCustomValidity("");
        }
    });

    // Evento keypress para el campo de número de celular
    $('#celular').on('keypress', function(event) {
        var charCode = event.which ? event.which : event.keyCode;
        if (charCode < 48 || charCode > 57) {
            event.preventDefault();
        }
    });

    // Evento input para el campo de número de celular
    $('#celular').on('input', function() {
        var entrada = $(this).val();
        if (!validarCelular(entrada)) {
            $(this)[0].setCustomValidity("El número de celular debe contener 11 dígitos.");
        } else {
            $(this)[0].setCustomValidity("");
        }
    });
});




