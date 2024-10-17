# Requerimientos del Sistema de Cotización de Ventanas

Este documento especifica los requerimientos funcionales para el sistema de cotización de ventanas.

## Registro de Entidades

- El sistema debe permitir el registro de un estilo de ventana con los siguientes atributos: tipo de ventana (O, XO, OXXO, OXO), dimensiones (ancho y alto), y número de naves.
- El sistema debe permitir el registro de una nave con los atributos: tipo de nave (O o X), dimensiones (ancho y alto), tipo de vidrio, acabado, y, si aplica, si es esmerilado.
- El sistema debe permitir el registro de un tipo de vidrio con los atributos: tipo (transparente, bronce, azul) y precio por cm².
- El sistema debe permitir el registro de un acabado de aluminio con los atributos: tipo (pulido, lacado brillante, lacado mate, anodizado) y precio por metro lineal.
- El sistema debe permitir el registro de elementos adicionales con atributos: esquinas (precio por unidad), chapas (precio por unidad), y materiales adicionales incluidos (remaches, tornillos, caucho).
- El sistema debe permitir el registro de un cliente con los atributos: nombre, tipo de cliente (e.g., empresa constructora), y dirección de contacto.
- El sistema debe permitir el registro de una cotización con los atributos: fecha, número de cotización, cliente, listado de ventanas, y descuento si corresponde.

## Gestión de Precios

- El sistema debe calcular el costo de cada ventana teniendo en cuenta los siguientes elementos:
  - Precio del aluminio (por metro lineal) según el tipo de acabado.
  - Precio del vidrio (por cm²) y costo adicional si el vidrio es esmerilado.
  - Precio de las esquinas (cantidad por ventana).
  - Precio de la chapa si aplica (para naves tipo X).
- El sistema debe aplicar un descuento del 10% si la cantidad de ventanas solicitadas excede las 100 unidades.

## Relaciones entre Entidades

- El sistema debe permitir asociar múltiples estilos de ventanas a un cliente.
- El sistema debe relacionar naves con ventanas, calculando automáticamente sus dimensiones basadas en el ancho y alto de la ventana completa.
- El sistema debe asociar un tipo de vidrio y un acabado a cada nave.
- El sistema debe calcular automáticamente el número de esquinas y chapas necesarias para cada ventana según el tipo y cantidad de naves.

## Consultas y Reportes

- El sistema debe permitir consultar la información de una ventana, incluyendo tipo, dimensiones (ancho y alto), número de naves, tipo de vidrio, acabado, y costo total.
- El sistema debe permitir consultar la información de un cliente, incluyendo nombre, tipo de cliente, y cotizaciones solicitadas.
- El sistema debe permitir consultar las cotizaciones realizadas, incluyendo cliente, fecha de la cotización, y costo total.
- El sistema debe generar informes de cotización, detallando el desglose de costos por ventana y aplicando descuentos si corresponde.

## Validaciones

- El sistema debe verificar que las dimensiones de las naves sean coherentes con el ancho y alto de la ventana.
- El sistema debe garantizar que el vidrio sea siempre 1.5 cm más pequeño que la nave en cada lado.
- El sistema debe asegurar que el descuento solo se aplique para más de 100 ventanas del mismo diseño.

