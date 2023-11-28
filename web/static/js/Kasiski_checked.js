// unchecked functions

function printArray(array) {
    console.log("Array:");
    for (const element of array) {
        console.log(element);
    }
}

function printKeysDict(keysDict) {
    console.log("Keys Dictionary:");

    for (const key in keysDict) {
        const [value, textAndKeys] = keysDict[key];
        
        console.log(`Key Size: ${key}`);
        console.log(`Value: ${value}`);
        
        console.log("Text and Keys:");
        for (const arrayTK of textAndKeys) {
            printArray(arrayTK);
        }

        console.log("\n");
    }
}
function product(...arrays) {
    if (arrays.length === 0) return [[]];

    const result = [];

    function cartesianProduct(index, current) {
        if (index === arrays.length) {
            result.push(current.slice());
            return;
        }

        for (const element of arrays[index]) {
            current[index] = element;
            cartesianProduct(index + 1, current);
        }
    }

    cartesianProduct(0, []);

    return result;
}

function extractKeys(mgDictionary) {
    const extractedKeys = [];

    // Convert the values of mgDictionary to an array
    const mgValuesArray = Object.values(mgDictionary);

    // Use the product function to get all combinations
    for (const combination of product(...mgValuesArray)) {
        const charString = combination.map(pair => String.fromCharCode(65 + parseInt(pair[0]))).join('');
        const avgScore = +(combination.reduce((acc, pair) => acc + pair[1], 0) / combination.length).toFixed(3);

        extractedKeys.push([charString, avgScore]);
    }

    return extractedKeys;
}



//CONSTANTS

const spanishFrequencies = [0.1253, 0.0142, 0.0468, 0.0586, 0.1368, 0.0069, 0.0101, 0.007, 0.0625, 0.0044, 0.0002, 0.0497, 0.0315, 0.0702, 0.0868, 0.0251, 0.0088, 0.0687, 0.0798, 0.0463, 0.0393, 0.009, 0.0001, 0.0022, 0.009, 0.0052];
const englishFrequencies = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074];
const englishValue = +(englishFrequencies.map(i => i**2).reduce((acc, val) => acc + val)).toFixed(3);
const spanishValue = +(spanishFrequencies.map(i => i**2).reduce((acc, val) => acc + val)).toFixed(3);
const languages = {'english': [englishFrequencies, englishValue], 'spanish': [spanishFrequencies, spanishValue]};
const randomValue = 0.038;
const ALPHABET="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

//AUX FOR TESTING

function print2DArray(array2D) {
    for (let i = 0; i < array2D.length; i++) {
        for (let j = 0; j < array2D[i].length; j++) {
            console.log(array2D[i][j]);
        }
    }
}

//KASISKI TEST
//
//Aux Functions for Kasiski Test

function gcd(a, b) {
    while (b) {
        [a, b] = [b, a % b];
    }
    return a;
}

function gcdCounts(numbers, gcdDict) {
    for (let i = 0; i < numbers.length; i++) {
        for (let j = i + 1; j < numbers.length; j++) {
            const commonDivisor = gcd(numbers[i], numbers[j]);

            if (!(commonDivisor in gcdDict)) {
                gcdDict[commonDivisor] = 1;
            } else {
                gcdDict[commonDivisor]++;
            }
        }
    }

    return gcdDict;
}

function factorizeNumber(number, factorsDict) {
    for (let i = 2; i <= Math.sqrt(number); i++) {
        if (number % i === 0) {
            factorsDict[i] = (factorsDict[i] || 0) + 1;
            factorsDict[number / i] = (factorsDict[number / i] || 0) + 1;
        }
    }
}

function findRepeatingDistances(inputString, minLength = 3, maxLength = 5) {
    const repeatingDistances = [];
    const substringPositions = {};

    for (let length = minLength; length <= maxLength; length++) {
        for (let i = 0; i < inputString.length - length + 1; i++) {
            const substring = inputString.substring(i, i + length);
            if (substring in substringPositions) {
                const distance = i - substringPositions[substring];
                repeatingDistances.push(distance);
            }
            substringPositions[substring] = i;
        }
    }

    return repeatingDistances;
}


function factorizeOrGcd(numbers, outputSize) {
    const factorsDict = {};

    for (const number of numbers) {
        try {
            factorizeNumber(number, factorsDict);
        } catch (error) {
            //console.log("Factorization took too long. Calculating GCD instead.");
            return gcdCounts(numbers, factorsDict);
        }
 
    }

    const arrayFactors = Object.entries(factorsDict).map(([key, value]) => [parseInt(key), value]);
    arrayFactors.push([1, 0]);
    const sortedFactors = arrayFactors
        .sort((a, b) => b[1] - a[1])
        .slice(0, outputSize);

    return sortedFactors;
}

//Kasiski Test -Checked
function kasiskiTest(inputString, minLength = 3, maxLength = 5, outputNumber = 5) {
    const distances = findRepeatingDistances(inputString, minLength, maxLength);
    const potentialKeyLengths = factorizeOrGcd(distances, outputNumber).map(row => row[0]);

    return potentialKeyLengths;
}

//FREQUENCE COMPARISON

//Aux functions frequence comparison
function arrangeTextInMatrix(text, m) {
    // Initialize the 2D matrix with empty strings
    const matrix = Array.from({ length: m }, () => '');

    // Populate the matrix with characters from the text
    for (let i = 0; i < text.length; i++) {
        const row_index = i % m;
        matrix[row_index] += text[i];
    }

    return matrix;
}

function charFreq(inputString) {
    // Uses an object to store frequencies
    const frequencies = {};
    for (const char of inputString) {
        // Skip non-alphabetic characters
        if (/[a-zA-Z]/.test(char)) {
            frequencies[char] = (frequencies[char] || 0) + 1;
        }
    }
    return frequencies;
}

function IC(text) {
    // Calculate frequencies of characters in the text
    const charFrequencies = charFreq(text);

    // Calculate the sum of freq comb 2
    const sumOfSquares = Object.values(charFrequencies).reduce((acc, freq) => acc + freq * (freq - 1), 0);

    // Calculate the index of coincidence
    const textLength = text.length;
    const ic = +(sumOfSquares / (textLength * (textLength - 1))).toFixed(3);

    return ic;
}

function isCloseEnough(rValue, expValue, testValue) {
    const maxDistance = +(Math.abs(rValue - expValue) / 2).toFixed(3);
    const goodIC = Math.abs(expValue - testValue) < maxDistance;
    return goodIC;
}

//Determine best key sizes
function bestKeySizes(plainText, numSizes, targetIC) {
    const possibleSizes = kasiskiTest(plainText);
    const keysScore = {};

    for (const m of possibleSizes) {
        const matrixText = arrangeTextInMatrix(plainText, m);
        let averageIC = 0;

        for (let i = 0; i < matrixText.length; i++) {
            averageIC += IC(matrixText[i]);
        }

        averageIC /= matrixText.length;
        keysScore[m] = +(averageIC.toFixed(3));
    }

    const sortedIC = Object.keys(keysScore)
        .map(m => [parseInt(m), keysScore[m], +(Math.abs(keysScore[m] - targetIC).toFixed(3))])
        .sort((a, b) => a[2] - b[2]);

    const bestLens = [];

    for (const l of sortedIC) {
        if (!new Set([1, 2]).has(l[0])) {
            bestLens.push([l[0], l[1]]);
        }

        if (bestLens.length === numSizes) {
            break;
        }
    }

    // If there are no other options, add the best one available
    if (bestLens.length === 0) {
        bestLens.push([sortedIC[0][0], sortedIC[0][1]]);
    }
    return bestLens;
}


//FINDING KEY


function shiftDict(dictionary, shift) {
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const shiftedAlphabet = alphabet.slice(shift) + alphabet.slice(0, shift);
    const shiftedDict = Object.fromEntries([...alphabet].map((k, i) => [k, dictionary[shiftedAlphabet[i]] || 0]));

    return shiftedDict;
}


function MgFilter(mgArray, target) {
    const indexedDiff = mgArray.map((value, i) => [i, value, Math.abs(value - target)]);

    // Sort the list by absolute difference in descending order
    const sortedIndexedDiff = indexedDiff.sort((a, b) => a[2] - b[2]);

    // Extract the sorted array
    const sortedArray = sortedIndexedDiff.map(([index, value]) => [index, value]);
    const bestScores = sortedArray.slice(0, 3);
    const bestScore = bestScores[0];

    // Filter other options based on closeness
    const otherOptions = bestScores.slice(1).filter(mg => isCloseEnough(randomValue, target, mg[1]));

    // Combine bestScore and otherOptions into a single list
    const filteredScores = [bestScore, ...otherOptions];

    return filteredScores;
}

function calculateMg(inputString, keySize, languageFrequencies, languageIC) {
    const matrix = arrangeTextInMatrix(inputString, keySize);
    const bestKeys = {};
    let strCounter = 0;

    for (const string of matrix) {
        const Mgs = [];
        const charFreqDict = charFreq(string);

        for (let g = 0; g < 26; g++) {
            const shiftedCharFreqDict = shiftDict(charFreqDict, g);
            const dotProduct = languageFrequencies.reduce((acc, val, i) => acc + val * Object.values(shiftedCharFreqDict)[i], 0);
            const Mg = +(dotProduct / string.length).toFixed(3);
            Mgs.push(Mg);
        }

        const filteredMgs = MgFilter(Mgs, languageIC);
        bestKeys[strCounter] = filteredMgs;
        strCounter++;
    }

    return bestKeys;
}

function printMg(mgDictResult){
console.log("Mg Dictionary:");
for (const strCounter in mgDictResult) {
    console.log(`String Counter: ${strCounter}`);
    const mgScores = mgDictResult[strCounter];
    
    for (const [keySize, mgScore] of mgScores) {
        console.log(`  Key Size: ${keySize}, Mg Score: ${mgScore}`);
    }
}}
//VIGENERE DECRYPTION


function vigenereDecryptKey(frase, clave) {
    if (clave.replace(/\s/g, '').match(/^[A-Za-z]+$/)) {
        const claveList = [...clave.toUpperCase()].map(letra => ALPHABET.indexOf(letra));
        let newFrase = '';
        let contador = 0;

        for (const letra of frase) {
            const decryptedLetter = ALPHABET[(ALPHABET.indexOf(letra.toUpperCase()) - claveList[contador] + ALPHABET.length) % ALPHABET.length];
            newFrase += decryptedLetter;
            contador = (contador + 1) % clave.length;
        }

        return newFrase;
    } else {
        console.log("The key must be a word or a phrase made up of letters.");
    }
}



//


function constructStrings(keysDict) {
    let finalString = '';

    for (const key in keysDict) {
        const textAndKeys = keysDict[key][1];

        // Concatenate the first elements of the second elements of each array
        const firstElementsConcat = textAndKeys.map(item => item[0]).join('');
        finalString += firstElementsConcat+"\n";

        // Concatenate the second elements of the second elements of each array
        const secondElementsConcat = textAndKeys.map(item => item[1]).join('');
        finalString += secondElementsConcat+"\n";

        // Concatenate all the first elements of the arrays
        finalString += keysDict[key][0]+"\n";
    }
    return finalString
}

function vigenereCryptanalysis(inputText, langInfo = languages['english']) {
    const keysDict = {};
    let keySizes = bestKeySizes(inputText, 20, langInfo[1]);

    if (keySizes.length >= 1) {
        const bestKeySize = [keySizes[0], keySizes[1]];
        const secondOptions = keySizes.slice(1).filter(key => isCloseEnough(randomValue, langInfo[1], key[1]));
        keySizes = [...bestKeySize, ...secondOptions];
    }

    let bestI = 0;
    let mgDict;

    for (const item of keySizes) {
        if (bestI === 0) {
            bestI = item[0];
        }

        const m = item[0];
        const value = item[1];

        if (m < 11) {
            // Call the calculateMg function for each key in size_scores
            mgDict = calculateMg(inputText, m, langInfo[0], langInfo[1]);
            const keys = extractKeys(mgDict);
            const textAndKeys = keys.map(key => [key[0], vigenereDecryptKey(inputText, key[0])]);

            // Append the corresponding value from size_scores and the mg_dict to the result list
            keysDict[m] = [value, textAndKeys];
        }
    }
    results=constructStrings(keysDict);
    console.log(results);

    return results;
}


//const text="RLWSWWYRVBINCPGNQWLXGDGGKTMRIJQCKRIEQXZYXSPISZPWRSDCEJLEFBEVYTLUMLFSMRJGJPGUMFEIPNPAAMLGRKRVMAXAMRKZCMQMFEEDESJGXZKWSLHKRELGWLGGSJQGBIDQXGYRSJCKCEFBHJYAALJWPIFAIKDVGKTSRXWPRKGRVYXS"
//const testVigAnalysis = vigenereCryptanalysis(text, languages['english']);

