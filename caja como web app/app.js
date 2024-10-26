class Store {
    constructor() {
        // Inventario inicial con productos, precios y cantidades
        this.inventory = {
            "pulsera": [3, 50],
            "sticker": [1, 200],
            "llavero": [10, 12],
            "postit": [3.5, 12],
        };
        // Registro de ventas
        this.salesRecord = {};
    }

    displayInventory() {
        let inventoryDisplay = "<table><tr><th>Producto</th><th>Precio</th><th>Cantidad</th></tr>";
        for (let producto in this.inventory) {
            let [precio, cantidad] = this.inventory[producto];
            inventoryDisplay += `<tr><td>${producto}</td><td>${precio.toFixed(2)}</td><td>${cantidad}</td></tr>`;
        }
        inventoryDisplay += "</table>";
        return inventoryDisplay;
    }

    purchaseProduct(productName, quantity) {
        if (!(productName in this.inventory)) {
            return `'${productName}' no está disponible en la tienda.`;
        }

        if (quantity <= 0) {
            return "La cantidad debe ser un número positivo.";
        }

        let [price, availableQuantity] = this.inventory[productName];
        if (quantity <= availableQuantity) {
            let totalPrice = price * quantity;
            this.inventory[productName][1] -= quantity;
            this.updateSalesRecord(productName, quantity);
            return `El precio total de ${quantity} '${productName}' es: S/${totalPrice.toFixed(2)}`;
        } else {
            return `No hay suficiente stock de '${productName}'. Stock disponible: ${availableQuantity} unidades.`;
        }
    }

    updateSalesRecord(producto, cantidad) {
        let fecha = new Date().toLocaleDateString();
        let hora = new Date().toLocaleTimeString();

        if (!this.salesRecord[fecha]) {
            this.salesRecord[fecha] = [];
        }
        this.salesRecord[fecha].push({ hora, producto, cantidad });
    }

    generateSalesReport() {
        let report = "<table><tr><th>Fecha</th><th>Hora</th><th>Producto</th><th>Cantidad</th></tr>";
        for (let fecha in this.salesRecord) {
            for (let venta of this.salesRecord[fecha]) {
                report += `<tr><td>${fecha}</td><td>${venta.hora}</td><td>${venta.producto}</td><td>${venta.cantidad}</td></tr>`;
            }
        }
        report += "</table>";
        return report;
    }
}

const store = new Store();

document.getElementById("showInventoryBtn").addEventListener("click", function() {
    document.getElementById("inventoryDisplay").innerHTML = store.displayInventory();
});

document.getElementById("purchaseBtn").addEventListener("click", function() {
    let productName = document.getElementById("product").value;
    let quantity = parseInt(document.getElementById("quantity").value);
    let result = store.purchaseProduct(productName, quantity);
    document.getElementById("purchaseResult").innerHTML = result;
});

document.getElementById("generateReportBtn").addEventListener("click", function() {
    document.getElementById("salesReportDisplay").innerHTML = store.generateSalesReport();
});
