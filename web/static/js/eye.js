
function validationEye(){
    var x = document.getElementById("confirm-password");
    var y = document.getElementById("hide1");
    var z = document.getElementById("hide2");
    if (x.type === "password"){
        x.type = "text";
        y.style.display="block";
        z.style.display="none";
    }else{
        x.type = "password";
        y.style.display="none";
        z.style.display="block";
    }
}

function validateUser(input){
    var nameLength = $(input).val().length;
    if (nameLength < 3 || nameLength > 20) {
        $('#user-error').text('El usuario debe tener entre 3 y 20 caracteres.');
        return false;
    } else {
        $('#user-error').text('');
        return true;
    }
}

function validateEmail(input){
    var email = $(input).val();
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        $('#email-error').text('Por favor, introduce una dirección de correo electrónico válida.');
        return false;
    } else {
        $('#email-error').text('');
        return true;
    }
}

function validatePassword(input){
    var password = $(input).val();
    if (password.length < 6) {
        $('#password-error').text('La contraseña debe tener al menos 6 caracteres.');
        return false;
    } else {
        $('#password-error').text('');
        return true;
    }
}

function validateConfirmPsw(){
    var password = $('#password').val();
    var confirmPassword = $('#confirm-password').val();
    if (password !== confirmPassword) {
        $('#confirm-password-error').text('Las contraseñas no coinciden.');
        return false;
    } else {
        $('#confirm-password-error').text('');
        return true;
    }
}

$(document).ready(function(){
    $('#myInput').on('click', function(){
        validationEye(this);
    });

    $('#user').on('input', function(){
        validateUser(this);
    });

    $('#email').on('input', function(){
        validateEmail(this);
    });

    $('#password').on('input', function(){
        validatePassword(this);
    });

    $('#confirm-password').on('input', function(){
        validateConfirmPsw();
    });

    $('form').on('submit', function(event){ 
        var userLength = $('#user').val().length;
        var email = $('#email').val();
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        var password = $('#password').val();
        var confirmPassword = $('#confirm-password').val();
        var valid = true; // Variable para verificar si todas las validaciones son correctas
        
        if (userLength === 0 || email.length === 0 || password.length === 0 || confirmPassword.length === 0) {
            // Verificar si algún campo está vacío y mostrar un mensaje de error
            $('#user-error').text('Por favor, completa todos los campos.');
            valid = false; // Indicar que la validación no pasó
            event.preventDefault(); // Evitar el envío del formulario
        } else if (userLength < 3 || userLength > 20) {
            $('#user-error').text('El usuario debe tener entre 3 y 20 caracteres.');
            valid = false; // Indicar que la validación no pasó
            event.preventDefault(); // Evitar el envío del formulario
        } else if (!emailRegex.test(email)) {
            $('#email-error').text('Por favor, introduce una dirección de correo electrónico válida.');
            valid = false; // Indicar que la validación no pasó
            event.preventDefault(); // Evitar el envío del formulario
        } else if (password.length < 6) {
            $('#password-error').text('La contraseña debe tener al menos 6 caracteres.');
            valid = false; // Indicar que la validación no pasó
            event.preventDefault(); // Evitar el envío del formulario
        } else if (password !== confirmPassword) {
            $('#confirm-password-error').text('Las contraseñas no coinciden.');
            valid = false; // Indicar que la validación no pasó
            event.preventDefault(); // Evitar el envío del formulario
        }
    });
});



