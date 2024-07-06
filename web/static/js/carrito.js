document.addEventListener('DOMContentLoaded', function() {
    // Variable de arreglos de Productos
    let allProducts = [];

    // Agregar evento de clic al icono de cierre
    document.querySelector('.row-product').addEventListener('click', function(event) {
        if (event.target.classList.contains('icon-close')) {
            // Obtener el título del producto a eliminar
            const titleToRemove = event.target.closest('.cart-product').querySelector('.titulo-producto-carrito').textContent;

            // Filtrar el array para excluir el producto que se está eliminando
            allProducts = allProducts.filter(product => product.title !== titleToRemove);

            // Actualizar la visualización del carrito
            showHTML();
        }
    });

    // Selección de elementos del DOM
    const btnCart = document.querySelector('.container-cart-icon');
    const containerCartProducts = document.querySelector('.container-cart-products');

    // Agregar evento de clic al icono del carrito
    btnCart.addEventListener('click', function() {
        containerCartProducts.classList.toggle('hidden-cart');
    });

    // Escucha los clics en el contenedor de productos
    document.querySelector('.galery').addEventListener('click', function(event) {
        // Verifica si el clic se produjo en un botón "Agregar al carrito"
        if (event.target.classList.contains('btn-add-cart')) {
            // Obtiene la información del producto
            const product = event.target.closest('.card-product');
            const infoProduct = {
                quantity: 1,
                title: product.querySelector('h2').textContent,
                price: product.querySelector('p').textContent,
            };

            // Agrega el producto al carrito
            addProductToCart(infoProduct);

            // Actualiza la visualización del carrito
            showHTML();
        }
    });

    // Función para agregar un producto al carrito
    function addProductToCart(infoProduct) {
        const exists = allProducts.some(product => product.title === infoProduct.title);

        if (exists) {
            const products = allProducts.map(product => {
                if (product.title === infoProduct.title) {
                    product.quantity++;
                    return product;
                } else {
                    return product;
                }
            });
            allProducts = [...products];
        } else {
            allProducts = [...allProducts, infoProduct];
        }
    }

    // Función para mostrar HTML
    const showHTML = () => {
        // Selección de elementos del DOM
        const cartEmpty = document.querySelector('.cart-empty');
        const rowProduct = document.querySelector('.row-product');
        const cartTotal = document.querySelector('.cart-total');
        const valorTotal = document.querySelector('.total-pagar');
        const countProducts = document.querySelector('#contador-productos');

        if (!allProducts.length) {
            cartEmpty.classList.remove('show');
            rowProduct.classList.add('hidden');
            cartTotal.classList.add('hidden');
        } else {
            cartEmpty.classList.add('hidden');
            rowProduct.classList.remove('hidden');
            cartTotal.classList.remove('hidden');
        }

        // Limpiar HTML
        rowProduct.innerHTML = '';

        let total = 0;
        let totalOfProducts = 0;

        allProducts.forEach(product => {
            const containerProduct = document.createElement('div');
            containerProduct.classList.add('cart-product');

            containerProduct.innerHTML = `
                <div class="info-cart-product">
                    <span class="cantidad-producto-carrito">${product.quantity}</span>
                    <p class="titulo-producto-carrito">${product.title}</p>
                    <span class="precio-producto-carrito">${product.price}</span>
                </div>
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="icon-close"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M6 18L18 6M6 6l12 12"
                    />
                </svg>
            `;

            rowProduct.append(containerProduct);

            total += product.quantity * parseFloat(product.price.replace('$', ''));
            totalOfProducts += product.quantity;
        });

        valorTotal.innerText = `$${total}`;
        countProducts.innerText = totalOfProducts;
    };
});
