// 1. Escribe un comentario en una línea
// Este es un comentario en una línea

// 2. Escribe un comentario en varias líneas
/* Este es un comentario
en varias líneas */

// 3. Declara variables con valores asociados a todos los datos de tipo primitivos
let user = "manuelytuza@mac-center.com"; // string
let cupOfTea = 3; // number
let password = true; // boolean
let bigInn = 838383838383838383883838383839392929929220n; // bigint
let mySymbol = Symbol("10"); // symbol
let unDef; // undefined
let varNull = null; // null

// 4. Imprime por consola el valor de todas las variables
console.log(user, cupOfTea, password, bigInn, mySymbol, unDef, varNull);

// 5. Imprime por consola el tipo de todas las variables
console.log(typeof user); // string
console.log(typeof cupOfTea); // number
console.log(typeof password); // boolean
console.log(typeof bigInn); // bigint
console.log(typeof mySymbol); // symbol
console.log(typeof unDef); // undefined
console.log(typeof varNull); // object

// 6. A continuación, modifica los valores de las variables por otros del mismo tipo
user = "alejo.ytuza@gmail.com";
cupOfTea = 4;
password = false;
bigInn = 8382829929209210101001010100101010n;
mySymbol = Symbol("carrera de la rata");
unDef = undefined;
varNull = null;

console.log(user, cupOfTea, password, bigInn, mySymbol, unDef, varNull);

// 7. A continuación, modifica los valores de las variables por otros de distinto tipo
user = 43; // Ahora es un number
cupOfTea = "luchar"; // Ahora es un string
password = "ratamon"; // Ahora es un string
bigInn = 838282; // Cambiado de bigint a number
varNull = "millonario"; // Ahora es un string

console.log(user, cupOfTea, password, bigInn, varNull);

// 8. Declara constantes con valores asociados a todos los tipos de datos primitivos
const user2 = "stream"; // string
const age = 13; // number
const intelligent = true; // boolean
const bigInn2 = 383838383883483838383838838383838383883838383838388383838383883838383838n; // bigint
const mySymbol2 = Symbol("Dios"); // symbol
const unDef2 = undefined; // undefined
const varNull2 = null; // null

console.log(user2, age, intelligent, bigInn2, mySymbol2, unDef2, varNull2);

// 9. A continuación, modifica los valores de las constantes
// Esto no es posible ya que las constantes no pueden cambiar su valor.
// Las siguientes líneas producen errores si se descomentan:
/*
user2 = "oso";
age = 45;
intelligent = false;
bigInn2 = 8218181818181818188199191919191919910910302n;
mySymbol2 = Symbol("Jesus");
unDef2 = "evalucion";
varNull2 = "millonario";
*/

// 10. Comenta las líneas que produzcan algún tipo de error al ejecutarse
// Las líneas que intentan modificar constantes ya están comentadas porque generan errores.
