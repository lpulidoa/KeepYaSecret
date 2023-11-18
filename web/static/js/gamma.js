var rmAccents = function (inputText) {
    var accents = "ÁÄáäÓÖóöÉËéÇçÍÏíïÚÜúüÑñ";
    var noAccents = "AAaaOOooEEeeCcIIiiUUuuNn";
    return inputText
        .split(" ")
        .map(function (chr) {
            const accentIndex = accents.indexOf(chr);
            return accentIndex !== -1 ? noAccents[accentIndex] : chr;
        })
        .join("").toLowerCase();
}

var normalizeInput = function (inputText) {
    return rmAccents(inputText)
        .replaceAll(/[^a-zA-Z]/g, "")
        .replaceAll(" ", "")
        .toLowerCase();
}

function ranPermutation() {
    var size = Math.floor(Math.random() * 26);
    while (size == 0) {
        size = Math.floor(Math.random() * 26);
    }
    var arr = new Array(size);
    for (var i = 0; i < arr.length; i++) arr[i] = i;
    var j;
    var temp;
    for (var i = arr.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    return arr;
}

function isAValidPermutation(permutation) {
    var dupMap = {};
    for (var i = 0; i < permutation.length; i++) {
        if (
            permutation.length == 0 ||
            permutation[i] < 0 ||
            permutation[i] > permutation.length - 1
        )
            return false;
        // Verificar duplicados.
        if (dupMap[permutation[i]]) return false;
        dupMap[permutation[i]] = true;
    }
    return true;
}

const dict1 = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
    8: "i",
    9: "j",
    10: "k",
    11: "l",
    12: "m",
    13: "n",
    14: "o",
    15: "p",
    16: "q",
    17: "r",
    18: "s",
    19: "t",
    20: "u",
    21: "v",
    22: "w",
    23: "x",
    24: "y",
    25: "z",
}

const dict = {
    a: 0,
    b: 1,
    c: 2,
    d: 3,
    e: 4,
    f: 5,
    g: 6,
    h: 7,
    i: 8,
    j: 9,
    k: 10,
    l: 11,
    m: 12,
    n: 13,
    o: 14,
    p: 15,
    q: 16,
    r: 17,
    s: 18,
    t: 19,
    u: 20,
    v: 21,
    w: 22,
    x: 23,
    y: 24,
    z: 25,
}

class Node {
    constructor(posX, posY, generation) {
        this.posX = posX;
        this.posY = posY;
        this.numIn = 0;
        this.maxSlope = 0;
        this.nodeOut = [];
        this.generation = generation;
    }
}

function shuffle(array) {
    let currentIndex = array.length,  randomIndex;
  
    // While there remain elements to shuffle.
    while (currentIndex != 0) {
  
      // Pick a remaining element.
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
  
      // And swap it with the current element.
      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
  
    return array;
  }

const alphSize = 26;
var nodes = [];
var map = new Map();

function posToId(x0, y0, x, y, length) {
    var len = length;
    if (x0 < 0) {
        len += Math.abs(x0);
    }
    return (y - y0) * len + (x - x0);
}

function gammaGraph(x0, y0, length, graphType) {
    nodes = [];
    map = new Map();
    var slopes = [];
    var maxY = 25;
    if (y0 <= 0) maxY += Math.abs(y0);
    if (graphType == 1) {
        //natural numbers
        for (var i = 0; i <= maxY; ++i) {
            slopes.push(i);
        }
    } else {
        //triangular numbers
        for (var i = 0; (i * (i + 1)) / 2 <= maxY; ++i) {
            slopes.push((i * (i + 1)) / 2);
        }
    }
    //
    //console.log(slopes);
    //                    Generacion 1
    nodes.push(new Node(x0, y0, 1));
    map.set(posToId(x0, y0, x0, y0, length), nodes.length - 1);
    //console.log(map.get(0));
    var i = 0;
    var generation = 1;
    while (true) {
        var x = nodes[i].posX + 1;
        var y = nodes[i].posY + slopes[i];
        if (x < length && y < alphSize) {
            nodes.push(new Node(x, y, generation));
            nodes[i + 1].numIn++;
            nodes[i + 1].maxSlope = slopes[i];
            nodes[i].nodeOut.push(posToId(x0, y0, x, y, length));
            map.set(posToId(x0, y0, x, y, length), nodes.length - 1);
            ++i;
        } else {
            break;
        }
    }
    //                    Generacion 2
    var size = nodes.length;
    //console.log(size);
    generation = 2;
    for (var i = 1; i < size; ++i) {
        var j = 0;
        var index = i;
        while (true) {
            var x = nodes[index].posX + 1;
            var y = nodes[index].posY + slopes[j];
            var id = posToId(x0, y0, x, y, length);
            if (map.get(id) >= 0) {
                pos = map.get(id);
            } else {
                pos = -1;
            }
            if (x < length && y < alphSize) {
                if (pos == -1) {
                    nodes.push(new Node(x, y, generation));
                    pos = nodes.length - 1;
                    map.set(posToId(x0, y0, x, y, length), pos);
                }
                var exists = false;
                for (var k = 0; k < nodes[index].nodeOut.length; ++k) {
                    if (nodes[index].nodeOut[k] == posToId(x0, y0, x, y, length)) {
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    nodes[pos].numIn++;
                    nodes[pos].maxSlope = Math.max(slopes[j], nodes[pos].maxSlope);
                    nodes[index].nodeOut.push(posToId(x0, y0, x, y, length));
                }
                ++j;
                index = pos;
            } else {
                break;
            }
        }
    }
    //                    Generacion 3
    generation = 3;
    var maxId =
        (length + Math.abs(Math.min(x0, 0))) *
        (alphSize + Math.abs(Math.min(y0, 0)));
    for (var i = 0; i <= maxId; ++i) {
        if (map.get(i) >= 0) {
            var node = nodes[map.get(i)];
            if (node.generation == 2) {
                var j = 0;
                var index = map.get(i);
                var maxSlope = node.maxSlope;
                while (slopes[j] <= maxSlope) {
                    var x = nodes[index].posX + 1;
                    var y = nodes[index].posY + slopes[j];
                    var id = posToId(x0, y0, x, y, length);
                    if (map.get(id) >= 0) {
                        pos = map.get(id);
                    } else {
                        pos = -1;
                    }
                    if (x < length && y < alphSize) {
                        if (pos == -1) {
                            nodes.push(new Node(x, y, generation));
                            pos = nodes.length - 1;
                            map.set(posToId(x0, y0, x, y, length), pos);
                            nodes[pos].numIn++;
                        }
                        var exists = false;
                        for (var k = 0; k < nodes[index].nodeOut.length; ++k) {
                            if (nodes[index].nodeOut[k] == posToId(x0, y0, x, y, length)) {
                                exists = true;
                                break;
                            }
                        }
                        if (!exists) {
                            nodes[pos].numIn++;
                            nodes[pos].maxSlope = Math.max(slopes[j], nodes[pos].maxSlope);
                            nodes[index].nodeOut.push(posToId(x0, y0, x, y, length));
                        }
                        ++j;
                        index = pos;
                    } else {
                        break;
                    }
                }
            }
        }
    }
    return nodes;
}

function calculatePosition(shiftNumber, letter) {
    var res = dict[letter] - shiftNumber;
    res = (res + alphSize) % alphSize;
    return res;
}

function cipher(x0, y0, permutation, clearText, graphType) {
    if (!isAValidPermutation(permutation)) {
        console.log("WHOOPS");
        return;
    }
    text = normalizeInput(clearText);
    size = permutation.length;
    nodes = gammaGraph(x0, y0, size, graphType);
    //console.log(nodes);
    var cipheredText = "";
    var position = 0;
    for (var i = 0; i < text.length; ++i) {
        var y = calculatePosition(permutation[position], clearText[i]);
        var shift = 0;
        if (map.get(posToId(x0, y0, position, y, size)) >= 0) {
            shift = nodes[map.get(posToId(x0, y0, position, y, size))].numIn;
        }
        cipheredText += "(";
        cipheredText += ((shift + dict[clearText[i]]) % alphSize) + "," + y;
        cipheredText += ")";
        if (i < text.length - 1) cipheredText += ",";
        ++position;
        position %= size;
    }
    return cipheredText;
}

function decipher(x0, y0, permutation, cipherText, graphType) {
    if (!isAValidPermutation(permutation)) {
        console.log("WHOOPS");
        return;
    }
    size = permutation.length;
    var clearText = "";
    var position = 0;
    for (var i = 0; i < cipherText.length; ++i) {
        if (cipherText[i] == "(") {
            ++i;
            var a = "";
            while (cipherText[i] != ",") {
                a += cipherText[i];
                ++i;
            }
            ++i;
            var b = "";
            while (cipherText[i] != ")") {
                b += cipherText[i];
                ++i;
            }
        } else continue;
        var c = parseInt(b);
        nodes = gammaGraph(x0, y0, size, graphType);
        var shift = 0;
        if (map.get(posToId(x0, y0, a, b, size)) >= 0) {
            shift = nodes[map.get(posToId(x0, y0, a, b, size))].numIn;
        }
        clearText += dict1[(c + permutation[position]) % alphSize];
        ++position;
        position %= size;
    }

    return clearText;
}

function setLetras(permutation, div = 12, canvas) {
    var letras = [];
    var size = permutation.length;
    var x0 = canvas.width / div;
    var y0 = ((div - 1) * canvas.height) / div;
    var x = canvas.width / div;
    var y = ((div - 1) * canvas.height) / div;
    var i = 0;
    var j = 0;
    var fila = [];
    while (j < alphSize && i < size) {
        var arr = [];
        var arr1 = [];
        arr1.push(x - x0, y - y0);
        arr.push(arr1);
        var letra = dict1[(permutation[i] + j) % alphSize];
        arr.push(letra);
        fila.push(arr);
        ++i;
        x += canvas.width / size + 8;
        if (i == size) {
            i = 0;
            x = canvas.width / div;
            j++;
            y -= canvas.height / (alphSize + 2);
            letras.push(fila);
            fila = [];
        }
    }
    console.log(letras)
    return letras;
}

function drawP(permutation, x0 = 0, y0 = 0, canvas, context) {
    var size = permutation.length;
    var div = 12;
    var letras = setLetras(permutation, div, canvas);
    //lineas del plano
    var colorLineas = "92e326";
    //x
    // context.beginPath();
    // context.moveTo(canvas.width / div - x0, 0);
    // context.lineTo(canvas.width / div - x0, canvas.height);
    // context.lineWidth = 1;
    // context.strokeStyle = "#" + colorLineas;
    // context.stroke();
    // //y
    // context.beginPath();
    // context.moveTo(0, ((div - 1) * canvas.height) / div - y0);
    // context.lineTo(canvas.width, ((div - 1) * canvas.height) / div - y0);
    // context.lineWidth = 1;
    // context.strokeStyle = "#" + colorLineas;
    // context.stroke();
    //lineas del plano
    //dibujar coordenadas
    // context.beginPath();
    //context.font = "[style] [variant] [weight] [size]/[line height] [font family]";
    var sizeFont = 11; //Tamaño letra
    context.font = sizeFont + "px " + "Spline Sans Mono, sans-serif";
    var i = 0;
    var j = 0;
    // var x = canvas.width / div - x0;
    // var y = ((div - 1) * canvas.height) / div - y0;
    var x = 6
    var y = ((div - 1) * canvas.height) / div - y0;
    context.moveTo(x, y);
    // console.log(letras);

    /**/
    // context.beginPath();
    // context.arc(x, y, 5, Math.PI / 2, Math.PI, true);

    for (var i = 0; i < alphSize; ++i) {
        for (var j = 0; j < size; ++j) {
            var letra = letras[i][j][1];
            var text = letra + "(" + j + "," + i + ")";
            context.fillStyle = "#EFF1F3"
            context.fillText(text, x + letras[i][j][0][0], y + letras[i][j][0][1]);
        }
    }
    context.stroke();
}

function drawPermutation(permutation, canvas, context) {
    if (permutation.length > 0 && permutation.length <= alphSize) {
        drawP(permutation, 0, 0, canvas, context)
        // window.addEventListener("keydown", checkKeyPressed, false);
        // var i = 0;
        // var j = 0;
        // function checkKeyPressed(e) {
        //     if (e.keyCode == "37") {
        //         i -= 10;
        //     }
        //     if (e.keyCode == "38") {
        //         j -= 10;
        //     }
        //     if (e.keyCode == "39") {
        //         i += 10;
        //     }
        //     if (e.keyCode == "40") {
        //         j += 10;
        //     }
        //     context.clearRect(0, 0, canvas.width, canvas.height);
        //     drawP(permutation, i, j, canvas, context);
        // }
    }
}

function drawG(nodes, x0, y0, movX, movY, size, canvas, context) {
    var div = 20;
    //lineas del plano
    var colorLineas = "EDFFAB";
    var posx = canvas.width / div;
    var posy = ((div - 1) * canvas.height) / div;
    var movx = canvas.width / div;
    var movy = canvas.height / div;
    context.beginPath();
    context.moveTo(posx - movx * x0 - movX, 0);
    context.lineTo(posx - movx * x0 - movX, canvas.height);
    context.lineWidth = 1;
    context.strokeStyle = "#" + colorLineas;
    context.stroke();
    //y
    context.beginPath();
    context.moveTo(0, posy + movy * y0 - movY);
    context.lineTo(canvas.width, posy + movy * y0 - movY);
    context.lineWidth = 1;
    context.strokeStyle = "#" + colorLineas;
    context.stroke();
    //lineas del plano
    //punto inicial
    context.beginPath();
    context.lineWidth = 1;
    context.strokeStyle = "#4062BB";
    context.fillStyle = "#4062BB";
    context.arc(posx - movX, posy - movY, 3, 0, 2 * Math.PI, true);
    context.fill();
    context.stroke();
    //grid con nodos de coordenada
    for (var i = 0; i < size; ++i) {
        for (var j = 0; j < alphSize; ++j) {
            context.beginPath();
            context.lineWidth = 1;
            context.strokeStyle = "#EFF1F3";
            context.fillStyle = "#EFF1F3";
            context.arc(
                posx - movx * (x0 - i) - movX,
                posy + movy * (y0 - j) - movY,
                1,
                0,
                2 * Math.PI,
                true
            );
            context.fill();
            context.stroke();
        }
    }
    //dibujo y conexiones de nodos
    for (var i = 0; i < nodes.length; ++i) {
        var node = nodes[i];
        if (i != 0) {
            context.beginPath();
            context.lineWidth = 0.25;
            context.strokeStyle = "#87D68D";
            context.fillStyle = "#87D68D";
            context.arc(
                posx - movx * (x0 - node.posX) - movX,
                posy + movy * (y0 - node.posY) - movY,
                2,
                0,
                2 * Math.PI,
                true
            );
            context.fill();
            context.stroke();
        }
        var colorUnion = "87D68D";
        for (var j = 0; j < node.nodeOut.length; ++j) {
            var pos2X = nodes[map.get(node.nodeOut[j])].posX;
            var pos2Y = nodes[map.get(node.nodeOut[j])].posY;
            context.beginPath();
            context.moveTo(
                posx - movx * (x0 - node.posX) - movX,
                posy + movy * (y0 - node.posY) - movY
            );
            context.lineTo(
                posx - movx * (x0 - pos2X) - movX,
                posy + movy * (y0 - pos2Y) - movY
            );
            context.lineWidth = 1;
            context.strokeStyle = "#" + colorUnion;
            context.stroke();
        }
    }
}

function drawGammaGraph(nodes, x0, y0, size, canvas, context) {
    drawG(nodes, x0, y0, 0, 0, size, canvas, context);
    window.addEventListener("keydown", checkKeyPressed, false);
    var i = 0;
    var j = 0;
    function checkKeyPressed(e) {
        if (e.keyCode == "37") {
            i -= 10;
        }
        if (e.keyCode == "38") {
            j -= 10;
        }
        if (e.keyCode == "39") {
            i += 10;
        }
        if (e.keyCode == "40") {
            j += 10;
        }
        context.clearRect(0, 0, canvas.width, canvas.height);
        drawG(nodes, x0, y0, i, j, size, canvas, context);
    }
}

var graphCanvas = document.querySelector("#graphCanvas");
var graphContext = graphCanvas.getContext("2d");
var graphWidth = graphCanvas.width;
var graphHeight = graphCanvas.height;

var permCanvas = document.querySelector("#permCanvas");
var permContext = permCanvas.getContext("2d");
var permWidth = permCanvas.width;
var permHeight = permCanvas.height;

document.addEventListener("keydown", function (e) {
    if([37, 38, 39, 40].indexOf(e.keyCode) > -1){
      e.preventDefault();
      // Do whatever else you want with the keydown event (i.e. your navigation).
    }
}, false)

document.getElementById('encrypt').onclick = function() {
    graphContext.clearRect(0, 0, graphCanvas.width, graphCanvas.height)
    permContext.clearRect(0, 0, permCanvas.width, permCanvas.height)


    var inputCoordX = document.getElementById("coordX").value
    var inputCoordY = document.getElementById("coordY").value
    var inputPermutation = document.getElementById("permutation").value
    var inputText = document.getElementById("text-encrypt").value

    if (inputText == ""){
        console.log("Must write some text") 
    } else {
        inputText = rmAccents(inputText)
    }
    
    if (inputCoordX == "") {
        inputCoordX = 0
        document.getElementById("coordX").value += 0
    } else {
        inputCoordX = parseInt(inputCoordX)
    }

    if (inputCoordY == "") {
        inputCoordY = 0
        document.getElementById("coordY").value += 0
    } else {
        inputCoordY = parseInt(inputCoordY)
    }

    if (inputPermutation == "") {
        inputPermutation = shuffle([0, 1, 2, 3, 4, 5, 6, 7, 8])
    } else {
        var permutationList = inputPermutation.split(",")
        .map(function (x) { 
            return parseInt(x, 10)
        })
        if (!isAValidPermutation(permutationList)) {
            inputPermutation = shuffle([0, 1, 2, 3, 4, 5, 6, 7, 8])
        } else {
            inputPermutation = permutationList
        }
    }

    document.getElementById("coordX").value = ""
    document.getElementById("coordY").value = ""
    document.getElementById("permutation").value = ""
    document.getElementById("text-encrypt").value = ""
    document.getElementById("text-decrypt").value = ""

    var outputText = cipher(inputCoordX, inputCoordY, inputPermutation, inputText, 1)
    document.getElementById("coordX").value = inputCoordX
    document.getElementById("coordY").value = inputCoordY
    document.getElementById("permutation").value = inputPermutation
    document.getElementById("text-encrypt").value = inputText
    document.getElementById("text-decrypt").value += outputText

    var nodes = gammaGraph(inputCoordX, inputCoordY, inputPermutation.length, 1)
    drawGammaGraph(nodes, inputCoordX, inputCoordY, inputPermutation.length, graphCanvas, graphContext)
    drawPermutation(inputPermutation, permCanvas, permContext)
    
}

document.getElementById('decrypt').onclick = function() {
    graphContext.clearRect(0, 0, graphCanvas.width, graphCanvas.height)
    permContext.clearRect(0, 0, permCanvas.width, permCanvas.height)

    var inputCoordX = document.getElementById("coordX").value
    var inputCoordY = document.getElementById("coordY").value
    var inputPermutation = document.getElementById("permutation").value
    var inputText = document.getElementById("text-decrypt").value

    

    if (inputCoordX == "") {
        console.log("error")
    } else {
        inputCoordX = parseInt(inputCoordX)
    }

    if (inputCoordY == "") {
        console.log("error")
    } else {
        inputCoordY = parseInt(inputCoordY)
    }

    if (inputPermutation == "") {
        console.log("error")
    } else {
        var permutationList = inputPermutation.split(",")
        .map(function (x) { 
            return parseInt(x, 10)
        })
        if (!isAValidPermutation(permutationList)) {
            console.log("error")
        } else {
            inputPermutation = permutationList
        }
    }

    document.getElementById("coordX").value = ""
    document.getElementById("coordY").value = ""
    document.getElementById("permutation").value = ""
    document.getElementById("text-encrypt").value = ""
    document.getElementById("text-decrypt").value = ""
    
    var outputText = decipher(inputCoordX, inputCoordY, inputPermutation, inputText, 1)
    document.getElementById("coordX").value = inputCoordX
    document.getElementById("coordY").value = inputCoordY
    document.getElementById("permutation").value = inputPermutation
    document.getElementById("text-encrypt").value = outputText
    document.getElementById("text-decrypt").value = inputText

    var nodes = gammaGraph(inputCoordX, inputCoordY, inputPermutation.length, 1)
    drawGammaGraph(nodes, inputCoordX, inputCoordY, inputPermutation.length, graphCanvas, graphContext)
    drawPermutation(inputPermutation, permCanvas, permContext)
    
}
     


